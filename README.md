# guone 
**guone** 是一个简单的基于 flask 开发的户外建筑自动识别 web 系统，支持图像分类和实时目标检测两种模式。

## 下载
使用命令：
<br>
```sh
git clone https://github.com/acthse/guone.git you_path
```

然后：
<br>
```sh
git submodule init
git submodule update
```

或者使用 `--recursive` 也阔以：<br>
```sh
git clone --recursive https://github.com/acthse/guone.git you_path
```

## 启动
下载完成后，进入 guone 构建项目：<br>
```sh
cd guone/
buildout
```

如果你没有安装 `buildout` 可使用 `pip` 安装：<br>
```sh
pip install zc.buildout
```

构建完成后，本地 debug 模式下启动 guone:
```sh
./runguone.sh debug   # 注意单词区分大小写
```
或者
```sh
./bin/guone
```
正式生产环境启动：
```sh
./runguone.sh
```
gunicorn 的配置在 gun.conf 中，可根据需求更改。

<br>
成功启动项目后，可看到如下信息：<br>

> [2018-06-07 19:33:02 +0800] [9928] [INFO] Starting gunicorn 19.8.1<br>
> [2018-06-07 19:33:02 +0800] [9928] [INFO] Listening at: http://0.0.0.0:8004 (9928)<br>
> [2018-06-07 19:33:02 +0800] [9928] [INFO] Using worker: gevent<br>
> [2018-06-07 19:33:02 +0800] [9931] [INFO] Booting worker with pid: 9931<br>

访问 `http://localhost:8004` 即可看到系统的登录界面使用 guone，但因为 guone 依赖 darknet 框架 和 VLFeat 工具包，
所以你需要安装完成 darknet 并下载配置 VLFeat 工具包后才能正常使用，下面介绍安装方法。

### 使用 darknet 

