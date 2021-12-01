import os
from PIL import Image
import glob

datadir = "imgs/"
animgif = "tiles_anim.gif"

img, *imgs = [Image.open(f) for f in sorted(glob.glob("imgs/hextiles_*.png"))]
img.save(fp=animgif, format='GIF', append_images=imgs, save_all=True, duration=40, loop=0)
