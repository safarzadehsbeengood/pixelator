import click
from PIL import Image

from app.pixelate import pixelate


@click.command()
@click.argument("path_to_image", type=click.Path(exists=True))
@click.argument("pixel_size", type=int)
def cli(path_to_image, pixel_size):
    img = Image.open(path_to_image)
    pixelate(img, pixel_size).show()


if __name__ == "__main__":
    cli()
