# A Quick Glance

![work flow of Slice approach](./markdown_image/cube_01.png)

**Use of stylistic GAN in Gaming Applications**<br>
We want to make use of StyleGAN to explore the feasibilities in 3D asset generation. Since StyleGAN only accept 2D images as input, we have to first convert 3D model data into 2D images. We will further explain three different conversion approach and pick the best one below. After training, we will reverse the process to get back the corresponding 3D voxel model result.

## Flatten approach
| 2D images           | its 3D representation |
|:-------------------:| :--------------------:|
| <img src="./markdown_image/flatten_sample.png" alt="drawing" width="256" height="256"/>| <img src="./markdown_image/3D_example.png" alt="drawing" width="256" height="256"/>|


## Texture approach
| 2D images           | its 3D representation |
|:-------------------:| :--------------------:|
|<img src="./markdown_image/texture_2D_sample.png" alt="drawing"/>|<img src="./markdown_image/texture_3D_sample.png" alt="drawing" height="256"/>|
## Slice approach
|       Method          | 2D images           | its 3D representation |
| :---------------------|:-------------------:| :--------------------:|
| Normal                |<img src="./markdown_image/slice_normal_sample.png" alt="drawing" height="256"/>|<img src="./markdown_image/3D_example.png" alt="drawing" height="256"/>|
| Hilbert               |<img src="./markdown_image/slice_Hilbert_sample.png" alt="drawing" height="256"/>|<img src="./markdown_image/3D_example.png" alt="drawing" height="256"/>|
| 3-axis                |<img src="./markdown_image/slice_3-axis_sample.png" alt="drawing" height="256"/>|<img src="./markdown_image/3D_example.png" alt="drawing" height="256"/>|
| Hilbert_with_3-axis   |<img src="./markdown_image/slice_Hilbert_with_3-axis_sample.png" alt="drawing" height="256"/>|<img src="./markdown_image/3D_example.png" alt="drawing" height="256"/>|



# Beginning
Since StyleGAN requires all the input image must be square image and its length of side must be the power of 2 (1024, 512, 256, ...). At the beginning of our project, we just simply flatten the 3D space into 2D images. At that time, we just test whether StyleGAN could recognize this transformation so the input data is monochrome.

In our approach, we set a cutoff for determining whether the voxel exists. For monochrome image, we set the cutoff to be 128, which means only if all the rgb value are lower than 128, then the voxel exists. For the chromatic image, the cutoff would be set to be 192. This would be explained in detail later (color approach).
## Flatten approach
1. Enlarge the 3D model by 3 along x,y,z axis (30, 30, 30, 3) -> (90, 90, 90, 3)
2. Flatten the 3D array (90, 90, 90, 3) -> (729000, 3)
3. In order to reshape the array into 2D image, which its size is 1024*1024, but the flatten array is only (729000, 3), so concatenate size of (319576, 3) white pixel [255, 255, 255] to the flatten array and make it to be (729000 + 319576, 3) -> (1048576, 3) -> (1024, 1024, 3)

This is how the input data created. 

## Result
<span style="color:red">Will be updated in the up comming version</span>

The result is not satisfying. Only proved that a cuboid-like model can be learned by StyleGAN.

# Improvement

Since we want to increase the fault tolerance, single line or pixels presented after the conversion into 2D image should be avoided. Therefore, new approach is implemented which scale the image after flattening so that no more single line presented.

## New flatten approach

1. Flatten the 3D array (40, 40, 40, 3) -> (64000, 3)
2. Concatenate size of (1536, 3) white pixel to flatten array (64000 + 1536, 3) -> (65536, 3)
3. Reshape the array to be 2D image with size 256 * 256 (65536, 3) -> (256, 256, 3)
4. Scale the image along width and height by 4. (256, 256, 3) -> (1024, 1024, 3)

## Assumption behind

1. Each voxel now is represented as a 4 * 4 area of pixels, even if some pixels go wrong, the result could still be satisfying since interpolation was applied to calculate the average rgb value of the voxel
2. This approach is conducive to recognize the image. As the convolution network is full of 3 * 3 filter, the rgb value in all the possible 3 * 3 grid would not change rapidly.

## Result

<span style="color:red">Will be updated in the up comming version</span>

Most of the results are satisfying. However some results need to be re-train several times to make it to be acceptable. We guess the network sometimes still rely on some random varibles, especially when the input dataset is mixed with different axis and color.

