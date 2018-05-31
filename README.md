# Guone 
### Guone 是一个较为简单的入门级建筑自动识别系统，支持传统分类和目标检测两种模式。
#### 系统录屏效果如下：
[![Watch the video](https://raw.github.com/GabLeRoux/WebMole/master/ressources/WebMole_Youtube_Video.png)](http://youtu.be/vt5fpE0bzSY)

# 项目结构及核心目录介绍

> 
 -  `darknet/`：[darknet](https://pjreddie.com/darknet/ "darknet") 根目录，可完全独立使用<br>
	-  `cfg/`：各版本网络<br>
		-  `...`
		-  `building_v3.cfg`：本系统采用的复杂版的网络配置<br>
		- `building_v3_tiny.cfg`：本系统采用的简版的网络配置<br>
		- `...`
	- `data/VOCdevkit/building2018/` : 本系统的训练数据集
	- `...`
	- `weights/`: 训练好的模型文件
		- `building_v3.weights`：对应 `building_v3.cfg`  训练出的复杂模型/权重文件
		- `building_v3_tiny.weights`：对应 ` building_v3_tiny.cfg`  训练出的简版模型/权重文件
	- `...`
-  `forms/`：所用表单<br>
- `models/`：数据模型<br>
-  `static/`：静态文件<br>
-  `scripts/`：脚本文件，传统分类模式的计算模块<br>
- `templates/`：HTML 模板<br>
- `views/`：路由、视图<br>
- `tests/`：测试图片<br>
	- `1/`：模式1（传统分类）的测试图片<br>
	- `2/`：模式2（目标检测）的测试图片<br>
- `config.py`：相关配置<br>
- `app.py`：启动文件<br>
# 启动 Guone
Guone的依赖较多，请按下面介绍安装相关依赖与支持。
## 使用 darknet 
`darknet` 是用 `C` 写的一个相当不错的开源神经网络框架，这是[作者的 `darknet` 主页](https://pjreddie.com/darknet/).
关于安装和使用，请阅读 `darknet` 主页的 `Installing Darknet` 和 `YOLO: Real-Time Object Detection`，里面有详细的介绍。之后需要在你的机子上根据你的需要以及硬件条件（是否安装了 `OpenCV`  和 `CUDA` ）` make` 完成后即可使用。
## 测试
站在大神的肩膀上，一切都变得很简单。
采用本系统训练好的模型（当然你也可以下载官网给出的其他模型）进行测试，命令如下（`windows` 下使用 `darknet.exe` 即可）
1. building_v3.cfg 复杂版网络
> `./darknet detector test cfg/building.data cfg/building_v3.cfg weights/building_v3.weights test_image_path`

2. building_v3_tiny.cfg 简版网络，速度比上面的快10多倍，检测效果略差。

>  `./darknet detector test cfg/building.data cfg/building_v3_tiny.cfg weights/building_v3_tiny.weights  test_image_path`

3. 开启摄像头实时检测，需要在编译时开启 ` CUDA ` 和  `OpenCV`,不用` -c `指定摄像头时` opencv` 默认为 `0`。
>  `./darknet detector demo cfg/building.data cfg/building_v3.cfg weights/building_v3.weights  [ -c <num> ]`

4. 检测本地视频文件，至少需要在编译时开启  `OpenCV`。

>  `./darknet detector demo cfg/building.data cfg/building_v3.cfg weights/building_v3.weights  test_video_file_path`

## 安装 opencv 以及安装后编译遇到问题
关于安装`opencv` ，各操作系统不相同，推荐 使用 `Google` 或者 必应搜索国际版 搜索关键字 `opencv3 install on your_system `来找到靠谱的教程，笔者 `mac os` 系统安装，推荐[这篇教程](https://www.learnopencv.com/install-opencv3-on-macos/)。
安装成功`opencv` 后，在 `MakeFile` 中令：
> `OPENCV = 1`

遇到问题：

> gcc -Iinclude/ -Isrc/ -DOPENCV `pkg-config --cflags opencv`  -Wall<br>
> -Wno-unknown-pragmas -Wfatal-``` errors -fPIC -Ofast -DOPENCV -c ./src/gemm.c -o obj/gemm.o In file included from<br>
> /usr/local/include/opencv2/core/types_c.h:59:0,<br>
>                  from /usr/local/include/opencv2/core/core_c.h:48,<br>
>                  from /usr/local/include/opencv2/highgui/highgui_c.h:45,<br>
>                  from include/darknet.h:25,<br>
>                  from ./src/utils.h:5,<br>
>                  from ./src/gemm.c:2: /usr/local/include/opencv2/core/cvdef.h:485:1: error: unknown type<br>
> name ‘namespace’  namespace cv {  ^~~~~~~~~ compilation terminated due
> to -Wfatal-errors. Makefile:85: recipe for target 'obj/gemm.o' failed
> make: *** [obj/gemm.o] Error 1<br>

这也是笔者在使用`opencv`编译所遇到的问题，可参考[这里](https://github.com/pjreddie/darknet/issues/485)解决。
## VLFeat
本系统在传统分类模式中图像特征的提取（计算图像`sift`特征值）使用了开源工具包`VLFeat`提供的二进制文件，[获取我要工具包](http://www.vlfeat.org/)。该工具包支持主流的`（Windows, Mac, Linux）`操作系统，下载好工具包后，我们只需要 `sift` 的可执行文件，将其在系统中的配置：
> 在`scripta/sift.py` 的方法 `process_image()`中的`cmmd`给出 `sift`  可执行文件的位置即可。
  
##其他依赖
发使用`python2.7`，数据库使用`sqlite3`，在使用` python app.py` 启动项目时，根据报错没有模块 `X` 使用 `pip install X` 安装即可，推荐采用虚拟隔离环境的方式（上面安装 `opencv` 的教程里也有，这里给出 `python2.x` 在 `mac os`下 的教程）。
> `pip install virtualenv virtualenvwrapper`
> `echo "VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python2" >> ~/.bash_profile`
> `echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bash_profile`
> `source ~/.bash_profile`

创建一个虚拟环境：
> `mkvirtualenv your_pro_name -p python2`

进入该环境：
> `workon your_pro_name`

在该环境中使用 `pip` 来安装需要的包，以及运行相关项目。当需要退出此环境时：
> `deactivate` 

## 启动 Guone
>  `workon your_pro_name` 
>  `python app.py`
