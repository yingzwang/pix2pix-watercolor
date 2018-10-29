from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import glob
import os

import imageio
from PIL import Image, ImageFont, ImageDraw
import numpy as np

# python tools/make_gif.py --im_duration 1.2 --max_steps 600  --im_size 256

def get_main_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--images_dir", type=str, default="results/v/train_gif/images", help="folder of input png images")
    parser.add_argument("--fnm", type=str, default="1", choices=["1", "2"], help="input png filename")
    parser.add_argument("--output_dir", type=str, default="results/v/train_gif")
    parser.add_argument("--im_size", type=int, default=256, help="output gif size")
    parser.add_argument("--font_size", type=int, default=20, help="text size on gif")
    parser.add_argument("--im_duration", type=float, default=0.1, help="gif duration per frame")
    parser.add_argument("--max_steps", type=int, default=100, help="max training steps to plot")
    parser.add_argument("--skip_steps", type=int, default=1, help="skipping steps")
    parser.add_argument("--fnm_gif", type=str, default="test.gif", help="output gif filename")
    a = parser.parse_args()
    return a


def get_step_num(file_path):
    """ 
    get step number from file name
    INPUT
    ------
    file_path: e.g., 'results/v/train1/images/00000050-1-outputs.png'
    OUTPUT
    ------
    step_num: e.g., 50
    """
    name, _ = os.path.splitext(os.path.basename(file_path)) # name: '00000050-2-outputs'
    dlen = 8 # length of the digits
    name = name[:dlen] # e.g., '00000050'
    step_num = int(name)
    return step_num

def add_text_to_image(image, text, font):
    layer = Image.new('RGBA', image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(layer)
    w, h = draw.textsize(text, font=font)
    ww, hh = image.size
    x, y = (ww - w) / 2, (hh - h) / 2 # center of the image
    #x, y = w / 2, hh - (h * 1.5) # lower left of the image
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 180))
    image = Image.alpha_composite(image, layer)
    return image


def get_png_paths(images_dir, fnm="1"):
    """
    search for the png files
    """
    if not os.path.exists(images_dir):
        raise Exception("Not exist: {}".format(os.path.abspath(images_dir)))
    else:
        # only search for output of image 1: "*-1-outputs.png"
        fnm_png = "*-" + fnm + "-outputs.png" 
        search_paths = os.path.join(images_dir, fnm_png)
        file_paths = sorted(glob.glob(search_paths))
        if len(file_paths) == 0:
            raise Exception("No files {} found in {}".format(fnm_png, os.path.abspath(images_dir)))
    return file_paths

def main():
    a = get_main_args()
    font = ImageFont.truetype('/Library/Fonts/Arial.ttf', a.font_size)
    images = []
    file_paths = get_png_paths(a.images_dir, fnm=a.fnm)
    for file_path in file_paths:
        step = get_step_num(file_path)
        if step > a.max_steps:
            break
        else:
            if step < 40:
                skip = 5
            elif step >=40 and step < 100:
                skip = 15
            elif step >=100 and step < 200:
                skip = 20
            else:
                skip = 50
            #if step % a.skip_steps == 0:
            if step % skip == 0:
                text = "step {}".format(step)
                image = Image.open(file_path).convert('RGBA')
                if image.size != (a.im_size, a.im_size):
                    image = image.resize((a.im_size, a.im_size), Image.BICUBIC)
                image = add_text_to_image(image, text, font)
                images.append(image)
                print(file_path)
   
    images = np.stack(images)
    imageio.mimsave(os.path.join(a.output_dir, a.fnm_gif), images, duration=a.im_duration)
    print("{} saved in {}".format(a.fnm_gif, os.path.abspath(a.output_dir)))

if __name__ == '__main__':
    main()