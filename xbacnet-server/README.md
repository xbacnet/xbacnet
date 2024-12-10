# xBACnet Server Service

## Introduction
This application is a BACnet server that supports many core services that
applications need to present data on a BACnet network.  It supports Who-Is
and I-Am for device binding, Read and Write Property, Read and Write
Property Multiple, and COV subscriptions.


## Prerequisites
bacpypes
mysql.connector


## Installation

* Download and install MySQL Connector 
refer to xbacnet-doc

* Download bacpypes online
```
$ cd ~/tools
$ git clone https://github.com/pypa/setuptools_scm.git
$ git clone https://github.com/pytest-dev/pytest-runner.git
$ git clone https://github.com/al45tair/netifaces.git
$ git clone https://github.com/JoelBender/bacpypes.git
```

* Install bacpypes
```
$ cd ~/tools/setuptools_scm/
$ sudo python3 setup.py install
$ cd ~/tools/pytest-runner/
$ sudo python3 setup.py install
$ cd ~/tools/netifaces/
$ sudo python3 setup.py install
$ cd ~/tools/bacpypes
$ sudo python3 setup.py install
```

* Allow port in firewall
```
$ sudo ufw allow 47808
```

* Configure xbacnet-server
```
sudo cp ~/xbacnet/xbacnet-server /xbacnet-server
cd /xbacnet-server
```
Open config file for local device address 
change address: lo to the actual interface name by running 'ip a'
change objectIdentifier: 600133 to an unique number
```
$ sudo nano config.ini
```
Edit settings file for database configuration
```
sudo nano settings.py
```

### Demo config.ini
```
[BACpypes]
objectName: xBACnet Server
address: 192.168.20.193/24
objectIdentifier: 20193
description: xBACnet Server
vendorName: xBACnet Inc.
maxApduLengthAccepted: 1024
segmentationSupported: segmentedBoth
vendorIdentifier: 15
foreignBBMD: 192.168.20.1
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
$ sudo cp -r ~/xbacnet/xbacnet-server /xbacnet-server
$ sudo cp /xbacnet-server/xbacnet-server.service /lib/systemd/system/
$ sudo systemctl enable xbacnet-server.service
$ sudo systemctl start xbacnet-server.service
```

* TODO
1. add logger
2. auto reload object_list
3. add try...except to pro_application.add_object(pro_object)
  