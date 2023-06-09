# Images Acquisition With Intel RealSense

This project involves using Intel Realsense to capture RGB images, depth images, pseudo colored depth images and depth data saved in .npy format, and can be applied to create custom datasets for algorithms such as object detection, instance segmentation, semantic segmentation and so on.

If you want to make a custom dataset from YOLO, please refer to the link [YOLO-Datasets-And-Training-Methods](https://github.com/Incalos/YOLO-Datasets-And-Training-Methods) for details.

To read RGB images and depth images in a similar way to the **pyrealsnese2** library, this project provides the corresponding interface **Dataloader.py**.

To batch modify the file name of the collected data, you can use **Rename.py**.

## Images Acquisition

### (1) Operation Steps

* Connect the Intel RealSense to the computer.

* Enter the following command in the terminal and run **RealsenseColorImage.py**. Please browse back for the meaning of the specific parameters.

   ```shell
   python RealsenseColorImage.py --image_format 0 --mode 0 --image_width 640 --image_height 480 --fps 30
   ```

* If the **mode** is set to 0, it is in automatic saving mode. To start, please use the English input method to click the **_S_** key of the keyboard, and to pause halfway, click the **_W_** key of the keyboard.

* If the **mode** is set to 1, it is in manual save mode. If there are any images displayed that you want to save, please click on the keyboard using the English input method **_S_** Key to save.

* If you want to end the program, hit the **_Q_** on your keyboard with the English input method.

### (2) Parameter Description In The Command

* **path** : `the root directory where all images are saved. If this parameter is an empty string, the collected images are saved in the current directory and the folder is named at local time. If not, it is saved in the provided path. Adding backward is supported if there are previously saved data in the provided path.`
* **mode** : `save mode. 0 means auto-save, 1 means manual save.`
* **image_format** : `image saving format. 0 represents .JPG, 1 represents .PNG.`
* **image_width** : `the width of the image, recommended to use 1280 or 640`
* **image_height** : `the height of the image, recommended to use 720 or 480`
* **fps** : `frame per second`

### (3) Running Results

After the program runs, three types of images saved will show in the following structure.

```
Year_Month_Day_Hour_Minute_Second/
   |——————DepthColorImages/
   |        └——————1.jpg
   |        └——————2.jpg  
   |        └——————3.jpg
   |        └——————...
   |——————DepthImages/
   |        └——————1.jpg
   |        └——————2.jpg 
   |        └——————3.jpg
   |        └——————...
   |——————DepthNpy/
   |        └——————1.npy
   |        └——————2.npy 
   |        └——————3.npy
   |        └——————...
   |——————images/
   |        └——————1.jpg
   |        └——————2.jpg  
   |        └——————3.jpg
   |        └——————...
   └——————intrinsics.json
```

* **Year_Month_Day_Hour_Minute_Second** : `the root directory where images are saved and the folder is named using local time`
* **DepthColorImages** : `the save path of pseudo-colorized depth images`
* **DepthImages** : `the save path of depth images`
* **DepthNpy** : `the save path of depth data and the format is numpy-specific binary files`
* **images** : `the save path of RGB images`
* **intrinsics.json** : `camera parameters of Intel RealSense`

## 2. Data Reading ( Dataloader.py )

**Dataloader.py** is used for data reading, the result is the same as **pyrealsense2**, the following is a use example.

```python
from Dataloader import LoadImages

path = '2023_03_28_20_14_30'
dataset = LoadImages(path)
for data in dataset:
  color_image, depthimage, inintrinsics = data
  fx, fy, ppx, ppy = inintrinsics.fx, inintrinsics.fy, inintrinsics.ppx, inintrinsics.ppy
```

The input parameter **path** is the name of the root directory of the dataset generated by **RealsenseColorImage.py**. 

The return values include the RGB image, the depth image, and the camera parameters.

## 3. File Name Batch Modification ( Rename.py )

Open the terminal and enter the following command. For the parameters **annotations**, the dataset is required to contain label files, which is visible in the link [YOLO-Datasets-And-Training-Methods](https://github.com/Incalos/YOLO-Datasets-And-Training-Methods).

```shell
python Rename.py --path 2023_03_28_20_14_30 --firstnum 1 --image_format 0 --annotations False
```

* **path** : `the root directory of the dataset to be modified`
* **firstnum** : `modify the first filename to the name you want, all of which are named by numbers`
* **image_format** : `format of the image in the dataset, 0 means .jpg format, 1 means .png format`
* **annotations** : `whether to modify the label files`
