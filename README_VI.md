<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">xBACnet v1.0.0</h1>
<h4 align="center">Xuất bản bất kỳ dữ liệu nào dưới dạng BACnet</h4>

[简体中文](./README_CN.md) | [English](./README.md) | [Français](./README_FR.md) | [Español](./README_ES.md) | [Русский](./README_RU.md) | [Português](./README_PT.md) | [हिन्दी](./README_HI.md) | [Bahasa Indonesia](./README_ID.md) | [Bahasa Melayu](./README_MS.md) | [Tiếng Việt](./README_VI.md) | [Türkçe](./README_TR.md) | [العربية](./README_AR.md)

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

## Cách sử dụng
Thêm đối tượng trong cơ sở dữ liệu, chỉnh sửa thuộc tính đối tượng, ghi dữ liệu cần xuất bản vào present_value

## Giao Diện Quản Lý Web

xBACnet hiện bao gồm giao diện quản lý web hiện đại để dễ dàng cấu hình và giám sát các đối tượng BACnet.

### Tính năng

#### 🔐 Xác thực Người dùng
- Hệ thống đăng nhập bảo mật với kiểm soát truy cập dựa trên vai trò
- Thông tin đăng nhập mặc định: `administrator` / `!BACnetPro1`

![Trang Đăng nhập](images/login.png)

#### 📊 Bảng Điều khiển
- Tổng quan hệ thống với thống kê thời gian thực
- Biểu đồ tương tác hiển thị phân phối đối tượng
- Giám sát trạng thái hệ thống
- Nhật ký hoạt động gần đây

![Bảng Điều khiển](images/dashboard.png)

#### 🏗️ Quản Lý Đối tượng BACnet
Thao tác CRUD đầy đủ cho tất cả các loại đối tượng BACnet:

**Đối tượng Analog**
- **Đầu vào Analog**: Giám sát giá trị đầu vào analog từ cảm biến
- **Đầu ra Analog**: Điều khiển thiết bị đầu ra analog
- **Giá trị Analog**: Lưu trữ và quản lý giá trị analog

![Đầu vào Analog](images/analog-inputs.png)
![Đầu ra Analog](images/analog-outputs.png)
![Giá trị Analog](images/analog-values.png)

**Đối tượng Binary**
- **Đầu vào Binary**: Giám sát trạng thái đầu vào binary (bật/tắt)
- **Đầu ra Binary**: Điều khiển thiết bị đầu ra binary
- **Giá trị Binary**: Lưu trữ và quản lý giá trị binary

![Đầu vào Binary](images/binary-inputs.png)
![Đầu ra Binary](images/binary-outputs.png)
![Giá trị Binary](images/binary-values.png)

**Đối tượng Multi-state**
- **Đầu vào Multi-state**: Giám sát thiết bị đầu vào multi-state
- **Đầu ra Multi-state**: Điều khiển thiết bị đầu ra multi-state
- **Giá trị Multi-state**: Lưu trữ và quản lý giá trị multi-state

![Đầu vào Multi-state](images/multi-state-inputs.png)
![Đầu ra Multi-state](images/multi-state-outputs.png)
![Giá trị Multi-state](images/multi-state-values.png)

#### 👥 Quản Lý Người dùng
- Tạo, chỉnh sửa và xóa tài khoản người dùng
- Quyền dựa trên vai trò
- Theo dõi hoạt động người dùng

![Quản Lý Người dùng](images/user-management.png)

### Bắt Đầu Nhanh

1. **Khởi động Máy chủ API**
   ```bash
   cd xbacnet-api
   python run.py --port 8000
   ```

2. **Khởi động Giao diện Web**
   ```bash
   cd xbacnet-web
   npm install
   npm run dev
   ```

3. **Truy cập Giao diện**
   - Mở trình duyệt tại `http://localhost:3000`
   - Đăng nhập với: `administrator` / `!BACnetPro1`

### Stack Công nghệ
- **Frontend**: Vue 3 + Element Plus + ECharts
- **Backend**: Python Falcon REST API
- **Cơ sở dữ liệu**: MySQL
- **Xác thực**: Bảo mật dựa trên JWT

## Nhóm WeChat

![WeChat Group](qr_code_wechat_group.png)
