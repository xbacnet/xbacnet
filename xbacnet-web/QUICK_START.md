# XBACnet Web Management Interface - Quick Start Guide

## 🚀 快速开始

### 1. 环境要求
- Node.js 16+
- npm 或 yarn
- XBACnet API 服务器运行在端口 8000

### 2. 安装和启动

```bash
# 克隆项目
cd xbacnet-web

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

或者使用启动脚本：
```bash
./start.sh
```

### 3. 访问应用
- 打开浏览器访问: http://localhost:3000
- 默认登录凭据:
  - 用户名: `administrator`
  - 密码: `!BACnetPro1`

## 📋 功能特性

### 🎛️ 仪表板
- 系统概览和统计信息
- 对象分布图表
- 系统状态监控
- 最近活动日志

### 🏗️ BACnet 对象管理
- **模拟对象**: 输入、输出、值
- **二进制对象**: 输入、输出、值  
- **多状态对象**: 输入、输出、值
- 完整的 CRUD 操作
- 实时状态监控

### 👥 用户管理
- 用户创建和编辑
- 角色权限管理
- 密码安全处理
- 用户活动跟踪

### 🎨 界面特性
- 响应式设计
- 深色/浅色主题切换
- 现代化 UI 组件
- 实时数据更新

## 🔧 开发

### 项目结构
```
src/
├── components/     # 可复用组件
├── views/         # 页面组件
├── stores/        # 状态管理
├── services/      # API 服务
├── router/        # 路由配置
├── assets/        # 静态资源
└── utils/         # 工具函数
```

### 常用命令
```bash
npm run dev        # 开发服务器
npm run build      # 生产构建
npm run preview    # 预览构建
npm run lint       # 代码检查
npm run format     # 代码格式化
```

### 环境配置
复制 `env.example` 到 `.env` 并修改配置：
```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_APP_TITLE=XBACnet Web Management
```

## 🐳 Docker 部署

### 构建镜像
```bash
docker build -t xbacnet-web .
```

### 运行容器
```bash
docker run -p 3000:3000 xbacnet-web
```

## 🔗 API 集成

Web 界面通过以下 API 端点与后端通信：

- `GET /api/health` - 健康检查
- `GET /api/stats` - 系统统计
- `GET /api/users` - 用户管理
- `GET /api/analog-inputs` - 模拟输入对象
- `GET /api/analog-outputs` - 模拟输出对象
- `GET /api/binary-inputs` - 二进制输入对象
- 更多端点...

## 🛠️ 故障排除

### 常见问题

1. **API 连接失败**
   - 确保 XBACnet API 服务器运行在端口 8000
   - 检查防火墙设置
   - 验证 API 服务器状态

2. **登录失败**
   - 检查默认凭据
   - 确认用户账户存在
   - 查看浏览器控制台错误

3. **页面加载缓慢**
   - 检查网络连接
   - 清除浏览器缓存
   - 查看 API 响应时间

### 调试模式
```bash
# 启用详细日志
VITE_LOG_LEVEL=debug npm run dev
```

## 📞 支持

- 查看完整文档: [README.md](./README.md)
- 报告问题: GitHub Issues
- 联系开发团队

## 🔄 更新日志

### v1.0.0
- 初始版本发布
- Vue 3 + Element Plus 界面
- BACnet 对象管理
- 用户认证系统
- 响应式设计
- 深色/浅色主题
