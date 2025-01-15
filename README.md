<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">xBACnet v1.0.0</h1>
<h4 align="center">Publish Any Data as BACnet</h4>

[简体中文](./README_CN.md) | [English](./README.md)

## xBACnet Introduction

xBACnet Publish Any Data as BACnet!

This application is a BACnet server that supports many core services that
applications need to present data on a BACnet network.  It supports Who-Is
and I-Am for device binding, Read and Write Property, Read and Write
Property Multiple, and COV subscriptions.


## Prerequisites 
MySQL Server
Python (3.4 3.5 3.6 3.7 3.8 3.9 3.10)


## Installation

* Clone Source Code
```
git clone https://gitee.com/xbacnet/xbacnet
```
* Create Database 
```
mysql -u root -p < xbacnet/database/xbacnet.sql
```
* Install Requirements
```
sudo cp ~/xbacnet/xbacnet-server /xbacnet-server
cd /xbacnet-server
sudo pip install -r requirements.txt
```

* Configure xbacnet-server

Open config file for local device address 
Modify address: lo to the actual interface name by running 'ip a'
Modify objectIdentifier
```
$ sudo nano /xbacnet-server/config.ini
```

Edit settings file for database configuration
```
sudo nano /xbacnet-server/settings.py
```

* Allow port in firewall
```
$ sudo ufw allow 47808
```


### Demo config.ini
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


* Debugging
```
$ sudo python3 server.py --debug --ini config.ini
-- Use --help for help
$ sudo python3 server.py --help
```

* Deploy xbacnet-server
```
sudo cp /xbacnet-server/xbacnet-server.service /lib/systemd/system/
```

```
sudo systemctl enable xbacnet-server.service
```

```
sudo systemctl start xbacnet-server.service
```

## How to Use
Add objects in the database, edit object properties, and write the data to be published into the presenter value

## TODO
1. Add logger
2. Add auto reload object_list
3. Add try...except to pro_application.add_object(pro_object)
4. API Add REST API
5. Add Web UI

## WeChat Group

![WeChat Group](qr_code_wechat_group.png)
