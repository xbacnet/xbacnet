<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">xBACnet v1.0.0</h1>
<h4 align="center">نشر أي بيانات كـ BACnet</h4>

[简体中文](./README_CN.md) | [English](./README.md) | Français | Español | Русский | Português | हिन्दी | Bahasa Indonesia | Bahasa Melayu | Tiếng Việt | Türkçe | العربية

## مقدمة xBACnet

xBACnet ينشر أي بيانات كـ BACnet!

هذا التطبيق هو برنامج خادم BACnet يُستخدم لنشر بيانات متنوعة كخدمات أساسية متعددة في شبكة BACnet.
الخدمات المدعومة تشمل Who-Is، I-Am لربط الأجهزة، قراءة/كتابة الخصائص، قراءة/كتابة خصائص متعددة والاشتراك في تغييرات القيم.


## المتطلبات المسبقة
قاعدة بيانات MySQL
Python (3.4 3.5 3.6 3.7 3.8 3.9 3.10)


## التثبيت

* استنساخ الكود المصدري
```
git clone https://gitee.com/xbacnet/xbacnet
```
* إنشاء قاعدة البيانات
```
mysql -u root -p < xbacnet/database/xbacnet.sql
```
* تثبيت التبعيات
```
sudo cp ~/xbacnet/xbacnet-server /xbacnet-server
cd /xbacnet-server
sudo pip install -r requirements.txt
```

* تكوين xbacnet-server

فتح ملف التكوين
تعديل العنوان: lo إلى اسم الواجهة الفعلي بتشغيل 'ip a'
تعديل معرف الكائن
```
$ sudo nano /xbacnet-server/config.ini
```

تحرير ملف إعدادات قاعدة البيانات
```
sudo nano /xbacnet-server/settings.py
```

* فتح منفذ الجدار الناري
```
$ sudo ufw allow 47808
```


### مثال config.ini
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


* التصحيح
```
$ sudo python3 server.py --debug --ini config.ini
-- استخدم --help للمساعدة
$ sudo python3 server.py --help
```

* نشر xbacnet-server
```
sudo cp /xbacnet-server/xbacnet-server.service /lib/systemd/system/
```

```
sudo systemctl enable xbacnet-server.service
```

```
sudo systemctl start xbacnet-server.service
```

* كيفية الاستخدام
إضافة كائنات في قاعدة البيانات، تحرير خصائص الكائنات، كتابة البيانات المراد نشرها في present_value

## خطة التطوير

1. إضافة سجلات
2. إعادة تحميل تلقائي لقائمة الكائنات
3. إضافة معالجة الاستثناءات
4. إضافة API
5. إضافة واجهة ويب

## مجموعة WeChat

![WeChat Group](qr_code_wechat_group.png)
