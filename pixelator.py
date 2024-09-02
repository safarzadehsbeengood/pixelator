import PIL
import PIL.Image
import PIL.JpegImagePlugin
import numpy as np
import sys
from tqdm import tqdm

if len(sys.argv) < 3 or len(sys.argv) > 3 or any(c.isalpha() for c in sys.argv[2]):
    print("Usage: python3 pixelator.py [path_to_image] [pixel_size]")
    print("(e.g. python3 pixelator.py ./4k.jpg 10)")
    sys.exit()

image_name = sys.argv[1] 
pix = sys.argv[2]

def matricize_pixel_data(pixel_data, img_size):
    with tqdm(total=len(pixel_data), desc="Reshaping original pixels") as pbar:
        matrix = [[] for _ in range(img_size[1])]
        for i in range(len(pixel_data)):
            matrix[i // img_size[0]].append(pixel_data[i])
            pbar.update()
        return matrix

def summarize_block(matrix, i, j, pixel_size):
    sum_r, sum_g, sum_b = 0, 0, 0
    for y in range(i, i+pixel_size):
        for x in range(j, j+pixel_size):
            sum_r += matrix[y][x][0]
            sum_g += matrix[y][x][1]
            sum_b += matrix[y][x][2]
    return (sum_r//(pixel_size**2), sum_g//(pixel_size**2), sum_b//(pixel_size**2))

def get_img_pixelized(img: PIL.JpegImagePlugin.JpegImageFile, pixel_size: int):
    print("Getting image data...")
    pixel_data = list(img.getdata())
    img_width, img_height = img.size
    # make list of "summary" pixels
    matrix = matricize_pixel_data(pixel_data, (img_width, img_height))
    summarized_img = [[] for _ in range(img_height // pixel_size)]
    with tqdm(total=(img_height // pixel_size) * (img_width // pixel_size), desc="Summarizing...") as pbar:
        for i in range(0, img_height-pixel_size, pixel_size):
            for j in range(0, img_width-pixel_size, pixel_size):
                summary = summarize_block(matrix, i, j, pixel_size)
                pbar.update(1)
                summarized_img[(i // pixel_size)].append(summary)
        for i in range(len(summarized_img)):
            for j in range(len(summarized_img[i])):
                summarized_img[i][j] = list(summarized_img[i][j])
    if not summarized_img[-1]:
        summarized_img.pop()
    summarized_img = expand_img(summarized_img, pixel_size)
    print("Reshaping...")
    np_img = np.array(reshape_matrix(summarized_img))
    print("Creating image...")
    res = PIL.Image.fromarray(np_img, mode="RGB")
    return res

def expand_img(pixels: list[list[tuple[int, int, int]]], pixel_size: int):
    # expand horizontally first
    with tqdm(colour="green", total=(len(pixels))*(len(pixels[0]))+(len(pixels)-1), desc="Expanding image") as pbar:
        for i in range(len(pixels)-1, -1, -1): # list
            for j in range(len(pixels[0])-1, -1, -1): # list
                tup = pixels[i][j]
                for _ in range(pixel_size):
                    pixels[i].insert(j, tup)
                pbar.update()
        for i in range(len(pixels)-1, -1, -1):
            for _ in range(pixel_size):
                pixels.insert(i, pixels[i])
            pbar.update()
        return pixels
                

def reshape_matrix(m):
    return np.array(m, dtype=np.uint8)
            
img = PIL.Image.open(image_name)
summary = get_img_pixelized(img, int(pix))
print("Showing image...")
summary.show()
