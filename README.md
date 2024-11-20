# OrbbecSDK_ros2_py

**本项目基于[pyorbbecsdk](https://github.com/orbbec/pyorbbecsdk)**

> 官方的[OrbbecSDK_ROS2_warpper](https://github.com/orbbec/OrbbecSDK_ROS2)用不了，遂自己编写 orz

# 依赖

克隆库，编译，安装

```bash
git clone https://github.com/orbbec/pyorbbecsdk.git
cd pyorbbecsdk
pip3 install -r requirements.txt

python setup.py build
python setup.py install
```

> 本项目是在树莓派上进行部署，未使用 python 虚拟环境，测试时建议在虚拟环境进行

# 部署

在工作空间下

```bash
cd src
git clone https://github.com/YinAGVlab/OrbbecSDK_ros2_py.git
cd ..
colcon build --packages-select OrbbecSDK_ros2_py
```
