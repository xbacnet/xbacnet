<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">xBACnet v1.0.0</h1>
<h4 align="center">Xuất bản bất kỳ dữ liệu nào dưới dạng BACnet</h4>

[简体中文](./README_CN.md) | [English](./README.md) | Français | Español | Русский | Português | हिन्दी | Bahasa Indonesia | Bahasa Melayu | Tiếng Việt

## Giới thiệu xBACnet

xBACnet xuất bản bất kỳ dữ liệu nào dưới dạng BACnet!

Ứng dụng này là phần mềm máy chủ BACnet được sử dụng để xuất bản các dữ liệu khác nhau như nhiều dịch vụ cốt lõi trong mạng BACnet.
Các dịch vụ được hỗ trợ bao gồm Who-Is, I-Am để liên kết thiết bị, đọc/ghi thuộc tính, đọc/ghi thuộc tính đa và đăng ký thay đổi giá trị.


## Yêu cầu
Cơ sở dữ liệu MySQL
Python (3.4 3.5 3.6 3.7 3.8 3.9 3.10)


## Cài đặt

* Sao chép mã nguồn
```
git clone https://gitee.com/xbacnet/xbacnet
```
* Tạo cơ sở dữ liệu
```
mysql -u root -p < xbacnet/database/xbacnet.sql
```
* Cài đặt các phụ thuộc
```
sudo cp ~/xbacnet/xbacnet-server /xbacnet-server
cd /xbacnet-server
sudo pip install -r requirements.txt
```

* Cấu hình xbacnet-server

Mở tệp cấu hình
Sửa đổi địa chỉ: lo thành tên giao diện thực tế bằng cách chạy 'ip a'
Sửa đổi ID đối tượng
```
$ sudo nano /xbacnet-server/config.ini
```

Chỉnh sửa tệp cài đặt cơ sở dữ liệu
```
sudo nano /xbacnet-server/settings.py
```

* Mở cổng tường lửa
```
$ sudo ufw allow 47808
```


### Ví dụ config.ini
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


* Gỡ lỗi
```
$ sudo python3 server.py --debug --ini config.ini
-- Sử dụng --help để được trợ giúp
$ sudo python3 server.py --help
```

* Triển khai xbacnet-server
```
sudo cp /xbacnet-server/xbacnet-server.service /lib/systemd/system/
```

```
sudo systemctl enable xbacnet-server.service
```

```
sudo systemctl start xbacnet-server.service
```

* Cách sử dụng
Thêm đối tượng trong cơ sở dữ liệu, chỉnh sửa thuộc tính đối tượng, ghi dữ liệu cần xuất bản vào present_value

## Kế hoạch phát triển

1. Thêm nhật ký
2. Tải lại tự động danh sách đối tượng
3. Thêm xử lý ngoại lệ
4. Thêm API
5. Thêm giao diện web

## Nhóm WeChat

![WeChat Group](qr_code_wechat_group.png)
