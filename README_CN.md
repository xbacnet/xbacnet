<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">xBACnet v1.0.0</h1>
<h4 align="center">把任何数据发布为BACnet</h4>

[简体中文](./README_CN.md) | [English](./README.md)

## xBACnet 介绍

xBACnet把任何数据发布为BACnet!

此应用是一个BACnet服务器软件，用于在BACnet网络中把各种数据数据发布为多种核心服务。
支持的服务有Who-Is、I-Am用于设备绑定，读写属性，读写多属性和值变化订阅。


## 前提  
MySQL数据库
Python (3.4 3.5 3.6 3.7 3.8 3.9 3.10)


## 安装

* 克隆源代码
```
git clone https://gitee.com/xbacnet/xbacnet
```
* 创建数据库
```
mysql -u root -p < xbacnet/database/xbacnet.sql
```
* 安装依赖库
```
sudo cp ~/xbacnet/xbacnet-server /xbacnet-server
cd /xbacnet-server
sudo pip install -r requirements.txt
```

* 配置xbacnet-server

打开配置文件
修改地址 Modify address: lo to the actual interface name by running 'ip a'
修改对象ID
```
$ sudo nano /xbacnet-server/config.ini
```

编辑数据库设置文件
```
sudo nano /xbacnet-server/settings.py
```

* 打开防火墙端口
```
$ sudo ufw allow 47808
```


### 示例config.ini 
```
[BACpypes]
objectName: xBACnet Server
address: 192.168.20.193
objectIdentifier: 20193
description: xBACnet Server
vendorName: xBACnet Inc.
maxApduLengthAccepted: 1024
segmentationSupported: segmentedBoth
vendorIdentifier: 1524
foreignBBMD: 192.168.1.1
foreignTTL: 30
systemStatus: operational
```


* 调试
```
$ sudo python3 server.py --debug --ini config.ini
-- Use --help for help
$ sudo python3 server.py --help
```

* 部署xbacnet-server
```
sudo cp /xbacnet-server/xbacnet-server.service /lib/systemd/system/
```

```
sudo systemctl enable xbacnet-server.service
```

```
sudo systemctl start xbacnet-server.service
```

* 如何使用
在数据库中的添加对象，编辑对象属性，把要发布的数据写入present_value

## 开发计划

1. 增加日志
2. 自动重加载对象列表
3. 增加异常处理
4. 增加API
5. 增加Web界面

## 微信群

![WeChat Group](qr_code_wechat_group.png)
