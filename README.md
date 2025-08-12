# Portaliano - Work Permit Automation System

A clean, efficient Flask web application for automating IKH (Izin Kerja Harian) and IKK (Izin Kerja Khusus) work permit processes.

## ✨ Features

- **🌐 Web Interface**: Clean, responsive dashboard for managing personnel data and automation
- **📋 IKH Automation**: Automated daily work permit processing
- **🔧 IKK Automation**: Automated special work permit processing (API, Ruang Terbatas, Ketinggian)
- **📊 CSV Management**: Upload and manage personnel data files
- **📡 Real-time Monitoring**: Live log monitoring and process status tracking
- **⏰ Multi-shift Support**: Support for different work shifts (1, 2, 3)
- **🛡️ Robust Error Handling**: Comprehensive error handling and recovery

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git

### Installation

1. **Clone and setup**
   ```bash
   git clone https://github.com/ibradan/Portaliano.git
   cd Portaliano
   ```

2. **Run with Virtual Environment (Recommended)**
   ```bash
   ./start_portal_venv.sh
   ```

   This will automatically:
   - Create virtual environment if not exists
   - Install all dependencies
   - Install Playwright browser
   - Start the Flask application

3. **Manual Setup (Alternative)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   playwright install chromium
   python app.py
   ```

### Access
Open your browser to `http://localhost:5000`

## 🎛️ Browser Configuration

### Quick Mode Switching
```bash
# Show browser window (for development/debugging)
./switch_browser_mode.sh visible

# Hide browser window (for production/server)
./switch_browser_mode.sh headless

# Check current configuration
./switch_browser_mode.sh status
```

### Manual Configuration
Edit `browser_config.py`:
- `HEADLESS_MODE = False` → Browser visible
- `HEADLESS_MODE = True` → Browser hidden

## 📁 Project Structure

```
Portaliano/
├── 🐍 app.py                     # Main Flask application
├── 📋 requirements.txt           # Python dependencies  
├── 🐳 Dockerfile                # Docker configuration
├── 🐳 docker-compose.yml        # Docker Compose setup
├── 🚀 start_portal_venv.sh       # Main launcher script
├── ✅ check_venv.py              # Environment verification
├── 🎛️ browser_config.py          # Browser mode configuration
├── 🔄 switch_browser_mode.sh     # Quick browser mode switcher
├── 📖 VENV_SETUP_GUIDE.md       # Setup documentation
├── 📊 personnel_list_*.csv       # Personnel data files
├── 🔧 portaliano.service         # Systemd service file
├── 📁 static/
│   ├── 🤖 ikh_automation.py      # IKH automation script
│   ├── 🤖 ikk_automation.py      # IKK automation script  
│   └── 🎨 style.css             # Web interface styles
├── 📁 templates/                 # HTML templates
│   ├── 🏠 dashboard.html         # Main dashboard
│   ├── 📋 ikh.html              # IKH automation page
│   ├── 🔧 ikk_*.html            # IKK automation pages
│   └── 📊 table.html            # Data display
├── 📁 uploads/                   # CSV upload directory
└── 📁 venv/                     # Virtual environment
```

## 🔧 Core Components

### Browser Configuration (`browser_config.py`)
- Centralized browser mode control
- Easy switching between visible/headless
- Configurable browser arguments and speed
- Development/Production presets

### Flask Application (`app.py`)
- RESTful API endpoints
- Session management and file handling  
- Process orchestration and monitoring
- Real-time logging system

### IKH Automation (`static/ikh_automation.py`)
- Daily work permit automation
- Personnel data processing
- Multi-shift support (Shift 1, 2, 3)
- Browser automation with Playwright

### IKK Automation (`static/ikk_automation.py`)  
- Special work permit automation
- Three categories: API, Ruang Terbatas, Ketinggian
- Certificate validation and expiry checking
- Dynamic calendar navigation

## 📊 CSV File Format

Personnel CSV files should contain:
- `Nama`: Personnel name
- `Nomor`: Personnel ID/NIK  
- `Sertif`: Certificate number (for IKK)
- `Expsertif`: Certificate expiry date (for IKK, format: DD/MM/YYYY)

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/dashboard` | GET | Main dashboard |
| `/ikh` | GET | IKH automation page |
| `/ikk/api` | GET | IKK API automation |
| `/ikk/ruang-terbatas` | GET | IKK Confined Space |
| `/ikk/ketinggian` | GET | IKK Height Work |
| `/upload` | POST | Upload CSV file |
| `/process` | POST | Start automation |
| `/stop_process` | POST | Stop process |
| `/get_log` | GET | Get real-time logs |

## 🐳 Docker Deployment

```bash
# Quick start with Docker Compose
docker-compose up -d

# Manual Docker build
docker build -t portaliano .
docker run -p 5000:5000 portaliano
```

## ⚙️ Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | `development` | Flask environment |
| `PORT` | `5000` | Application port |
| `PLAYWRIGHT_HEADLESS` | `false` | Browser visibility |

## 🔍 Monitoring & Troubleshooting

### Check Environment
```bash
python check_venv.py
```

### View Logs
- Real-time logs available in web interface
- Check terminal output for detailed information

### Common Issues

1. **Playwright not installed**
   ```bash
   source venv/bin/activate
   playwright install chromium
   ```

2. **Permission denied**
   ```bash
   chmod +x start_portal_venv.sh
   ```

3. **Port already in use**
   ```bash
   export PORT=8080
   ./start_portal_venv.sh
   ```

## 🎯 Recent Improvements

✅ **Clean Virtual Environment**: Isolated Python dependencies  
✅ **User Package Cleanup**: Removed conflicting system packages  
✅ **Simplified Structure**: Removed unnecessary files and scripts  
✅ **Browser Visibility**: Set headless=False for development  
✅ **Documentation**: Comprehensive setup guides  

## 📝 License

MIT License - See LICENSE file for details

## 💬 Support

For issues and questions, please create an issue in the GitHub repository.
