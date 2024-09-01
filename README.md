## A tiny image pixelator.
Depending on your `pixellation_factor`, this algorithm goes through an image by blocks of pixels, takes the average of the RGB values, and creates a pixellized image from it.

Setup:
```bash
$ git clone https://github.com/safarzadehsbeengood/pixelator.git
$ cd pixelator
$ python3 -m venv .
$ source bin/activate
$ pip install -r requirements.txt
```

Usage:
```bash
$ python3 pixelator.py [path_to_image] [pixellation_factor]
```
