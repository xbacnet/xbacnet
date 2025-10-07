<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">xBACnet v1.0.0</h1>
<h4 align="center">Herhangi bir veriyi BACnet olarak yayınla</h4>

[简体中文](./README_CN.md) | [English](./README.md) | Français | Español | Русский | Português | हिन्दी | Bahasa Indonesia | Bahasa Melayu | Tiếng Việt | Türkçe

## xBACnet Giriş

xBACnet herhangi bir veriyi BACnet olarak yayınlar!

Bu uygulama, BACnet ağında çeşitli verileri birden fazla temel hizmet olarak yayınlamak için kullanılan bir BACnet sunucu yazılımıdır.
Desteklenen hizmetler arasında cihaz bağlama için Who-Is, I-Am, özellik okuma/yazma, çoklu özellik okuma/yazma ve değer değişikliği aboneliği bulunur.


## Önkoşullar
MySQL veritabanı
Python (3.4 3.5 3.6 3.7 3.8 3.9 3.10)


## Kurulum

* Kaynak kodu klonla
```
git clone https://gitee.com/xbacnet/xbacnet
```
* Veritabanı oluştur
```
mysql -u root -p < xbacnet/database/xbacnet.sql
```
* Bağımlılıkları yükle
```
sudo cp ~/xbacnet/xbacnet-server /xbacnet-server
cd /xbacnet-server
sudo pip install -r requirements.txt
```

* xbacnet-server'ı yapılandır

Yapılandırma dosyasını aç
Adresi değiştir: 'ip a' çalıştırarak lo'yu gerçek arayüz adına değiştir
Nesne ID'sini değiştir
```
$ sudo nano /xbacnet-server/config.ini
```

Veritabanı ayarları dosyasını düzenle
```
sudo nano /xbacnet-server/settings.py
```

* Güvenlik duvarı portunu aç
```
$ sudo ufw allow 47808
```


### Örnek config.ini
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


* Hata ayıklama
```
$ sudo python3 server.py --debug --ini config.ini
-- Yardım için --help kullan
$ sudo python3 server.py --help
```

* xbacnet-server'ı dağıt
```
sudo cp /xbacnet-server/xbacnet-server.service /lib/systemd/system/
```

```
sudo systemctl enable xbacnet-server.service
```

```
sudo systemctl start xbacnet-server.service
```

* Nasıl kullanılır
Veritabanına nesneler ekle, nesne özelliklerini düzenle, yayınlanacak verileri present_value'ya yaz

## Geliştirme planı

1. Günlük kayıtları ekle
2. Nesne listesinin otomatik yeniden yüklenmesi
3. İstisna işleme ekle
4. API ekle
5. Web arayüzü ekle

## WeChat Grubu

![WeChat Group](qr_code_wechat_group.png)
