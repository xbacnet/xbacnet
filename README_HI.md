<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">xBACnet v1.0.0</h1>
<h4 align="center">किसी भी डेटा को BACnet के रूप में प्रकाशित करें</h4>

[简体中文](./README_CN.md) | [English](./README.md) | Français | Español | Русский | Português | हिन्दी

## xBACnet का परिचय

xBACnet किसी भी डेटा को BACnet के रूप में प्रकाशित करता है!

यह एप्लिकेशन एक BACnet सर्वर सॉफ्टवेयर है जिसका उपयोग BACnet नेटवर्क में विभिन्न डेटा को कई मुख्य सेवाओं के रूप में प्रकाशित करने के लिए किया जाता है।
समर्थित सेवाओं में Who-Is, I-Am डिवाइस बाइंडिंग के लिए, गुण पढ़ना/लिखना, कई गुण पढ़ना/लिखना और मूल्य परिवर्तन सब्सक्रिप्शन शामिल हैं।


## आवश्यकताएं
MySQL डेटाबेस
Python (3.4 3.5 3.6 3.7 3.8 3.9 3.10)


## स्थापना

* स्रोत कोड क्लोन करें
```
git clone https://gitee.com/xbacnet/xbacnet
```
* डेटाबेस बनाएं
```
mysql -u root -p < xbacnet/database/xbacnet.sql
```
* निर्भरताएं स्थापित करें
```
sudo cp ~/xbacnet/xbacnet-server /xbacnet-server
cd /xbacnet-server
sudo pip install -r requirements.txt
```

* xbacnet-server कॉन्फ़िगर करें

कॉन्फ़िगरेशन फ़ाइल खोलें
पता संशोधित करें: 'ip a' चलाकर lo को वास्तविक इंटरफ़ेस नाम में बदलें
ऑब्जेक्ट ID संशोधित करें
```
$ sudo nano /xbacnet-server/config.ini
```

डेटाबेस सेटिंग्स फ़ाइल संपादित करें
```
sudo nano /xbacnet-server/settings.py
```

* फ़ायरवॉल पोर्ट खोलें
```
$ sudo ufw allow 47808
```


### उदाहरण config.ini
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


* डिबगिंग
```
$ sudo python3 server.py --debug --ini config.ini
-- सहायता के लिए --help का उपयोग करें
$ sudo python3 server.py --help
```

* xbacnet-server तैनात करें
```
sudo cp /xbacnet-server/xbacnet-server.service /lib/systemd/system/
```

```
sudo systemctl enable xbacnet-server.service
```

```
sudo systemctl start xbacnet-server.service
```

* कैसे उपयोग करें
डेटाबेस में ऑब्जेक्ट जोड़ें, ऑब्जेक्ट गुण संपादित करें, प्रकाशित करने के लिए डेटा को present_value में लिखें

## विकास योजना

1. लॉग जोड़ें
2. ऑब्जेक्ट सूची का स्वचालित पुनः लोड
3. अपवाद हैंडलिंग जोड़ें
4. API जोड़ें
5. वेब इंटरफ़ेस जोड़ें

## WeChat समूह

![WeChat Group](qr_code_wechat_group.png)
