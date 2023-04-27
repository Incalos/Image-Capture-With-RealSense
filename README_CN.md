# Intel RealSense 采图程序

本项目主要关于使用 **Intel RealSense** 相机采集RGB图像、深度图像、伪彩色化的深度图像以及.npy格式保存的深度数据。

采集到的图像可适用于制作目标检测、实例分割、语义分割等算法的自定义数据集。其中，目标检测YOLO算法的自定义数据集制作具体可参考 [YOLO-Datasets-And-Training-Methods](https://github.com/Incalos/YOLO-Datasets-And-Training-Methods)。

若要以类似于 **pyrealsnese2** 库的方式读取RGB图像以及深度图像，本项目提供了相应的接口 **Dataloader.py**。

若要进行对采集到的数据批量修改文件名，可以使用 **Rename.py**。

## 1. 采图 ( RealsenseColorImage.py )

### (1) 操作步骤

* 将RealSense相机通过数据线连接到电脑上。

* 打开终端，在终端里输入以下命令，运行 **RealsenseColorImage.py**。具体参数含义请向后浏览。

   ```shell
   python RealsenseColorImage.py --image_format 0 --mode 0 --image_width 640 --image_height 480 --fps 30
   ```

* 如果设置了 **mode** 为0，则为自动保存模式。若要开始，请使用英文输入法点击键盘的 **_S_** 键，若要中途暂停，则点击键盘的 **_W_** 键。

* 如果设置了 **mode** 为1，则为手动保存模式。如果实时展示的图片中有想要保存的，请使用英文输入法点击键盘的 **_S_** 键保存。 

* 如果想要结束程序的运行，请使用英文输入法点击键盘的 **_Q_** 键结束程序。

### (2) 命令行中的参数说明

* **path** : `所有图片保存的根目录，如果此参数为空字符串，则将采集到的图片保存在当前目录下，以本地时间命名文件夹。若不为空，则在提供的路径内保存。如果提供的路径内已经有了之前保存的数据，则支持向后添加。`
* **mode** : `拍照模式，0表示自动保存，1表示手动保存`
* **image_format** : `图片保存的格式，0表示保存为.jpg格式，1表示保存为.png格式`
* **image_width** : `图片的宽度，此处建议选择像素大小为1280或者640`
* **image_height** : `图片的高度，此处建议选择像素大小为720或者480`
* **fps** : `相机拍摄的帧率`

### (3) 结果保存格式

在程序运行结束后，不同的图片将会保存在以下的目录结构中。

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

* **Year_Month_Day_Hour_Minute_Second** : `结果保存的根目录文件夹，使用本地时间命名`
* **DepthColorImages** : `伪彩色化深度图像的保存位置`
* **DepthImages** : `深度图像的保存位置`
* **DepthNpy** : `以.npy格式保存的深度数据`
* **images** : `RGB图像的保存位置`
* **intrinsics.json** : `当前状态下获取到的相机的参数`

## 2. 数据读取 ( Dataloader.py )

**Dataloader.py** 用于数据读取，读取结果与 **pyrealsense2** 一致，使用示例如下。

```python
from Dataloader import LoadImages

path = '2023_03_28_20_14_30'
dataset = LoadImages(path)
for data in dataset:
  color_image, depthimage, inintrinsics = data
  fx, fy, ppx, ppy = inintrinsics.fx, inintrinsics.fy, inintrinsics.ppx, inintrinsics.ppy
```

其中传递的参数 **path** 为 **RealsenseColorImage.py** 生成的数据集根目录名。

返回值包括RGB图像、深度图像以及相机参数。

## 3. 文件名批量修改 ( Rename.py )

打开终端，输入以下命令。对于其中的参数 **annotations** 要求数据集中包含有标签文件，详细可见链接 [YOLO-Datasets-And-Training-Methods](https://github.com/Incalos/YOLO-Datasets-And-Training-Methods)。

```shell
python Rename.py --path 2023_03_28_20_14_30 --firstnum 1 --image_format 0 --annotations False
```

* **path** : `要修改的数据集的根目录名`
* **firstnum** : `第一个文件名要修改成的名称，这里全部以数字命名`
* **image_format** : `数据集中图片的格式，0表示.jpg格式，1表示.png格式`
* **annotations** : `是否修改标注好的标签文件`