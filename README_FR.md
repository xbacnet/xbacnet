<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">xBACnet v1.0.0</h1>
<h4 align="center">Publier n'importe quelle donnée en tant que BACnet</h4>

[简体中文](./README_CN.md) | [English](./README.md) | [Français](./README_FR.md) | [Español](./README_ES.md) | [Русский](./README_RU.md) | [Português](./README_PT.md) | [हिन्दी](./README_HI.md) | [Bahasa Indonesia](./README_ID.md) | [Bahasa Melayu](./README_MS.md) | [Tiếng Việt](./README_VI.md) | [Türkçe](./README_TR.md) | [العربية](./README_AR.md)

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

## Comment utiliser
Ajouter des objets dans la base de données, éditer les propriétés des objets, écrire les données à publier dans present_value

## Interface de Gestion Web

xBACnet inclut maintenant une interface de gestion web moderne pour faciliter la configuration et la surveillance des objets BACnet.

### Fonctionnalités

#### 🔐 Authentification Utilisateur
- Système de connexion sécurisé avec contrôle d'accès basé sur les rôles
- Identifiants par défaut : `administrator` / `!BACnetPro1`

![Page de Connexion](images/login.png)

#### 📊 Tableau de Bord
- Aperçu du système avec statistiques en temps réel
- Graphiques interactifs montrant la distribution des objets
- Surveillance de l'état du système
- Journaux d'activité récente

![Tableau de Bord](images/dashboard.png)

#### 🏗️ Gestion des Objets BACnet
Opérations CRUD complètes pour tous les types d'objets BACnet :

**Objets Analogiques**
- **Entrées Analogiques** : Surveiller les valeurs d'entrée analogique des capteurs
- **Sorties Analogiques** : Contrôler les dispositifs de sortie analogique
- **Valeurs Analogiques** : Stocker et gérer les valeurs analogiques

![Entrées Analogiques](images/analog-inputs.png)
![Sorties Analogiques](images/analog-outputs.png)
![Valeurs Analogiques](images/analog-values.png)

**Objets Binaires**
- **Entrées Binaires** : Surveiller les états d'entrée binaire (marche/arrêt)
- **Sorties Binaires** : Contrôler les dispositifs de sortie binaire
- **Valeurs Binaires** : Stocker et gérer les valeurs binaires

![Entrées Binaires](images/binary-inputs.png)
![Sorties Binaires](images/binary-outputs.png)
![Valeurs Binaires](images/binary-values.png)

**Objets Multi-états**
- **Entrées Multi-états** : Surveiller les dispositifs d'entrée multi-états
- **Sorties Multi-états** : Contrôler les dispositifs de sortie multi-états
- **Valeurs Multi-états** : Stocker et gérer les valeurs multi-états

![Entrées Multi-états](images/multi-state-inputs.png)
![Sorties Multi-états](images/multi-state-outputs.png)
![Valeurs Multi-états](images/multi-state-values.png)

#### 👥 Gestion des Utilisateurs
- Créer, modifier et supprimer des comptes utilisateur
- Permissions basées sur les rôles
- Suivi de l'activité utilisateur

![Gestion des Utilisateurs](images/user-management.png)

### Démarrage Rapide

1. **Démarrer le Serveur API**
   ```bash
   cd xbacnet-api
   python run.py --port 8000
   ```

2. **Démarrer l'Interface Web**
   ```bash
   cd xbacnet-web
   npm install
   npm run dev
   ```

3. **Accéder à l'Interface**
   - Ouvrir le navigateur sur `http://localhost:3000`
   - Se connecter avec : `administrator` / `!BACnetPro1`

### Stack Technologique
- **Frontend** : Vue 3 + Element Plus + ECharts
- **Backend** : Python Falcon REST API
- **Base de Données** : MySQL
- **Authentification** : Sécurité basée sur JWT

## Groupe WeChat

![WeChat Group](qr_code_wechat_group.png)
