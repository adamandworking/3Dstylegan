import numpy as np
from numba import jit
from util import convert_3D_color, to_color_3Dimage

@jit(nopython=True)
def flatten_to_3D(png_array, color):
    boolean_table = np.zeros((64,64,64))
    cutoff = 192 if color else 128
    flatten_array = png_array.flatten()
    rgb_3Darray = flatten_array.reshape((64,64,64,3))

    for x in range(64):
        for y in range(64):
            for z in range(64):
                if np.any(rgb_3Darray[x][y][z] < cutoff):
                    boolean_table[x][y][z] = True

    if color:
        convert_3D_color(rgb_3Darray)

    return boolean_table, rgb_3Darray 