# Guone 
### Guone 是一个较为简单的入门级建筑自动识别系统，支持传统分类和目标检测两种模式。
#### 系统录屏效果如下：
[![Watch the video](https://raw.github.com/GabLeRoux/WebMole/master/ressources/WebMole_Youtube_Video.png)](http://youtu.be/vt5fpE0bzSY)
# 启动

> `python app.py`


# 项目结构及核心目录介绍
> 
-  `darknet/`：[darknet](https://pjreddie.com/darknet/ "darknet") 根目录<br>
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
-  `forms/`：所用表单<br>
-  `models/`：数据模型<br>
-  `static/`：静态文件<br>
-  `scripts/`：脚本文件，传统分类模式的计算模块<br>
- `templates/`：HTML 模板<br>
- `views/`：路由、视图<br>
-  `tests/`：测试图片<br>
	- `1/`：模式1（传统分类）的测试图片
	- `2/`：模式2（目标检测）的测试图片
- `config.py`：相关配置<br>
-  `app.py`：启动文件<br>
