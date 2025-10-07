<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">xBACnet v1.0.0</h1>
<h4 align="center">Publicar cualquier dato como BACnet</h4>

[简体中文](./README_CN.md) | [English](./README.md) | Français | Español

## Introducción xBACnet

¡xBACnet publica cualquier dato como BACnet!

Esta aplicación es un software servidor BACnet utilizado para publicar varios datos como múltiples servicios principales en una red BACnet.
Los servicios soportados incluyen Who-Is, I-Am para vinculación de dispositivos, lectura/escritura de propiedades, lectura/escritura de propiedades múltiples y suscripción a cambios de valor.


## Prerrequisitos
Base de datos MySQL
Python (3.4 3.5 3.6 3.7 3.8 3.9 3.10)


## Instalación

* Clonar el código fuente
```
git clone https://gitee.com/xbacnet/xbacnet
```
* Crear la base de datos
```
mysql -u root -p < xbacnet/database/xbacnet.sql
```
* Instalar dependencias
```
sudo cp ~/xbacnet/xbacnet-server /xbacnet-server
cd /xbacnet-server
sudo pip install -r requirements.txt
```

* Configurar xbacnet-server

Abrir el archivo de configuración
Modificar la dirección: lo al nombre de interfaz real ejecutando 'ip a'
Modificar el ID del objeto
```
$ sudo nano /xbacnet-server/config.ini
```

Editar el archivo de configuración de la base de datos
```
sudo nano /xbacnet-server/settings.py
```

* Abrir el puerto del firewall
```
$ sudo ufw allow 47808
```


### Ejemplo config.ini
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


* Depuración
```
$ sudo python3 server.py --debug --ini config.ini
-- Usar --help para ayuda
$ sudo python3 server.py --help
```

* Desplegar xbacnet-server
```
sudo cp /xbacnet-server/xbacnet-server.service /lib/systemd/system/
```

```
sudo systemctl enable xbacnet-server.service
```

```
sudo systemctl start xbacnet-server.service
```

* Cómo usar
Agregar objetos en la base de datos, editar propiedades de objetos, escribir los datos a publicar en present_value

## Plan de desarrollo

1. Agregar registros
2. Recarga automática de la lista de objetos
3. Agregar manejo de excepciones
4. Agregar API
5. Agregar interfaz web

## Grupo WeChat

![WeChat Group](qr_code_wechat_group.png)
