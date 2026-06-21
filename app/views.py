import uuid

from django.conf import settings
from django.http import JsonResponse
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
    for size in PIXEL_SIZES:
        if (h // size) == 0 or (w // size) == 0:
            continue
        logger.log(logging.INFO, f"Size {size} processing...")
        pixelate(img, size).save(session_dir / f"{size}.jpg", "JPEG", quality=85)
        logger.log(logging.INFO, f"Size {size} finished.")

    return JsonResponse({"session_id": session_id, "sizes": PIXEL_SIZES})
