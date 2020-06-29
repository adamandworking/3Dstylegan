import numpy as np
from numba import jit
from util import convert_3D_color, to_color_3Dimage

@jit(nopython=True)
def slice_to_3D(mode, png_array, color, axis = 'z'):
    cutoff = 192 if color else 128
    Hilbert_mapping = [
    [1 ,2 ,15,16,17,20,21,22],
    [4 ,3 ,14,13,18,19,24,23],
    [5 ,8 ,9 ,12,31,30,25,26],
    [6 ,7 ,10,11,32,29,28,27],
    [59,58,55,54,33,36,37,38],
    [60,57,56,53,34,35,40,39],
    [61,62,51,52,47,46,41,42],
    [64,63,50,49,48,45,44,43],
]
    if mode in ['normal', 'Hilbert', '3-axis', 'Hilbert_with_3-axis']:
        boolean_table = np.zeros((64, 64, 64))
        rgb_3Darray = np.zeros((64, 64, 64, 3))
    if mode in ['3-axis', 'Hilbert_with_3-axis']:
        x_axis_png = np.zeros((512, 512))
        y_axis_png = np.zeros((512, 512))
        z_axis_png = np.zeros((512, 512))
        x_axis_rgb_3Darray = np.zeros((64, 64, 64, 3))
        y_axis_rgb_3Darray = np.zeros((64, 64, 64, 3))
        z_axis_rgb_3Darray = np.zeros((64, 64, 64, 3))
    if mode in ['normal', 'Hilbert']:
        for i in range(8):
            for j in range(8):
                for a in range(64):
                    for b in range(64):
                        if mode == 'normal':
                            layer_num = (7 - i) * 8 + (7 - j)
                        if mode == 'Hilbert':
                            layer_num = 64 - Hilbert_mapping[i][j]
                        if np.all(png_array[i * 64 + a][j * 64 + b] < cutoff):
                            if axis == 'x':
                                boolean_table[layer_num][a][b] = True
                                rgb_3Darray[layer_num][a][b] = png_array[i * 64 + a][j * 64 + b]
                            if axis == 'y':
                                boolean_table[a][layer_num][b] = True
                                rgb_3Darray[a][layer_num][b] = png_array[i * 64 + a][j * 64 + b]
                            if axis == 'z':
                                boolean_table[a][b][layer_num] = True
                                rgb_3Darray[a][b][layer_num] = png_array[i * 64 + a][j * 64 + b]      
    if mode in ['3-axis', 'Hilbert_with_3-axis']:
        x_axis_png = png_array[0:512, 0:512]
        y_axis_png = png_array[512:1024, 0:512]
        z_axis_png = png_array[0:512, 512:1024]
        for i in range(8):
            for j in range(8):
                if mode == '3-axis':
                    layer_num = (7 - i) * 8 + (7 - j)
                if mode == 'Hilbert_with_3-axis':
                    layer_num = 64 - Hilbert_mapping[i][j]
                x_axis_rgb_3Darray[layer_num,:,:] =  x_axis_png[i * 64 : (i + 1) * 64 , j * 64 : (j + 1) * 64]
                y_axis_rgb_3Darray[:,layer_num,:] =  y_axis_png[i * 64 : (i + 1) * 64 , j * 64 : (j + 1) * 64]
                z_axis_rgb_3Darray[:,:,layer_num] =  z_axis_png[i * 64 : (i + 1) * 64 , j * 64 : (j + 1) * 64]
        for i in range(64):
            for j in range(64):
                for k in range(64):
                    k = 64 - k
                    result = np.array([np.any(x_axis_rgb_3Darray[i][j][k] < cutoff), np.any(y_axis_rgb_3Darray[i][j][k] < cutoff), np.any(z_axis_rgb_3Darray[i][j][k] < cutoff)])
                    if axis_judgement(result):
                        boolean_table[i][j][k] = True
                        rgb_3Darray[i][j][k] = (x_axis_rgb_3Darray[i][j][k] + y_axis_rgb_3Darray[i][j][k] + z_axis_rgb_3Darray[i][j][k]) / 3
    if color:
        convert_3D_color(rgb_3Darray)
    return boolean_table, rgb_3Darray

@jit(nopython=True)
def axis_judgement(xyz_result, choice = 1):
    if(choice == 0):
        return np.any(xyz_result)
    elif(choice == 1):
        if(np.count_nonzero(xyz_result) >= 2):
            return True
        else:
            return False
    elif(choice == 2):
        return np.all(xyz_result)

