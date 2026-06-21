import numpy as np
from PIL import Image


def pixelate(img: Image.Image, pixel_size: int) -> Image.Image:
    arr = np.array(img.convert("RGB"))
    h, w, _ = arr.shape
    h_trim = (h // pixel_size) * pixel_size
    w_trim = (w // pixel_size) * pixel_size
    arr = arr[:h_trim, :w_trim]
    blocks = arr.reshape(h_trim // pixel_size, pixel_size, w_trim // pixel_size, pixel_size, 3)
    averaged = blocks.mean(axis=(1, 3)).astype(np.uint8)
    expanded = np.repeat(np.repeat(averaged, pixel_size, axis=0), pixel_size, axis=1)
    return Image.fromarray(expanded, mode="RGB")
