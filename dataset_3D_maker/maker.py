import numpy as np
import PIL.Image
# binvox to image(flatten, slice + different method)

# 3D array to image(flatten, slice + different method)

# raw_minecraft to dataset_minecraft

# z_up method?

# resize 3D array method?

from tool import binvox_to_nparray

def binvox_to_png(mode, path_binvox, axis = 'z'):
    mapping_Hilbert = np.array([
        [1 ,2 ,15,16,17,20,21,22],
        [4 ,3 ,14,13,18,19,24,23],
        [5 ,8 ,9 ,12,31,30,25,26],
        [6 ,7 ,10,11,32,29,28,27],
        [59,58,55,54,33,36,37,38],
        [60,57,56,53,34,35,40,39],
        [61,62,51,52,47,46,41,42],
        [64,63,50,49,48,45,44,43],
    ])
    nparray = binvox_to_nparray(path_binvox)
    assert nparray.shape == (64, 64, 64), 'The dimension must be (64, 64, 64)'
    assert mode in ['flatten','normal', 'Hilbert', '3-axis', 'Hilbert_with_3-axis'], 'Invalid mode'
    
    array_2D = np.zeros((512, 512, 3))
    if mode == 'flatten':
        data_flatten_array = nparray.flatten()
        png_flatten_array = np.zeros((64 * 64 * 64, 3))
        for idx, element in enumerate(data_flatten_array):
            if element == True:
                png_flatten_array[idx] = [0, 0, 0]
            else:
                png_flatten_array[idx] = [255, 255, 255]
        array_2D = png_flatten_array.reshape((512, 512 , 3))

    if mode in ['normal', 'Hilbert']:
        count = 0
        for level in reversed(range(64)):
            if mode == 'normal':
                row_index = count//8
                col_index = count - row_index * 8
            if mode == 'Hilbert':
                row_index, col_index = np.where(mapping_Hilbert == count + 1)
                row_index, col_index = row_index[0], col_index[0]
            current_grid = nparray[:,:,level]
            for x in range(64):
                for y in range(64):
                    if current_grid[x][y] == True:
                        array_2D[row_index * 64 + x][col_index * 64 + y] = [0, 0, 0]
                    else:
                        array_2D[row_index * 64 + x][col_index * 64 + y] = [255, 255, 255]
            count += 1

    if mode in ['3-axis', 'Hilbert_with_3-axis']:
        array_2D = np.zeros((1024, 1024, 3))
        array_2D += 255
        count = 0
        for level in reversed(range(64)):
            if mode == '3-axis':
                row_index = count // 8
                col_index = count - row_index * 8
            if mode == 'Hilbert_with_3-axis':
                row_index, col_index = np.where(mapping_Hilbert == count + 1)
                row_index, col_index = row_index[0], col_index[0]
            x_current_grid = nparray[level,:,:]
            y_current_grid = nparray[:,level,:]
            z_current_grid = nparray[:,:,level]
            for x in range(64):
                for y in range(64):
                    array_2D[row_index * 64 + x][col_index * 64 + y] = [0, 0, 0] if x_current_grid[x][y] else [255, 255, 255]
                    array_2D[512 + row_index * 64 + x][col_index * 64 + y] = [0, 0, 0] if y_current_grid[x][y] else [255, 255, 255]
                    array_2D[row_index * 64 + x][512 + col_index * 64 + y] = [0, 0, 0] if z_current_grid[x][y] else [255, 255, 255]
            count += 1
    array_2D = np.uint8(array_2D)
    png = PIL.Image.fromarray(array_2D)
    png.save('OUTPUT/test.png')

if __name__ == '__main__':
    binvox_to_png('Hilbert_with_3-axis','INPUT/test.binvox')
    