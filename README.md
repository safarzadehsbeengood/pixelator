# Pixelator

Converts images into pixel art by dividing them into blocks, averaging the RGB values within each block, and scaling back up. Block size is configurable — larger blocks = more pixelated.

## Web App

Upload an image and explore different pixel sizes interactively via a slider (24–128px, step 4). The image is pre-processed at all sizes on upload, so the slider updates instantly.

**Setup:**
```bash
git clone https://github.com/safarzadehsbeengood/pixelator.git
cd pixelator
uv sync
uv run python manage.py runserver
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000).

## CLI

```bash
uv run pixelate <path_to_image> <pixel_size>
```

**Example:**
```bash
uv run pixelate ./imgs/napoleon.jpg 32
```

Opens the pixelated result in your default image viewer.

## Requirements

- [uv](https://docs.astral.sh/uv/) — `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Python 3.12+
