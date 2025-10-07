<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">xBACnet v1.0.0</h1>
<h4 align="center">Publier n'importe quelle donnée en tant que BACnet</h4>

[简体中文](./README_CN.md) | [English](./README.md) | Français

## Introduction xBACnet

xBACnet publie n'importe quelle donnée en tant que BACnet !

Cette application est un logiciel serveur BACnet utilisé pour publier diverses données en tant que multiples services de base dans un réseau BACnet.
Les services pris en charge incluent Who-Is, I-Am pour la liaison d'appareils, lecture/écriture de propriétés, lecture/écriture de propriétés multiples et abonnement aux changements de valeur.


## Prérequis
Base de données MySQL
Python (3.4 3.5 3.6 3.7 3.8 3.9 3.10)


## Installation

* Cloner le code source
```
git clone https://gitee.com/xbacnet/xbacnet
```
* Créer la base de données
```
mysql -u root -p < xbacnet/database/xbacnet.sql
```
* Installer les dépendances
```
sudo cp ~/xbacnet/xbacnet-server /xbacnet-server
cd /xbacnet-server
sudo pip install -r requirements.txt
```

* Configurer xbacnet-server

Ouvrir le fichier de configuration
Modifier l'adresse : lo vers le nom d'interface réel en exécutant 'ip a'
Modifier l'ID d'objet
```
$ sudo nano /xbacnet-server/config.ini
```

Éditer le fichier de paramètres de base de données
```
sudo nano /xbacnet-server/settings.py
```

* Ouvrir le port du pare-feu
```
$ sudo ufw allow 47808
```


### Exemple config.ini
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


* Débogage
```
$ sudo python3 server.py --debug --ini config.ini
-- Utiliser --help pour l'aide
$ sudo python3 server.py --help
```

* Déployer xbacnet-server
```
sudo cp /xbacnet-server/xbacnet-server.service /lib/systemd/system/
```

```
sudo systemctl enable xbacnet-server.service
```

```
sudo systemctl start xbacnet-server.service
```

* Comment utiliser
Ajouter des objets dans la base de données, éditer les propriétés des objets, écrire les données à publier dans present_value

## Plan de développement

1. Ajouter des journaux
2. Rechargement automatique de la liste des objets
3. Ajouter la gestion des exceptions
4. Ajouter une API
5. Ajouter une interface Web

## Groupe WeChat

![WeChat Group](qr_code_wechat_group.png)
