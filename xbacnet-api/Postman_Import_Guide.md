# XBACnet API Postman 导入指南

## 📋 概述

本文档介绍如何将 XBACnet API 导入到 Postman 工具中进行 API 测试。

## 🚀 快速开始

### 1. 下载 Postman
- 访问 [Postman 官网](https://www.postman.com/)
- 下载并安装 Postman 客户端
- 或者使用 Postman Web 版本

### 2. 导入 API 集合
1. 打开 Postman
2. 点击 "Import" 按钮
3. 选择 "Upload Files"
4. 选择 `XBACnet_API_Postman.json` 文件
5. 点击 "Import" 完成导入

### 3. 配置环境变量
导入后，你需要配置环境变量：

1. 在 Postman 中点击右上角的 "Environments" 标签
2. 创建新环境或编辑现有环境
3. 设置以下变量：
   - `baseUrl`: `http://localhost:8000` (默认值)

## 📁 API 集合结构

导入的 API 集合包含以下文件夹：

### 🔍 API Information
- **Get API Info**: 获取 API 信息和可用端点

### 🏥 Health & Statistics
- **Health Check**: 检查 API 和数据库健康状态
- **Get Statistics**: 获取数据库中的对象统计信息

### 📊 Analog Input Objects
- **List Analog Inputs**: 获取模拟输入对象列表
- **Create Analog Input**: 创建新的模拟输入对象
- **Get Analog Input by ID**: 根据 ID 获取模拟输入对象
- **Update Analog Input**: 更新模拟输入对象
- **Delete Analog Input**: 删除模拟输入对象

### 📈 Analog Output Objects
- **List Analog Outputs**: 获取模拟输出对象列表
- **Create Analog Output**: 创建新的模拟输出对象
- **Get Analog Output by ID**: 根据 ID 获取模拟输出对象
- **Update Analog Output**: 更新模拟输出对象
- **Delete Analog Output**: 删除模拟输出对象

### 🔘 Binary Input Objects
- **List Binary Inputs**: 获取二进制输入对象列表
- **Create Binary Input**: 创建新的二进制输入对象
- **Get Binary Input by ID**: 根据 ID 获取二进制输入对象
- **Update Binary Input**: 更新二进制输入对象
- **Delete Binary Input**: 删除二进制输入对象

### 🔘 Binary Output Objects
- **List Binary Outputs**: 获取二进制输出对象列表
- **Create Binary Output**: 创建新的二进制输出对象
- **Get Binary Output by ID**: 根据 ID 获取二进制输出对象
- **Update Binary Output**: 更新二进制输出对象
- **Delete Binary Output**: 删除二进制输出对象

### 🔢 Multi-state Input Objects
- **List Multi-state Inputs**: 获取多状态输入对象列表
- **Create Multi-state Input**: 创建新的多状态输入对象
- **Get Multi-state Input by ID**: 根据 ID 获取多状态输入对象
- **Update Multi-state Input**: 更新多状态输入对象
- **Delete Multi-state Input**: 删除多状态输入对象

### 🔢 Multi-state Output Objects
- **List Multi-state Outputs**: 获取多状态输出对象列表
- **Create Multi-state Output**: 创建新的多状态输出对象
- **Get Multi-state Output by ID**: 根据 ID 获取多状态输出对象
- **Update Multi-state Output**: 更新多状态输出对象
- **Delete Multi-state Output**: 删除多状态输出对象

### 📊 Analog Value Objects
- **List Analog Values**: 获取模拟值对象列表
- **Create Analog Value**: 创建新的模拟值对象
- **Get Analog Value by ID**: 根据 ID 获取模拟值对象
- **Update Analog Value**: 更新模拟值对象
- **Delete Analog Value**: 删除模拟值对象

### 🔘 Binary Value Objects
- **List Binary Values**: 获取二进制值对象列表
- **Create Binary Value**: 创建新的二进制值对象
- **Get Binary Value by ID**: 根据 ID 获取二进制值对象
- **Update Binary Value**: 更新二进制值对象
- **Delete Binary Value**: 删除二进制值对象

### 🔢 Multi-state Value Objects
- **List Multi-state Values**: 获取多状态值对象列表
- **Create Multi-state Value**: 创建新的多状态值对象

### 👥 User Management
- **List Users**: 获取用户列表
- **Create User**: 创建新用户
- **Get User by ID**: 根据ID获取用户
- **Update User**: 更新用户信息
- **Delete User**: 删除用户
- **User Login**: 用户身份验证
- **User Logout**: 用户退出登录
- **Get Multi-state Value by ID**: 根据 ID 获取多状态值对象
- **Update Multi-state Value**: 更新多状态值对象
- **Delete Multi-state Value**: 删除多状态值对象

## 🧪 测试步骤

### 1. 启动 XBACnet API 服务器
```bash
cd xbacnet-api
python run.py
```

### 2. 验证服务器运行
1. 在 Postman 中运行 "Health Check" 请求
2. 确认返回状态为 "healthy"

### 3. 测试 CRUD 操作
1. **创建对象**: 使用 "Create" 请求创建新对象
2. **获取对象**: 使用 "Get by ID" 请求获取创建的对象
3. **更新对象**: 使用 "Update" 请求修改对象属性
4. **删除对象**: 使用 "Delete" 请求删除对象

## 📝 请求示例

### 创建模拟输入对象
```json
{
  "object_identifier": 10001,
  "object_name": "Temperature_Sensor_1",
  "present_value": 25.5,
  "description": "Room temperature sensor",
  "status_flags": "0000",
  "event_state": "normal",
  "out_of_service": false,
  "units": "degreesCelsius",
  "cov_increment": 0.1
}
```

### 创建二进制输入对象
```json
{
  "object_identifier": 40001,
  "object_name": "Door_Sensor_1",
  "present_value": "active",
  "description": "Door open/close sensor",
  "status_flags": "0000",
  "event_state": "normal",
  "out_of_service": false,
  "polarity": "normal"
}
```

### 创建多状态输入对象
```json
{
  "object_identifier": 70001,
  "object_name": "HVAC_Mode_1",
  "present_value": 1,
  "description": "HVAC system mode",
  "status_flags": "0000",
  "event_state": "normal",
  "out_of_service": false,
  "number_of_states": 4,
  "state_text": ["Off", "Heat", "Cool", "Auto"]
}
```

### 用户管理示例

#### 创建用户
```json
{
  "name": "john_doe",
  "display_name": "John Doe",
  "email": "john.doe@example.com",
  "password": "securepassword123",
  "is_admin": false
}
```

#### 用户登录
```json
{
  "name": "john_doe",
  "password": "securepassword123"
}
```

#### 更新用户
```json
{
  "display_name": "John Smith",
  "email": "john.smith@example.com",
  "is_admin": true
}
```

#### 用户退出登录
```json
{
  "user_id": 1
}
```

或者使用用户名：
```json
{
  "name": "john_doe"
}
```

## 🔧 自定义配置

### 修改基础 URL
如果你的 API 服务器运行在不同的端口或主机上，可以修改环境变量：
- `baseUrl`: `http://your-server:port`

### 添加认证
如果 API 需要认证，可以在请求头中添加：
- `Authorization`: `Bearer your-token`

### 批量测试
可以使用 Postman 的 Collection Runner：
1. 选择集合
2. 点击 "Run" 按钮
3. 配置运行参数
4. 点击 "Run XBACnet API" 开始测试

### 自动化测试
Postman 集合包含预配置的测试脚本：
- 状态码检查
- 响应时间检查
- 响应格式验证

## 🎯 Postman 特色功能

### 1. 环境管理
- 支持多环境配置
- 开发、测试、生产环境切换
- 环境变量自动替换

### 2. 测试脚本
- 预请求脚本
- 测试后脚本
- 自动断言验证

### 3. 数据驱动测试
- CSV 数据文件导入
- 批量数据测试
- 参数化测试

### 4. 监控和报告
- 测试结果统计
- 性能监控
- 详细测试报告

## 🐛 常见问题

### 1. 连接失败
- 检查 API 服务器是否正在运行
- 确认端口号是否正确
- 检查防火墙设置

### 2. 404 错误
- 确认 API 路径是否正确
- 检查对象 ID 是否存在

### 3. 400 错误
- 检查请求体格式是否正确
- 确认必需字段是否已填写
- 验证数据类型是否正确

### 4. 500 错误
- 检查数据库连接
- 查看服务器日志
- 确认数据库表是否存在

## 📚 更多资源

- [XBACnet API 文档](./README.md)
- [Postman 官方文档](https://learning.postman.com/)
- [BACnet 协议规范](https://www.bacnet.org/)

## 🤝 支持

如果你在使用过程中遇到问题，请：
1. 查看本文档的常见问题部分
2. 检查 XBACnet API 服务器日志
3. 联系 XBACnet 团队获取支持

## 🔄 与 Apipost 的兼容性

这个 Postman 导出文件也可以导入到 Apipost 中使用：
1. 打开 Apipost
2. 选择 "导入" -> "导入文件"
3. 选择 `XBACnet_API_Postman.json` 文件
4. 完成导入后即可使用

两种工具都支持相同的 API 测试功能，你可以根据个人喜好选择使用。
