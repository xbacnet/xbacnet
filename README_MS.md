<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">xBACnet v1.0.0</h1>
<h4 align="center">Terbitkan sebarang data sebagai BACnet</h4>

[简体中文](./README_CN.md) | [English](./README.md) | Français | Español | Русский | Português | हिन्दी | Bahasa Indonesia | Bahasa Melayu

## Pengenalan xBACnet

xBACnet menerbitkan sebarang data sebagai BACnet!

Aplikasi ini adalah perisian pelayan BACnet yang digunakan untuk menerbitkan pelbagai data sebagai pelbagai perkhidmatan teras dalam rangkaian BACnet.
Perkhidmatan yang disokong termasuk Who-Is, I-Am untuk pengikatan peranti, membaca/menulis sifat, membaca/menulis sifat berganda dan langganan perubahan nilai.


## Prasyarat
Pangkalan data MySQL
Python (3.4 3.5 3.6 3.7 3.8 3.9 3.10)


## Pemasangan

* Klon kod sumber
```
git clone https://gitee.com/xbacnet/xbacnet
```
* Cipta pangkalan data
```
mysql -u root -p < xbacnet/database/xbacnet.sql
```
* Pasang kebergantungan
```
sudo cp ~/xbacnet/xbacnet-server /xbacnet-server
cd /xbacnet-server
sudo pip install -r requirements.txt
```

* Konfigurasi xbacnet-server

Buka fail konfigurasi
Ubah alamat: lo kepada nama antara muka sebenar dengan menjalankan 'ip a'
Ubah ID objek
```
$ sudo nano /xbacnet-server/config.ini
```

Edit fail tetapan pangkalan data
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


* Penyahpepijat
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
Tambah objek dalam pangkalan data, edit sifat objek, tulis data yang akan diterbitkan ke present_value

## Rancangan pembangunan

1. Tambah log
2. Muat semula automatik senarai objek
3. Tambah pengendalian pengecualian
4. Tambah API
5. Tambah antara muka web

## Kumpulan WeChat

![WeChat Group](qr_code_wechat_group.png)