# StyleGAN2 launched
According to [StyleGAN2 repository](https://github.com/NVlabs/stylegan2), they had revisited different features, including progressive growing, removing normalization artifacts, etc. As the result, This revised StyleGAN benefits our 3D model training. The incoming results were trained by StyleGAN2.  

Since we had proved that StyleGAN2 is capable to recongnize color and shape in our approach. We further extend the possible 3D space from (40, 40, 40, 3) to (64, 64, 64 ,3) and it can be reshaped as a 512 * 512 image, noted that 64 * 64 * 64 = 512 * 512. Therefore, no more white pixels are needed in the flatten array. All the pixels in 2D image could be fully utilized.

# Flatten approach in StyleGAN2
This time we would 512 * 512 image as our shape of input images becausae it helps reduce the training time. Surprisingly, the network still can recognize the input dataset but just only for the one contains less variations.

## Approach
1. Flatten the 3D array (64, 64, 64, 3) -> (262144, 3)
2. Reshape the array to be 2D image with size 512 * 512 (262144, 3) -> (512, 512, 3)

## results (bookcase) Variation: Shelfboard
| 2D images           | its 3D representation |
|:-------------------:| :--------------------:|
|<img src="./markdown_image/bookcase_shelfboard_sample1.png" height="256"/>|<img src="./markdown_image/bookcase_shelfboard_sample1_3D.png" height="256"/>|
|<img src="./markdown_image/bookcase_shelfboard_sample2.png" height="256"/>|<img src="./markdown_image/bookcase_shelfboard_sample2_3D.png" height="256"/>|
|<img src="./markdown_image/bookcase_shelfboard_sample3.png" height="256"/>|<img src="./markdown_image/bookcase_shelfboard_sample3_3D.png" height="256"/>|
|<img src="./markdown_image/bookcase_shelfboard_sample4.png" height="256"/>|<img src="./markdown_image/bookcase_shelfboard_sample4_3D.png" height="256"/>|

## results (table)  Variation: Style
| 2D images           | its 3D representation |
|:-------------------:| :--------------------:|
|<img src="./markdown_image/flatten_table_sample1.png" height="256"/>|<img src="./markdown_image/flatten_table_sample1_3D.png" height="256"/>|
|<img src="./markdown_image/flatten_table_sample2.png" height="256"/>|<img src="./markdown_image/flatten_table_sample2_3D.png" height="256"/>|
|<img src="./markdown_image/flatten_table_sample3.png" height="256"/>|<img src="./markdown_image/flatten_table_sample3_3D.png" height="256"/>|
|<img src="./markdown_image/flatten_table_sample4.png" height="256"/>|<img src="./markdown_image/flatten_table_sample4_3D.png" height="256"/>|

As the result, the StyleGAN seems that it cannot recognize the shape of the table in flatten approach.
On the other hand, we were developing texture approach meanwhile.
# Texture approach
In this approach, we choose texture as our input dataset. We choose Minecraft human texture as our input dataset since it is relatively low resolution and contains tons of resources on the internet thanks to the community.

## results 
### generator
![](./markdown_image/texture_sample.png)
### style mixing
| Coarse style           | Fine style |
|:-------------------:| :--------------------:|
|<img src="./markdown_image/texture_coarse.png"/>|<img src="./markdown_image/texture_fine.png"/>|


# Slice approach
As we want to take the advantages of powerful recognizing 2D images features ability in StyleGAN2. We choose to revise the representation of 3D model to be slice approach.

## Approach
1. Slice the 3D model along x/y/z axis. Slicing along which axis depends on the input dataset. (64, 64, 64, 3) -> (64, 64, 3, 64)
2. Paste those sliced images to a 512 * 512 image. (64, 64, 3, 64) -> (512, 512, 3)

## Asumption behind
1. If those 2D images which converted from 3D models, they share more similiar area by slicing along one specific axis, then that axis would be more appropriate as our choice since this is good for the network to recognize our input dataset.

## results 
| 2D images           | its 3D representation |
|:-------------------:| :--------------------:|
|<img src="./markdown_image/normal_sample1.png" height="256"/>|<img src="./markdown_image/normal_sample1_3D.png" height="256"/>|
|<img src="./markdown_image/normal_sample2.png" height="256"/>|<img src="./markdown_image/normal_sample2_3D.png" height="256"/>|
|<img src="./markdown_image/normal_sample3.png" height="256"/>|<img src="./markdown_image/normal_sample3_3D.png" height="256"/>|
|<img src="./markdown_image/normal_sample4.png" height="256"/>|<img src="./markdown_image/normal_sample4_3D.png" height="256"/>|

# Improvement of slice approach

![stylegan synthesis network](./markdown_image/stylegan%20synthesis%20network.png)  
Source: [StyleGAN2 paper](https://arxiv.org/pdf/1912.04958.pdf)  

From the network structure, we can find that the synthesis network make a image from low resolution to high resolution. If we could arrange the slice in this approach:  
![Hilbert's curve](./markdown_image/Hilbert's%20curve.png)  
Source: [DateGenetics](http://datagenetics.com/blog/march22013/)
Then the relationship of the slice could be strengthened and this helps synthesis process.

4 x 4 :  
![4x4convert](./markdown_image/cube_02.png)

At least in every 4 or 8 adjacent slice could be segmented as the same 8 x 8 or 4 x 4 grid respectively. We assume that it is good for the network, especially increasing the ability of style-mixing.

## Slice approach with Hilbert's curve

1. Slice the 3D model along x/y/z axis as usual. Slicing along which axis depends on the input dataset.
2. Place the slices of 3D model as the arranged order mentioned before.
3. Every slice size is (64, 64, 3) so there will be 8 slices in every row of the final image (512, 512, 3).

### results 
| 2D images           | its 3D representation |
|:-------------------:| :--------------------:|
|<img src="./markdown_image/Hilbert_table1.png" height="256"/>|<img src="./markdown_image/Hilbert_table1_3D.png" height="256"/>|
|<img src="./markdown_image/Hilbert_table2.png" height="256"/>|<img src="./markdown_image/Hilbert_table2_3D.png" height="256"/>|
|<img src="./markdown_image/Hilbert_table3.png" height="256"/>|<img src="./markdown_image/Hilbert_table3_3D.png" height="256"/>|
|<img src="./markdown_image/Hilbert_table4.png" height="256"/>|<img src="./markdown_image/Hilbert_table4_3D.png" height="256"/>|

Suprisingly, the training time has reduced after using this approach and it is quite hard to prove that the style-mixing ability has been increased. We would try to measure this in the upcomming version.

## Slice approach with 3 dimension

1. Slice the 3D model along x, y and z axis, place the slices of 3D model as the order of Hilbert's curve.
2. Then we will get 3 images with size (512, 512, 3).
3. In a (1024, 1024, 3) image, we can place 4 (512, 512, 3) images at 4 corners as the x one is placed at the top left corner, y is placed at the left bottom corner, z is placed at the top right corner and the last corner will be remained as blank white color.

### results 
| 2D images           | its 3D representation |
|:-------------------:| :--------------------:|
|<img src="./markdown_image/3-axis_sample1.png" height="256"/>|<img src="./markdown_image/3-axis_sample1_3D.png" height="256"/>|
|<img src="./markdown_image/3-axis_sample2.png" height="256"/>|<img src="./markdown_image/3-axis_sample2_3D.png" height="256"/>|
|<img src="./markdown_image/3-axis_sample3.png" height="256"/>|<img src="./markdown_image/3-axis_sample3_3D.png" height="256"/>|
|<img src="./markdown_image/3-axis_sample4.png" height="256"/>|<img src="./markdown_image/3-axis_sample4_3D.png" height="256"/>|  

# More results of slice approach with Hilbert's curve

## 3D texture
As the styleGAN cannot recognized the 3D model with different textures added, such as wooden or rock texture. We guess maybe there is not enough hidden layers that are responsible for finer details in 512 x 512 level. Therefore, we change the texture into simple striped texture with different colors.

## chair
| 2D images           | its 3D representation |
|:-------------------:| :--------------------:|
|<img src="./markdown_image/Hilbert_chair1.png" height="256"/>|<img src="./markdown_image/Hilbert_chair1_3D.png" height="256"/>|
|<img src="./markdown_image/Hilbert_chair2.png" height="256"/>|<img src="./markdown_image/Hilbert_chair2_3D.png" height="256"/>|
|<img src="./markdown_image/Hilbert_chair3.png" height="256"/>|<img src="./markdown_image/Hilbert_chair3_3D.png" height="256"/>|
|<img src="./markdown_image/Hilbert_chair4.png" height="256"/>|<img src="./markdown_image/Hilbert_chair4_3D.png" height="256"/>|

# pkl file download
(OneDrive link)[https://mycuhk-my.sharepoint.com/:u:/g/personal/1155095136_link_cuhk_edu_hk/ERLYZY_BhIlEmG2NLEVsjPcBHuVw6d5RB24b7U2ubozWpw?e=oc4pEr]

# Example for How to use the program

## For Generator:
```bash
python run_generator.py generate-images --network=pkl_folder/Normal_table.pkl --seeds=6600-6900 --truncation-psi=0.7 --mode=normal --color=False
```
## For truncation change:
```bash
python run_generator.py truncation-trick --network=pkl_folder/Hilbert_stripe.pkl --seeds=270 --interval=0.1 --mode=Hilbert --color=True
```
## For Style mixing:
```bash
python run_generator.py style-mixing-example --network=pkl_folder/Hilbert_stripe.pkl --row-seeds=270,147 --col-seeds=68,79,75 --truncation-psi=0.7 --col-styles=1,2,3,4 --mode=Hilbert --color=True
```

For more example, please read caller.py.  
If you want to create you own dataset, you may use the code in this folder: "dataset_3D_maker"  
Please feel free to let me know if you have encountered any problems via gmail(adamandworking@gmail.com). Enjoy!