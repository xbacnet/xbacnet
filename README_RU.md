<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">xBACnet v1.0.0</h1>
<h4 align="center">Публикация любых данных как BACnet</h4>

[简体中文](./README_CN.md) | [English](./README.md) | Français | Español | Русский

## Введение xBACnet

xBACnet публикует любые данные как BACnet!

Это приложение представляет собой серверное программное обеспечение BACnet, используемое для публикации различных данных в качестве множественных основных сервисов в сети BACnet.
Поддерживаемые сервисы включают Who-Is, I-Am для привязки устройств, чтение/запись свойств, чтение/запись множественных свойств и подписку на изменения значений.


## Предварительные требования
База данных MySQL
Python (3.4 3.5 3.6 3.7 3.8 3.9 3.10)


## Установка

* Клонировать исходный код
```
git clone https://gitee.com/xbacnet/xbacnet
```
* Создать базу данных
```
mysql -u root -p < xbacnet/database/xbacnet.sql
```
* Установить зависимости
```
sudo cp ~/xbacnet/xbacnet-server /xbacnet-server
cd /xbacnet-server
sudo pip install -r requirements.txt
```

* Настроить xbacnet-server

Открыть файл конфигурации
Изменить адрес: lo на реальное имя интерфейса, выполнив 'ip a'
Изменить идентификатор объекта
```
$ sudo nano /xbacnet-server/config.ini
```

Редактировать файл настроек базы данных
```
sudo nano /xbacnet-server/settings.py
```

* Открыть порт брандмауэра
```
$ sudo ufw allow 47808
```


### Пример config.ini
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


* Отладка
```
$ sudo python3 server.py --debug --ini config.ini
-- Использовать --help для справки
$ sudo python3 server.py --help
```

* Развернуть xbacnet-server
```
sudo cp /xbacnet-server/xbacnet-server.service /lib/systemd/system/
```

```
sudo systemctl enable xbacnet-server.service
```

```
sudo systemctl start xbacnet-server.service
```

* Как использовать
Добавить объекты в базу данных, редактировать свойства объектов, записать данные для публикации в present_value

## План разработки

1. Добавить логирование
2. Автоматическая перезагрузка списка объектов
3. Добавить обработку исключений
4. Добавить API
5. Добавить веб-интерфейс

## Группа WeChat

![WeChat Group](qr_code_wechat_group.png)
