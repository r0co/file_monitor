# 项目介绍

> 简介

该项目使用python3开发，用于各种攻防演练中的简单防御，目前仅支持linux服务器。

> 功能

1. 监视指定目录下文件的增加、删除及更改。
2. 自带黑名单机制。当探测到危险文件生成时，自动更改改文件权限（文件权限及黑名单由用户所决定）。

# 配置与使用

## 配置

> 项目配置

打开file_monitor.py，在__init__方法中进行各种修改即可。

配置项包括：

1. 需要监视的文件夹的路径（最好为绝对路径）
2. 文件后缀名黑名单
3. 赋予危险文件的默认权限
4. 提示信息颜色

> 环境配置

```
pip install -r requirements.txt
```

或

```
pip3 install wheels/termcolor-1.1.0-py2.py3-none-any.whl
```


## 使用

```
python3 file_monitor.py
```

# 项目运行截图

![](http://ww1.sinaimg.cn/large/006oxUXCly1gboznx75x2j30p004wjrl.jpg)
