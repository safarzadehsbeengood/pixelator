# Pixelator

Converts images into pixel art by dividing them into blocks, averaging the RGB values within each block, and scaling back up. Block size is configurable — larger blocks = more pixelated.

## Web App (local dev)

```bash
git clone https://github.com/safarzadehsbeengood/pixelator.git
cd pixelator
uv sync
uv run python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

## CLI

```bash
uv run pixelate <path_to_image> <pixel_size>
```

```bash
uv run pixelate ./imgs/napoleon.jpg 32
```

Opens the pixelated result in your default image viewer.

## Requirements

- [uv](https://docs.astral.sh/uv/) — `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Python 3.12+

---

## Deploying on a Raspberry Pi via Cloudflare Tunnel

Exposes the app publicly through your own domain with no open ports or dynamic DNS.

### 1. Prerequisites

- Docker installed on the Pi — `curl -fsSL https://get.docker.com | sh`
- A domain managed by Cloudflare
- `cloudflared` installed on the Pi:

```bash
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64 \
  -o cloudflared
sudo mv cloudflared /usr/local/bin/ && sudo chmod +x /usr/local/bin/cloudflared
```

> Use `cloudflared-linux-arm` for 32-bit Pi OS.

### 2. Build and run the container

Generate a secret key:
```bash
python3 -c "import secrets; print(secrets.token_hex(50))"
```

Build the image and start the container:
```bash
git clone https://github.com/safarzadehsbeengood/pixelator.git
cd pixelator
docker build -t pixelator .

docker run -d \
  --name pixelator \
  --restart unless-stopped \
  -p 127.0.0.1:8000:8000 \
  -e DJANGO_SECRET_KEY="<your-generated-key>" \
  -e DJANGO_ALLOWED_HOSTS="pixel.yourdomain.com" \
  pixelator
```

The container only binds to `127.0.0.1` — it is not reachable from outside the Pi until cloudflared is running.

### 3. Configure the Cloudflare Tunnel

Log in (opens a browser window — run this on a machine with a browser, or use a token):
```bash
cloudflared login
```

Create the tunnel:
```bash
cloudflared tunnel create pixelator
```

Create `~/.cloudflared/config.yml`:
```yaml
tunnel: pixelator
credentials-file: /home/pi/.cloudflared/<UUID>.json

ingress:
  - hostname: pixel.yourdomain.com
    service: http://127.0.0.1:8000
  - service: http_status:404
```

Replace `<UUID>` with the filename created by `tunnel create` (shown in output, also in `~/.cloudflared/`).

Add the DNS record (creates a CNAME automatically in your Cloudflare dashboard):
```bash
cloudflared tunnel route dns pixelator pixel.yourdomain.com
```

### 4. Run cloudflared as a service

```bash
sudo cloudflared service install
sudo systemctl enable --now cloudflared
```

### 5. Update Django settings

In `config/settings.py`, add your subdomain to `CSRF_TRUSTED_ORIGINS` so uploads aren't rejected:

```python
CSRF_TRUSTED_ORIGINS = ["https://pixel.yourdomain.com"]
```

Then rebuild the container:
```bash
docker build -t pixelator .
docker restart pixelator
```

### Updating the app

```bash
git pull
docker build -t pixelator .
docker stop pixelator && docker rm pixelator
docker run -d \
  --name pixelator \
  --restart unless-stopped \
  -p 127.0.0.1:8000:8000 \
  -e DJANGO_SECRET_KEY="<your-generated-key>" \
  -e DJANGO_ALLOWED_HOSTS="pixel.yourdomain.com" \
  pixelator
```
