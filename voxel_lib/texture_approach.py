import numpy as np
from numba import jit
import subprocess
import os
import PIL.Image

@jit(nopython=True)
def convert_2D_color(gen_2D):
    return_2D_array = np.zeros((gen_2D.shape[0], gen_2D.shape[1], 4))
    for row in range(gen_2D.shape[0]):
        for col in range(gen_2D.shape[1]):
            if np.any(gen_2D[row][col] < 128):
                for idx in range(3):
                    if gen_2D[row][col][idx] > 127:
                        return_2D_array[row][col][idx] = 127 * 2
                    else:
                        return_2D_array[row][col][idx] = gen_2D[row][col][idx] * 2
                return_2D_array[row][col][3] = 255
            else:
                return_2D_array[row][col] = [255,255,255,0]
    return return_2D_array

def minecraft_to_3D(png_array):
    png_array = convert_2D_color(png_array)
    if not os.path.exists('voxel_lib/cache/'):
        os.makedirs('voxel_lib/cache/')
    png_array = np.uint8(png_array)
    png_array = PIL.Image.fromarray(png_array, 'RGBA')
    png_array.save('voxel_lib/cache/tmp.png')
    subprocess.call('php voxel_lib/minecraft_3D.php')
    minecraft_3Dimg = PIL.Image.open('voxel_lib/cache/tmp_gen.png')
    minecraft_3Dimg = np.array(minecraft_3Dimg)
    minecraft_3Dimg = minecraft_3Dimg[:,:,0:3]
    return minecraft_3Dimg
