from util import to_color_3Dimage, to_monochrome_image, png_to_numpy
from voxel_lib.slice_approach import slice_to_3D 
from voxel_lib.texture_approach import minecraft_to_3D 
from voxel_lib.flatten_approach import flatten_to_3D 
import PIL.Image
import glob
import os

def slice_convert_2D_to_3D():
    input_list = glob.glob('INPUT/*.png') 
    for file in input_list:
        basename = os.path.basename(file)
        numpy_png = png_to_numpy(file)
        boolean_table, rgb_3Darray = slice_to_3D('normal', numpy_png, False)

        color_image3D = to_color_3Dimage(boolean_table, rgb_3Darray)
        color_image3D = PIL.Image.fromarray(color_image3D)
        color_image3D.save('OUTPUT/color_' + basename)

        monochrome_image3D = to_monochrome_image(boolean_table)
        monochrome_image3D = PIL.Image.fromarray(monochrome_image3D)
        monochrome_image3D.save('OUTPUT/mono_chrome_' + basename)
 
def minecraft_convert_2D_to_3D():
    input_list = glob.glob('INPUT/*.png')
    for file in input_list:
        basename = os.path.basename(file)
        numpy_png = png_to_numpy(file)
        image3D = minecraft_to_3D(numpy_png)
        image3D = PIL.Image.fromarray(image3D)
        image3D.save('OUTPUT/minecraft_' + basename)

def single_image_converter(numpy_png, mode, color):
    if mode in ['flatten','normal', 'Hilbert', '3-axis', 'Hilbert_with_3-axis']:
        if mode in ['flatten']:
            boolean_table, rgb_3Darray = flatten_to_3D(numpy_png, color)
        if mode in ['normal', 'Hilbert', '3-axis', 'Hilbert_with_3-axis']:
            boolean_table, rgb_3Darray = slice_to_3D(mode, numpy_png, color)
        color_image3D = to_color_3Dimage(boolean_table, rgb_3Darray)
        monochrome_image3D = to_monochrome_image(boolean_table)
    if mode in ['texture']:
        color_image3D = minecraft_to_3D(numpy_png)
        monochrome_image3D = None
    return color_image3D, monochrome_image3D



if __name__ == '__main__':
    # slice_convert_2D_to_3D()
    # minecraft_convert_2D_to_3D()
    print('program end')
