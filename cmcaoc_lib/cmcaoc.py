"""Cyrille's library of helpful functions for AoC."""

import numpy as np
from PIL import Image

# pip install numpy
# pip install pillow


def matPrint(mat, cwidth=1, replace=0, replacement="."):
    """Print a matrix nicely."""
    nh, nw = mat.shape
    print("Dimension", nh, nw)

    for y in range(nh):
        for x in range(nw):
            vlen = len(str(mat[y, x]))
            if mat[y, x] == replace:
                print(replacement + " " * (cwidth - len(replacement)), end="")
            else:
                print(str(mat[y, x]) + " " * (cwidth - vlen), end="")
        print()


def matWrap(mat, width=1, value=""):
    """Add a border of values around a matrix."""
    h, w = mat.shape

    if mat.dtype == "U1":
        nmat = np.full(np.array(mat.shape) + 2 * width, value)

    vnumeric = ["float64", "int64", np.uint8]
    if mat.dtype in vnumeric:
        if value == "":
            value = 0
        nmat = np.full(np.array(mat.shape) + 2 * width, value, dtype=mat.dtype)

    # copy mat contents to new matrix
    nmat[width : mat.shape[0] + width, width : mat.shape[1] + width] = mat

    return nmat


def makePixelListHw(surf, scale=True, boost=0, res=1):
    """Take numpy matrix and returned populated pixel list."""
    # make the pixel list
    # boost non-zero values to scale
    surf[surf > 0] += boost
    if scale:
        surf = int(255 / surf.max()) * surf

    pixlist = []
    h, w = surf.shape
    for y in range(h):
        for _ in range(res):
            for x in range(w):
                for _ in range(res):
                    pixlist.append((surf[y, x], surf[y, x], surf[y, x]))
    return {"pixlist": pixlist, "h": h * res, "w": w * res}


def makeRgbImage(pixlist, filename, height, width):
    """Save provided data into image."""
    # create image of dimension
    im = Image.new("RGB", (width, height))
    im.putdata(pixlist)
    im.save(filename + ".png")


if __name__ == "__main__":
    print("Use as library, not main module!")
