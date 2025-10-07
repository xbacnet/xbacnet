# XBACnet Web Management Interface

A modern Vue3-based web interface for managing XBACnet BACnet objects and system administration.

## Features

- 🎨 **Modern UI**: Built with Vue 3, Element Plus, and responsive design
- 🔐 **User Authentication**: Login/logout with role-based access control
- 📊 **Dashboard**: System overview with statistics and charts
- 🏗️ **BACnet Object Management**: Full CRUD operations for all BACnet object types
- 👥 **User Management**: Create, edit, and manage system users
- 🌙 **Dark/Light Theme**: Toggle between themes
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile devices
- 🔄 **Real-time Updates**: Live data refresh and status monitoring

## Supported BACnet Object Types

- **Analog Objects**: Input, Output, Value
- **Binary Objects**: Input, Output, Value  
- **Multi-state Objects**: Input, Output, Value
- **User Management**: Authentication and authorization

## Technology Stack

- **Frontend**: Vue 3, Vue Router, Pinia
- **UI Framework**: Element Plus
- **Charts**: ECharts
- **Build Tool**: Vite
- **Styling**: SCSS
- **HTTP Client**: Axios

## Prerequisites

- Node.js 16+ 
- npm or yarn
- XBACnet API server running on port 8000

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd xbacnet-web
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```

5. **Open browser**
   Navigate to `http://localhost:3000`

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# API Configuration
VITE_API_BASE_URL=http://localhost:8000/api

# Application Configuration
VITE_APP_TITLE=XBACnet Web Management
VITE_APP_DESCRIPTION=XBACnet Web Management Interface
```

### API Proxy

The development server is configured to proxy API requests to the XBACnet API server. Make sure the API server is running on `http://localhost:8000`.

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run format` - Format code with Prettier

## Project Structure

```
src/
├── components/          # Reusable Vue components
│   └── layout/         # Layout components (Header, Sidebar, etc.)
├── views/              # Page components
│   ├── auth/          # Authentication pages
│   ├── objects/       # BACnet object management pages
│   └── users/         # User management pages
├── stores/            # Pinia stores for state management
├── services/          # API services and HTTP clients
├── router/            # Vue Router configuration
├── assets/            # Static assets (images, styles)
└── utils/             # Utility functions
```

## Usage

### Authentication

1. **Login**: Use the default credentials or create a new user
   - Username: `administrator`
   - Password: `!BACnetPro1`

2. **User Management**: Admin users can create, edit, and delete users

### BACnet Object Management

1. **View Objects**: Browse all BACnet objects in the system
2. **Create Objects**: Add new BACnet objects with full property configuration
3. **Edit Objects**: Modify existing object properties
4. **Delete Objects**: Remove objects from the system
5. **Monitor Status**: View real-time object status and values

### Dashboard

- **Statistics**: Overview of system objects and users
- **Charts**: Visual representation of object distribution
- **Activity Log**: Recent system activities and changes

## API Integration

The web interface communicates with the XBACnet API server using RESTful endpoints:

- `GET /api/health` - Health check
- `GET /api/stats` - System statistics
- `GET /api/users` - User management
- `GET /api/analog-inputs` - Analog input objects
- `GET /api/analog-outputs` - Analog output objects
- `GET /api/binary-inputs` - Binary input objects
- And more...

## Development

### Adding New Features

1. **Create Components**: Add new Vue components in `src/components/`
2. **Add Routes**: Define new routes in `src/router/index.js`
3. **API Integration**: Add API methods in `src/services/api.js`
4. **State Management**: Use Pinia stores for complex state

### Styling

- Use SCSS variables for consistent theming
- Follow Element Plus design guidelines
- Ensure responsive design for all screen sizes

### Testing

```bash
# Run unit tests
npm run test

# Run e2e tests
npm run test:e2e
```

## Deployment

### Production Build

```bash
npm run build
```

The built files will be in the `dist/` directory.

### Docker Deployment

```bash
# Build Docker image
docker build -t xbacnet-web .

# Run container
docker run -p 3000:80 xbacnet-web
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Browser Support

- Chrome 88+
- Firefox 85+
- Safari 14+
- Edge 88+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Contact the development team

## Changelog

### v1.0.0
- Initial release
- Vue 3 + Element Plus interface
- BACnet object management
- User authentication
- Dashboard with statistics
- Responsive design
- Dark/light theme support
