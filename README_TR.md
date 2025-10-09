<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">xBACnet v1.0.0</h1>
<h4 align="center">Herhangi bir veriyi BACnet olarak yayınla</h4>

[简体中文](./README_CN.md) | [English](./README.md) | [Français](./README_FR.md) | [Español](./README_ES.md) | [Русский](./README_RU.md) | [Português](./README_PT.md) | [हिन्दी](./README_HI.md) | [Bahasa Indonesia](./README_ID.md) | [Bahasa Melayu](./README_MS.md) | [Tiếng Việt](./README_VI.md) | [Türkçe](./README_TR.md) | [العربية](./README_AR.md)

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

## Nasıl kullanılır
Veritabanına nesneler ekle, nesne özelliklerini düzenle, yayınlanacak verileri present_value'ya yaz

## Web Yönetim Arayüzü

xBACnet artık BACnet nesnelerinin kolay yapılandırması ve izlenmesi için modern bir web tabanlı yönetim arayüzü içeriyor.

### Özellikler

#### 🔐 Kullanıcı Kimlik Doğrulama
- Rol tabanlı erişim kontrolü ile güvenli giriş sistemi
- Varsayılan kimlik bilgileri: `administrator` / `!BACnetPro1`

![Giriş Sayfası](images/login.png)

#### 📊 Kontrol Paneli
- Gerçek zamanlı istatistiklerle sistem genel bakışı
- Nesne dağılımını gösteren etkileşimli grafikler
- Sistem durumu izleme
- Son aktivite günlükleri

![Kontrol Paneli](images/dashboard.png)

#### 🏗️ BACnet Nesne Yönetimi
Tüm BACnet nesne türleri için tam CRUD işlemleri:

**Analog Nesneler**
- **Analog Girişler**: Sensörlerden analog giriş değerlerini izleme
- **Analog Çıkışlar**: Analog çıkış cihazlarını kontrol etme
- **Analog Değerler**: Analog değerleri saklama ve yönetme

![Analog Girişler](images/analog-inputs.png)
![Analog Çıkışlar](images/analog-outputs.png)
![Analog Değerler](images/analog-values.png)

**İkili Nesneler**
- **İkili Girişler**: İkili giriş durumlarını izleme (açık/kapalı)
- **İkili Çıkışlar**: İkili çıkış cihazlarını kontrol etme
- **İkili Değerler**: İkili değerleri saklama ve yönetme

![İkili Girişler](images/binary-inputs.png)
![İkili Çıkışlar](images/binary-outputs.png)
![İkili Değerler](images/binary-values.png)

**Çok Durumlu Nesneler**
- **Çok Durumlu Girişler**: Çok durumlu giriş cihazlarını izleme
- **Çok Durumlu Çıkışlar**: Çok durumlu çıkış cihazlarını kontrol etme
- **Çok Durumlu Değerler**: Çok durumlu değerleri saklama ve yönetme

![Çok Durumlu Girişler](images/multi-state-inputs.png)
![Çok Durumlu Çıkışlar](images/multi-state-outputs.png)
![Çok Durumlu Değerler](images/multi-state-values.png)

#### 👥 Kullanıcı Yönetimi
- Kullanıcı hesapları oluşturma, düzenleme ve silme
- Rol tabanlı izinler
- Kullanıcı aktivite takibi

![Kullanıcı Yönetimi](images/user-management.png)

### Hızlı Başlangıç

1. **API Sunucusunu Başlat**
   ```bash
   cd xbacnet-api
   python run.py --port 8000
   ```

2. **Web Arayüzünü Başlat**
   ```bash
   cd xbacnet-web
   npm install
   npm run dev
   ```

3. **Arayüze Erişim**
   - Tarayıcıyı `http://localhost:3000` adresinde aç
   - Şununla giriş yap: `administrator` / `!BACnetPro1`

### Teknoloji Yığını
- **Frontend**: Vue 3 + Element Plus + ECharts
- **Backend**: Python Falcon REST API
- **Veritabanı**: MySQL
- **Kimlik Doğrulama**: JWT tabanlı güvenlik

## WeChat Grubu

![WeChat Group](qr_code_wechat_group.png)