darknet 是一个用 C 和 CUDA 编写的相当不错的开源神经网络框架，这是[作者的 darknet 主页](https://pjreddie.com/darknet/)。<br><br>
关于安装和使用，请阅读 darknet 主页的 [`Installing Darknet`](https://pjreddie.com/darknet/install/) 和 
[`YOLO: Real-Time Object Detection`](https://pjreddie.com/darknet/yolo/)，有详细介绍。<br>
你需要在你的机子上根据你的需要以及硬件条件决定是否安装 OpenCV  和 CUDA，安装完成后，
在 `MakeFile` 中修改相关选项。因为我的代码已经编译过，你需要进入 darknet 目录执行：<br>
```sh
meke clean
```

然后重新编译完成即可使用：<br>
```sh
meke -j16
```

#### 测试一下
站在大神的肩膀上，一切都变得很简单。<br><br>
采用本系统训练好的模型（当然你也可以下载官网给出的其他模型）进行测试，命令如下（windows 下使用 `darknet.exe` 即可）
1. building_v3.cfg 复杂版网络
```sh
./darknet detector test cfg/building.data cfg/building_v3.cfg weights/building_v3.weights test_image_path
```

2. building_v3_tiny.cfg 简版网络，速度比上面的快10多倍，检测效果略差。

```sh
/darknet detector test cfg/building.data cfg/building_v3_tiny.cfg weights/building_v3_tiny.weights  test_image_path
```

3. 开启摄像头实时检测，需要在编译时开启 CUDA 和 opencv,不用` -c `指定摄像头时 opencv 默认为 0。
```sh
./darknet detector demo cfg/building.data cfg/building_v3.cfg weights/building_v3.weights  [ -c <num> ]
```

4. 检测本地视频文件，至少需要在编译时开启 opencv。

```sh
./darknet detector demo cfg/building.data cfg/building_v3.cfg weights/building_v3.weights  test_video_file_path
```


如果测试成功，则说明你已经成功安装并可以使用 darknet 框架了。

#### 安装 opencv 以及安装后编译遇到问题
关于安装opencv ，各操作系统不相同，推荐 使用 Google 或者必应搜索国际版 搜索关键字 `opencv3 install on your_system `来找到靠谱的教程。<br>
笔者 `mac os` 系统安装，推荐[这篇教程](https://www.learnopencv.com/install-opencv3-on-macos/)。<br>
安装成功opencv 后，在 MakeFile 中令：
```sh
OPENCV = 1
```

遇到问题：

> gcc -Iinclude/ -Isrc/ -DOPENCV `pkg-config --cflags opencv`  -Wall -Wno-unknown-pragmas -Wfatal-```<br>
> errors -fPIC -Ofast -DOPENCV -c ./src/gemm.c -o obj/gemm.o<br>
> In file included from /usr/local/include/opencv2/core/types_c.h:59:0,<br>
>                  from /usr/local/include/opencv2/core/core_c.h:48,<br>
>                  from /usr/local/include/opencv2/highgui/highgui_c.h:45,<br>
>                  from include/darknet.h:25,<br>
>                  from ./src/utils.h:5,<br>
>                  from ./src/gemm.c:2:<br>
> /usr/local/include/opencv2/core/cvdef.h:485:1: error: unknown type name ‘namespace’<br>
> namespace cv {<br>
>    ^~~~~~~~~ <br>
> compilation terminated due to -Wfatal-errors.<br>
> Makefile:85: recipe for target 'obj/gemm.o' failed<br>
> make: *** [obj/gemm.o] Error 1
>


这也是笔者在使用`opencv`编译所遇到的问题，可参考[这里](https://github.com/pjreddie/darknet/issues/485)解决。

### VLFeat
本系统在传统图像分类模式中图像特征的提取（计算图像`sift`特征值）使用了开源工具包`VLFeat`提供的二进制文件，[获取我要工具包](http://www.vlfeat.org/)。该工具包支持主流的`（windows, Mac, Linux）`操作系统，下载好工具包后，我们只需要 `sift` 的可执行文件，将其在系统中的配置：
> 在 scripta/sift.py 的方法 `process_image()`中的`cmmd`给出 `sift`  可执行文件的位置即可。

### buildout
buildout 是一个基于 Python 的构建工具, 通过一个配置文件，可以从多个部分创建、组装并部署你的应用，即使应用包含了非 Python 的组件，buildout 也能够胜任。 buildout 不但能够像 setuptools 一样自动更新或下载安装依赖包，而且还能够像 virtualenv 一样，构建一个封闭隔离的开发环境。<br><br>
开发过程中如果需要添加依赖，只需要在 setup.py 中的 install_requires 中添加你的包名，然后 `buildout` 一下即可。

## 关于训练
本系统的有两种模式，其中主要介绍实时目标识别 `Yolo(darknet)` 关于自己数据集的训练。
### Yolo (darknet)
训练过程步骤细节较多，需细心关注，大致可以分为以下阶段：

1. 数据准备，采集图像数据，预处理等；
2. 标注，推荐使用[LabelImg](https://github.com/tzutalin/labelImg)。该工具在 linux  和 windows 下安装极为简单，mac os 下比较困难，作者在 github 上有说明。
3. 理解并修改 `darknet/scripts/voc_label.py`，并用其将标注产生的 `xml` 文件转换成 `yolo` 需要的格式，以及生成相关图像路径文件；
4. 准备你的 `pro_name.names` 和 `pro_name.data` ；
5. 配置你想采用的网络，本系统使用了 `yolov3-voc.cfg` 和 `yolov3-tiny.cfg`两个版本 ；
5. 下载预训练模型/权重文件，开始训练，命令如下：
```sh
./darknet detector train cfg/your_pro_name.data cfg/your_pro_name.cfg [预训练模型] [-gpus 0,1,2,3]
```

> 这里墙裂推荐使用 GPU，没有条件的可以瞅瞅[极客云](http://www.jikecloud.net/)，不是打广告，笔者就是用的这个，觉着很好用，方便性，价比高。CPU 的话，额，等的你花儿都谢了。<br>

 7. 测试你的模型/权重文件。

具体过程可以参考[这篇](https://www.cnblogs.com/antflow/p/7350274.html)博文。<br>
这是 yolov2 的训练过程，与 yolov3 的训练过程主要相差在网络文件的修改配置，v3 可看[这篇](https://blog.csdn.net/lilai619/article/details/79695109)博文。
### 图像分类模式
图像分类模式的本地图像库训练方法很简单：依次使用脚本<br>
 - `guone/core/savevocab.py`         图像训练<br>
 - `guone/core/buildindex.py`       建库创索引/存储库<br>
 - `guone/query.py`(可选)       查询测试<br>

此部分图像处理参考自[《Python计算机视觉编程》](http://yongyuan.name/pcvwithpython/)
