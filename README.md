# Guone 
### Guone 是一个较为简单的入门级建筑自动识别系统，支持传统分类和目标检测两种模式。
#### 系统录屏效果如下：
[![Watch the video](https://raw.github.com/GabLeRoux/WebMole/master/ressources/WebMole_Youtube_Video.png)](http://youtu.be/vt5fpE0bzSY)

# 项目结构及核心目录介绍

> 
 1.  `darknet/`：[darknet](https://pjreddie.com/darknet/ "darknet") 根目录，可完全独立使用<br>
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
 2.  `forms/`：所用表单<br>
 3.  `models/`：数据模型<br>
 4.  `static/`：静态文件<br>
 5.  `scripts/`：脚本文件，传统分类模式的计算模块<br>
 6. `templates/`：HTML 模板<br>
 7. `views/`：路由、视图<br>
 8.  `tests/`：测试图片<br>
	- `1/`：模式1（传统分类）的测试图片
	- `2/`：模式2（目标检测）的测试图片
 9. `config.py`：相关配置<br>
 10.  `app.py`：启动文件<br>
# 启动 Guone
Guone的依赖较多，请按下面介绍安装相关依赖与支持。
## 使用 darknet 
darknet 是用 C 写的一个相当不错的开源神经网络框架，这是[作者的 `darknet` 主页](https://pjreddie.com/darknet/)，关于安装和使用，请阅读 `darknet` 主页的 `Installing Darknet` 和 `YOLO: Real-Time Object Detection`，里面有详细的介绍。之后需要在你的机子上根据你的需要以及硬件条件（是否安装了 `OpenCV`  和 `CUDA` ）` make` 完成后即可使用。
## 测试
站在大神的肩膀上，一切都变得很简单。
采用本系统训练好的模型（当然你也可以下载官网给出的其他模型）进行测试，命令如下（mac os 与linux下）
1. building_v3.cfg 复杂版网络
> `./darknet detector test cfg/building.data cfg/building_v3.cfg weights/building_v3.weights test_image_path`

2. building_v3_tiny.cfg 简版网络

>  `./darknet detector test cfg/building.data cfg/building_v3_tiny.cfg weights/building_v3_tiny.weights `
## 启动
> `python app.py`
