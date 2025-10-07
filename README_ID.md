<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">xBACnet v1.0.0</h1>
<h4 align="center">Publikasikan data apa pun sebagai BACnet</h4>

[简体中文](./README_CN.md) | [English](./README.md) | Français | Español | Русский | Português | हिन्दी | Bahasa Indonesia

## Pengenalan xBACnet

xBACnet mempublikasikan data apa pun sebagai BACnet!

Aplikasi ini adalah perangkat lunak server BACnet yang digunakan untuk mempublikasikan berbagai data sebagai beberapa layanan inti dalam jaringan BACnet.
Layanan yang didukung termasuk Who-Is, I-Am untuk pengikatan perangkat, membaca/menulis properti, membaca/menulis properti ganda dan berlangganan perubahan nilai.


## Prasyarat
Database MySQL
Python (3.4 3.5 3.6 3.7 3.8 3.9 3.10)


## Instalasi

* Kloning kode sumber
```
git clone https://gitee.com/xbacnet/xbacnet
```
* Buat database
```
mysql -u root -p < xbacnet/database/xbacnet.sql
```
* Instal dependensi
```
sudo cp ~/xbacnet/xbacnet-server /xbacnet-server
cd /xbacnet-server
sudo pip install -r requirements.txt
```

* Konfigurasi xbacnet-server

Buka file konfigurasi
Ubah alamat: lo ke nama antarmuka yang sebenarnya dengan menjalankan 'ip a'
Ubah ID objek
```
$ sudo nano /xbacnet-server/config.ini
```

Edit file pengaturan database
```
sudo nano /xbacnet-server/settings.py
```

* Buka port firewall
```
$ sudo ufw allow 47808
```


### Contoh config.ini
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
-- Gunakan --help untuk bantuan
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

* Cara menggunakan
Tambahkan objek dalam database, edit properti objek, tulis data yang akan dipublikasikan ke present_value

## Rencana pengembangan

1. Tambahkan log
2. Muat ulang otomatis daftar objek
3. Tambahkan penanganan pengecualian
4. Tambahkan API
5. Tambahkan antarmuka web

## Grup WeChat

![WeChat Group](qr_code_wechat_group.png)
