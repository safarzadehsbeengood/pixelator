import shutil
import time
from pathlib import Path

from django.apps import AppConfig

# Sessions older than this are deleted on startup
SESSION_MAX_AGE_SECONDS = 3600


class AppConfig(AppConfig):
    name = "app"

    def ready(self):
        from django.conf import settings

        media_root = Path(settings.MEDIA_ROOT)
        if not media_root.exists():
            return

        now = time.time()
        for entry in media_root.iterdir():
            if not entry.is_dir():
                continue
            age = now - entry.stat().st_mtime
            if age > SESSION_MAX_AGE_SECONDS:
                shutil.rmtree(entry)
