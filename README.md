# Portal Automation System

A robust Flask web application for automating IKH (Izin Kerja Harian) and IKK (Izin Kerja Khusus) work permit processes.

## Features

- **Web Interface**: Clean, responsive dashboard for managing personnel data and automation
- **IKH Automation**: Automated daily work permit processing
- **IKK Automation**: Automated special work permit processing for API, Ruang Terbatas, and Ketinggian categories
- **CSV Management**: Upload and manage personnel data files
- **Real-time Monitoring**: Live log monitoring and process status tracking
- **Multi-shift Support**: Support for different work shifts
- **Robust Error Handling**: Comprehensive error handling and recovery mechanisms

## Architecture

### Core Components

1. **Flask Application** (`app.py`)
   - Main web server with RESTful API endpoints
   - Session management and file handling
   - Process orchestration and monitoring
   - Caching for improved performance

2. **IKH Automation** (`static/ikh_automation.py`)
   - Daily work permit automation
   - Personnel data processing
   - Date and shift management

3. **IKK Automation** (`static/ikk_automation.py`)
   - Special work permit automation
   - Category-specific processing (API, Ruang Terbatas, Ketinggian)
   - Certificate validation and management

### Key Improvements

- **Removed excessive debugging code** that was cluttering the logs
- **Consolidated duplicate functions** for better maintainability
- **Implemented proper error handling** with graceful degradation
- **Added caching mechanisms** for improved performance
- **Streamlined process management** with thread pools
- **Enhanced security** with proper session handling
- **Improved code organization** with clear separation of concerns

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ibradan/Portaliano.git
   cd Portal
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # or
   .venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**
   ```bash
   playwright install chromium
   ```

## Usage

### Starting the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

### Environment Variables

- `FLASK_ENV`: Set to `production` for production deployment
- `SECRET_KEY`: Secret key for session management
- `PORT`: Port number (default: 5000)
- `MAX_WORKERS`: Maximum thread pool workers (default: 4)
- `UPLOAD_FOLDER`: Upload directory (default: uploads)
- `MAX_FILE_SIZE`: Maximum file size in bytes (default: 5MB)

### CSV File Format

Personnel CSV files should contain the following columns:
- `Nama`: Personnel name
- `Nomor`: Personnel ID/NIK
- `Sertif`: Certificate number (for IKK)
- `Expsertif`: Certificate expiry date (for IKK)

### API Endpoints

- `GET /dashboard`: Main dashboard
- `GET /ikh`: IKH automation page
- `GET /ikk`: IKK categories page
- `GET /ikk/api`: IKK API automation
- `GET /ikk/ruang-terbatas`: IKK Ruang Terbatas automation
- `GET /ikk/ketinggian`: IKK Ketinggian automation
- `POST /upload`: Upload CSV file
- `POST /process`: Start automation process
- `POST /stop_process`: Stop running process
- `GET /get_log`: Get automation logs
- `GET /check_completion`: Check process status

## Docker Deployment

```bash
# Build image
docker build -t portal-automation .

# Run container
docker run -p 5000:5000 portal-automation

# Or use docker-compose
docker-compose up -d
```

## File Structure

```
Portal/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose configuration
├── static/
│   ├── ikh_automation.py      # IKH automation script
│   ├── ikk_automation.py      # IKK automation script
│   └── style.css             # CSS styles
├── templates/                 # HTML templates
│   ├── dashboard.html
│   ├── ikh.html
│   ├── ikk_*.html
│   └── ...
├── uploads/                   # Upload directory
├── personnel_list_*.csv       # Personnel data files
└── README.md                  # This file
```

## Performance Optimizations

1. **Caching**: LRU cache for CSV data and file listings
2. **Thread Pool**: Concurrent process execution
3. **Resource Management**: Proper cleanup and signal handling
4. **Memory Efficiency**: Limited CSV row loading (50 rows max for preview)
5. **Connection Pooling**: Optimized database connections

## Security Features

1. **File Upload Validation**: Secure filename handling and type checking
2. **Session Management**: HTTP-only cookies with proper expiration
3. **Input Sanitization**: Protection against injection attacks
4. **Error Handling**: No sensitive information in error messages
5. **Process Isolation**: Sandboxed automation processes

## Monitoring and Logging

- **Structured Logging**: Consistent log format with timestamps
- **Process Monitoring**: Real-time status tracking
- **Error Screenshots**: Automatic error capture for debugging
- **Performance Metrics**: Response time and resource usage tracking

## Troubleshooting

### Common Issues

1. **Playwright Installation**
   ```bash
   playwright install --with-deps chromium
   ```

2. **Permission Issues**
   ```bash
   chmod +x static/*.py
   ```

3. **Port Already in Use**
   ```bash
   export PORT=8000
   python app.py
   ```

### Debug Mode

Set `FLASK_ENV=development` for detailed error messages and auto-reload.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please create an issue in the GitHub repository.
