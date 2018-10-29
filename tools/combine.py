from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import argparse
import os
from PIL import Image

"""
python tools/combine.py --size 572 --a_dir photos/color --b_dir photos/line --c_dir photos
"""  


parser = argparse.ArgumentParser()
parser.add_argument("--a_dir", type=str, default='photos/color', help="folder of A images")
parser.add_argument("--b_dir", type=str, default='photos/line', help="folder of B images")
parser.add_argument("--c_dir", type=str, default='photos', help="folder of output (combined) images")
parser.add_argument("--size", type=int, default=256, help="size to use for resize operation")
a = parser.parse_args()


def load_and_resize(src_path, size):
    """
    load an image and resize to a square image
    INPUT
    -------
    src: an PIL Image
    size: an integer, size of the square image
    """
    
    if os.path.exists(src_path):
        src = Image.open(src_path).convert('RGB')
    else:
        raise Exception("could not find image {}".format(src_path))

    src = Image.open(src_path).convert('RGB')

    height, width = src.size
    if min(height, width) < size:
        # raise Exception("input image is smaller than {}".format(size))
        print("Warning: {} is smaller than {}".format(src_path, size))
    # resize and make square
    dst = src.resize((size, size), Image.BICUBIC)
    assert(dst.size[0] == dst.size[1])
    return dst


def combine(imA, imB):
    """
    create a new image by combining A and B horizontally
    INPUT
    ------
    imA: a PIL Image
    imB: a PIL Image
    OUTPUT
    -------
    imC: a PIL Image, A-B image
    """
    # check image sizes
    if imA.size != imB.size:
        raise Exception("cannot combine two images with different sizes")
    
    height, width = imA.size
    total_width = width * 2
    imC = Image.new('RGB', (total_width, height))
    x_offset = 0
    for im in [imA, imB]:
        imC.paste(im, (x_offset, 0))
        x_offset += im.size[1]
    return imC


def main():
        
    # A folder and B folder must exist
    if a.a_dir is None:
        raise Exception("missing a_dir")
    if a.b_dir is None:
        raise Exception("missing b_dir")
        
    # create C folder if not exist
    if not os.path.exists(a.c_dir):
        os.makedirs(a.c_dir)

    for fname_ext in os.listdir(a.a_dir):
        # fname_ext: same for A, B, and combined, e.g., "1.png"
        A_path = os.path.join(a.a_dir, fname_ext) # e.g., "photos/color/1.png"
        B_path = os.path.join(a.b_dir, fname_ext) # e.g., "photos/line/1.png"
        C_path = os.path.join(a.c_dir, fname_ext) # e.g., "photos/1.png"

        # A image 
        imA = load_and_resize(A_path, a.size)
        # B image 
        imB = load_and_resize(B_path, a.size)
        # combined image
        # imC = combine(imA, imB)
        imC = combine(imB, imA)
        imC.save(C_path)
        
        # for testing (and presentation slides)
        # save images of size 512        
        imA = load_and_resize(A_path, 512)
        imA.save(os.path.join(a.c_dir, "c"+fname_ext))
        # save line images of size 512 
        imB = load_and_resize(B_path, 512)
        imB.save(os.path.join(a.c_dir, "l"+fname_ext))


main()
