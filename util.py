import PIL.Image
import numpy as np
from pyface.api import GUI
from mayavi import mlab
from numba import jit

def png_to_numpy(png_path):
    png = PIL.Image.open(png_path)
    png_numpy = np.array(png)
    return png_numpy

def to_color_3Dimage(boolean_table, rgb_3Darray, space=64):
    fig = mlab.figure(1, size=(512, 555))
    xx, yy, zz = np.where(boolean_table == 1)
    s = np.arange(len(xx))
    lut = np.zeros((len(xx), 4))
    for row in s:
        temp = np.append((rgb_3Darray[xx[row]][yy[row]][zz[row]]), 255)
        lut[row, :] = temp
    currfig = mlab.points3d(xx, yy, zz, s,
                            scale_mode='none',
                            mode="cube",
                            scale_factor=1)
    currfig.module_manager.scalar_lut_manager.lut.number_of_colors = len(s)
    currfig.module_manager.scalar_lut_manager.lut.table = lut

    mlab.view(azimuth=315, elevation=65, distance=140, focalpoint=(space/2, space/2, space/2))
    fig.scene.camera.parallel_projection = True
    fig.scene.camera.parallel_scale = 65  # smaller the number, greater zoom
    mlab.axes(figure=fig, nb_labels=5, extent=(0, space, 0, space, 0, space))
    mlab.outline(extent=(0, space, 0, space, 0, space))

    GUI().process_events()
    imgmap_RGB = mlab.screenshot(figure=fig, mode='rgb', antialiased=True)
    img_RGB = np.uint8(imgmap_RGB)
    # img_RGB = PIL.Image.fromarray(img_RGB)
    mlab.clf()
    return img_RGB

def to_monochrome_image(boolean_table, space=64):
    xx, yy, zz = np.where(boolean_table == 1)
    fig = mlab.figure(1, size=(512, 555))
    mlab.points3d(xx, yy, zz,
                    scale_mode='none',
                    color=(0, 1, 0),
                    mode="cube",
                    scale_factor=1)
    mlab.view(azimuth=315, elevation=65, distance=140, focalpoint=(space/2, space/2, space/2))
    fig.scene.camera.parallel_projection = True
    fig.scene.camera.parallel_scale = 65
    mlab.axes(figure=fig, nb_labels=5, extent=(0, space, 0, space, 0, space))
    mlab.outline(extent=(0, space, 0, space, 0, space))
    GUI().process_events()
    imgmap_RGB = mlab.screenshot(figure=fig, mode='rgb', antialiased=True)
    img_RGB = np.uint8(imgmap_RGB)
    # img_RGB = PIL.Image.fromarray(img_RGB)
    mlab.clf()
    return img_RGB

@jit(nopython=True)
def convert_3D_color(rgb_3Darray, mode='normalization'):
    if mode == 'normalization':
        max_value = np.amax(rgb_3Darray)
        for x in range(64):
            for y in range(64):
                for z in range(64):
                    for idx, element in enumerate(rgb_3Darray[x][y][z]):
                        rgb_3Darray[x][y][z][idx] = int(element / max_value  * 255)            

    if mode == 'cut_to_128':
        for x in range(64):
            for y in range(64):
                for z in range(64):
                    for idx, element in enumerate(rgb_3Darray[x][y][z]):
                        if element > 127:
                            rgb_3Darray[x][y][z][idx] = 127
                        rgb_3Darray[x][y][z][idx] *= 2
    return rgb_3Darray
    