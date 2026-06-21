import json
import shutil
import uuid

from django.conf import settings
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from PIL import Image, UnidentifiedImageError
import logging

from .pixelate import pixelate

PIXEL_SIZES = list(range(24, 129, 4))

logger = logging.getLogger(__name__)


def index(request):
    return render(request, "app/index.html")


def upload(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        img = Image.open(request.FILES["image"]).convert("RGB")
    except (KeyError, UnidentifiedImageError, Exception):
        return JsonResponse({"error": "Invalid or missing image file"}, status=400)

    session_id = str(uuid.uuid4())
    session_dir = settings.MEDIA_ROOT / session_id
    session_dir.mkdir(parents=True)

    w, h = img.size
    sizes = [s for s in PIXEL_SIZES if (h // s) > 0 and (w // s) > 0]
    total = len(sizes)

    def generate():
        for i, size in enumerate(sizes):
            logger.info("Size %d processing...", size)
            pixelate(img, size).save(session_dir / f"{size}.jpg", "JPEG", quality=85)
            logger.info("Size %d finished.", size)
            yield json.dumps({"progress": (i + 1) / total}) + "\n"
        yield json.dumps({"done": True, "session_id": session_id, "sizes": PIXEL_SIZES}) + "\n"

    return StreamingHttpResponse(generate(), content_type="application/x-ndjson")


def delete_session(request, session_id):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    # Sanitise: session_id must be a valid UUID to prevent path traversal
    try:
        uuid.UUID(session_id)
    except ValueError:
        return JsonResponse({"error": "Invalid session"}, status=400)

    session_dir = settings.MEDIA_ROOT / session_id
    if session_dir.exists():
        shutil.rmtree(session_dir)
        logger.info("Deleted session %s", session_id)

    return JsonResponse({"ok": True})
