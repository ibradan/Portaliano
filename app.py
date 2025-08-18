from flask import Flask, render_template, request, redirect, url_for, jsonify, session, send_file
import csv
import subprocess
import os
import sys
import uuid
import logging
import signal
import datetime
from werkzeug.utils import secure_filename
from functools import lru_cache
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from datetime import date
import json
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production-' + str(uuid.uuid4()))
app.config.update(
    UPLOAD_FOLDER=os.environ.get('UPLOAD_FOLDER', 'uploads'),
    MAX_CONTENT_LENGTH=int(os.environ.get('MAX_FILE_SIZE', 5 * 1024 * 1024)),  # 5MB
    ALLOWED_EXTENSIONS={'csv'},
    JSON_SORT_KEYS=False,
    SESSION_COOKIE_SECURE=os.environ.get('FLASK_ENV') == 'production',
    SESSION_COOKIE_HTTPONLY=True,
    PERMANENT_SESSION_LIFETIME=3600  # 1 hour
)

# Thread pool for automation processes
executor = ThreadPoolExecutor(max_workers=int(os.environ.get('MAX_WORKERS', 4)))
current_process = None

def cleanup_resources():
    """Cleanup resources on shutdown."""
    try:
        executor.shutdown(wait=True)
        logger.info("Resources cleaned up successfully")
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")

def signal_handler(sig, frame):
    logger.info("Received shutdown signal, cleaning up...")
    cleanup_resources()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def allowed_file(filename):
    """Check if uploaded file has allowed extension."""
    return ('.' in filename and 
            filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS'])

def ensure_upload_dir():
    """Ensure upload directory exists."""
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@lru_cache(maxsize=32)
def get_csv_files_cached(cache_key):
    """Get available CSV files with caching."""
    csv_files = []
    uploads_dir = app.config['UPLOAD_FOLDER']
    
    # Check for specific category files
    category_files = [
        ('personnel_list_ALL.csv', 'IKH - All Personnel', 'ikh'),
        ('personnel_list_IA.csv', 'IKK Api (IA)', 'ikk-api'),
        ('personnel_list_IR.csv', 'IKK Ruang Terbatas (IR)', 'ikk-ruang-terbatas'),
        ('personnel_list_IK.csv', 'IKK Ketinggian (IK)', 'ikk-ketinggian'),
        ('personnel_list.csv', 'Default Personnel List', 'default')
    ]
    
    for file_path, display_name, category in category_files:
        if os.path.exists(file_path):
            csv_files.append({
                'name': display_name,
                'path': file_path,
                'category': category
            })
    
    # Check uploads directory
    ensure_upload_dir()
    try:
        for entry in os.scandir(uploads_dir):
            if entry.is_file() and entry.name.endswith('.csv'):
                csv_files.append({
                    'name': entry.name,
                    'path': os.path.join(uploads_dir, entry.name),
                    'category': 'uploaded'
                })
    except OSError:
        pass
    
    return csv_files

def get_available_csv_files():
    """Get available CSV files with cache invalidation."""
    cache_key = int(time.time() / 30)  # Cache for 30 seconds
    return get_csv_files_cached(cache_key)

def get_csv_path():
    """Get current CSV path from session with fallback."""
    csv_path = session.get('csv_path')
    if csv_path and os.path.exists(csv_path):
        return csv_path
    
    # Fallback to default
    default_csv = 'personnel_list.csv'
    if os.path.exists(default_csv):
        session['csv_path'] = default_csv
        return default_csv
    
    return None

@lru_cache(maxsize=64)
def read_csv_data_cached(csv_path, file_mtime):
    """Read CSV data with caching based on file modification time."""
    try:
        with open(csv_path, 'r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
            return data[:50]  # Limit to 50 rows for performance
    except Exception as e:
        logger.error(f"Error reading CSV {csv_path}: {e}")
        return []

def read_csv_data(csv_path):
    """Read CSV data with caching."""
    if not csv_path or not os.path.exists(csv_path):
        return []
    
    try:
        file_mtime = int(os.path.getmtime(csv_path))
        return read_csv_data_cached(csv_path, file_mtime)
    except Exception as e:
        logger.error(f"Error getting CSV data: {e}")
        return []

def get_category_csv_path(category):
    """Get CSV path for specific category."""
    category_mapping = {
        'ikh': 'personnel_list_ALL.csv',
        'ikk-api': 'personnel_list_IA.csv',
        'ikk-ruang-terbatas': 'personnel_list_IR.csv',
        'ikk-ketinggian': 'personnel_list_IK.csv'
    }
    
    csv_file = category_mapping.get(category)
    if csv_file and os.path.exists(csv_file):
        return csv_file
    return None

# Routes
@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    """Dashboard with CSV preview."""
    csv_path = get_csv_path()
    csv_data = read_csv_data(csv_path) if csv_path else []
    available_files = get_available_csv_files()
    current_file = next((f['name'] for f in available_files if f['path'] == csv_path), 'No file selected')
    
    return render_template('dashboard.html', 
                         csv_data=csv_data, 
                         available_files=available_files, 
                         current_file=current_file)

@app.route('/ikh')
def ikh():
    """IKH automation page."""
    csv_path = get_category_csv_path('ikh')
    if csv_path:
        session['csv_path'] = csv_path
    
    csv_data = read_csv_data(csv_path) if csv_path else []
    available_files = get_available_csv_files()
    current_file = next((f['name'] for f in available_files if f['path'] == csv_path), 'No file selected')
    today_date = date.today().strftime('%Y-%m-%d')
    
    return render_template('ikh.html', 
                         csv_data=csv_data, 
                         available_files=available_files, 
                         current_file=current_file, 
                         today_date=today_date)

@app.route('/ikk')
def ikk_categories():
    """IKK categories page."""
    return render_template('ikk_categories.html')

@app.route('/ikk/api')
def ikk_api():
    """IKK Api automation page."""
    csv_path = get_category_csv_path('ikk-api')
    if csv_path:
        session['csv_path'] = csv_path
    
    csv_data = read_csv_data(csv_path) if csv_path else []
    today_date = date.today().strftime('%Y-%m-%d')
    
    return render_template('ikk_api.html', 
                         csv_data=csv_data, 
                         today_date=today_date)

@app.route('/ikk/ruang-terbatas')
def ikk_ruang_terbatas():
    """IKK Ruang Terbatas automation page."""
    csv_path = get_category_csv_path('ikk-ruang-terbatas')
    if csv_path:
        session['csv_path'] = csv_path
    
    csv_data = read_csv_data(csv_path) if csv_path else []
    today_date = date.today().strftime('%Y-%m-%d')
    
    return render_template('ikk_ruang_terbatas.html', 
                         csv_data=csv_data, 
                         today_date=today_date)

@app.route('/ikk/ketinggian')
def ikk_ketinggian():
    """IKK Ketinggian automation page."""
    csv_path = get_category_csv_path('ikk-ketinggian')
    if csv_path:
        session['csv_path'] = csv_path
    
    csv_data = read_csv_data(csv_path) if csv_path else []
    today_date = date.today().strftime('%Y-%m-%d')
    
    return render_template('ikk_ketinggian.html', 
                         csv_data=csv_data, 
                         today_date=today_date)

@app.route('/upload', methods=['POST'])
def upload():
    """Handle file upload."""
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file provided'}), 400
    
    file = request.files['file']
    category = request.form.get('category', 'uploaded')
    
    if not file.filename or not allowed_file(file.filename):
        return jsonify({'status': 'error', 'message': 'Invalid file type. Please upload a CSV file.'}), 400
    
    try:
        ensure_upload_dir()
        filename = secure_filename(file.filename)
        
        # Handle category-specific uploads
        if category in ['ikk-api', 'ikk-ruang-terbatas', 'ikk-ketinggian']:
            category_mapping = {
                'ikk-api': 'personnel_list_IA.csv',
                'ikk-ruang-terbatas': 'personnel_list_IR.csv',
                'ikk-ketinggian': 'personnel_list_IK.csv'
            }
            file_path = category_mapping[category]
        elif category == 'ikh':
            file_path = 'personnel_list_ALL.csv'
        else:
            unique_name = f"{uuid.uuid4().hex}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
        
        file.save(file_path)
        session['csv_path'] = file_path
        
        # Clear caches
        get_csv_files_cached.cache_clear()
        read_csv_data_cached.cache_clear()
        
        return jsonify({'status': 'success', 'message': 'File uploaded successfully'})
            
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        return jsonify({'status': 'error', 'message': 'Upload failed'}), 500

@app.route('/select_csv', methods=['POST'])
def select_csv():
    """Select CSV file."""
    try:
        data = request.get_json()
        selected_path = data.get('csv_path') if data else None
        
        if not selected_path:
            return jsonify({'status': 'error', 'message': 'No file path provided'}), 400
        
        available_files = get_available_csv_files()
        valid_paths = [f['path'] for f in available_files]
        
        if selected_path in valid_paths:
            session['csv_path'] = selected_path
            read_csv_data_cached.cache_clear()
            return jsonify({'status': 'success', 'message': 'CSV file selected successfully'})
        else:
            return jsonify({'status': 'error', 'message': 'Invalid CSV file selected'}), 400
    except Exception as e:
        logger.error(f"CSV selection failed: {e}")
        return jsonify({'status': 'error', 'message': 'Selection failed'}), 500

def clear_log_file():
    """Clear automation log file."""
    try:
        open('automation.log', 'w').close()
    except Exception:
        pass

def run_automation_process(script_path, csv_path, selected_indices, selected_date, selected_shift, mode):
    """Run automation process."""
    global current_process
    try:
        env = os.environ.copy()
        env['DISPLAY'] = os.environ.get('DISPLAY', ':0')
        env['PLAYWRIGHT_HEADLESS'] = os.environ.get('PLAYWRIGHT_HEADLESS', 'true')
        env['PYTHONUNBUFFERED'] = '1'
        
        # Build command based on script type
        if 'ikk_automation.py' in script_path:
            category_map = {
                'IKK-API': 'IA',
                'IKK-RUANG-TERBATAS': 'IR', 
                'IKK-KETINGGIAN': 'IK'
            }
            category = category_map.get(mode, 'IA')
            
            # Use today's date if no selected_date provided
            work_date = selected_date if selected_date else datetime.datetime.now().strftime('%d/%m/%Y')
            
            process_args = [
                'python3', 
                script_path, 
                category,
                work_date,
                'MELTING REPAIR',
                str(selected_shift or 1)
            ]
            if selected_indices and len(selected_indices) > 0:
                process_args.extend([str(i) for i in selected_indices])
        else:
            # IKH script format
            process_args = ['python3', script_path, csv_path]
            
            if selected_indices and len(selected_indices) > 0:
                process_args.extend([str(i) for i in selected_indices])
            
            if selected_date:
                process_args.append(f"--date={selected_date}")
                
            if selected_shift:
                process_args.append(f"--shift={selected_shift}")
        
        logger.info(f"Starting {mode} automation with command: {' '.join(process_args)}")
        
        # Initialize log with detailed information
        log_path = 'automation.log'
        with open(log_path, 'w', encoding='utf-8') as log_file:
            log_file.write(f"🚀 {mode} AUTOMATION STARTED\n")
            log_file.write("="*50 + "\n")
            log_file.write(f"📂 Category: {category if 'ikk_automation.py' in script_path else 'IKH'}\n")
            log_file.write(f"📄 CSV File: {csv_path}\n")
            log_file.write(f"📅 Date: {selected_date}\n")
            log_file.write(f"⏰ Shift: {selected_shift}\n")
            log_file.write(f"🔧 Script: {script_path}\n")
            log_file.write(f"💻 Command: {' '.join(process_args)}\n")
            log_file.write("="*50 + "\n\n")
            log_file.flush()
        
        # Start process with line buffering for real-time output
        with open(log_path, 'a', encoding='utf-8') as log_file:
            current_process = subprocess.Popen(
                process_args, 
                stdout=log_file, 
                stderr=subprocess.STDOUT, 
                text=True, 
                env=env,
                bufsize=1,  # Line buffering for real-time output
                universal_newlines=True
            )
            
            try:
                return_code = current_process.wait(timeout=1800)  # 30 minutes
                
                if return_code == 0:
                    log_file.write(f"\n🎉 {mode} COMPLETED SUCCESSFULLY!\n")
                    log_file.write("="*50 + "\n")
                    log_file.write(f"✅ Process finished with exit code: {return_code}\n")
                    log_file.write(f"⏰ Completion time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    log_file.write("="*50 + "\n")
                else:
                    log_file.write(f"\n❌ PROCESS FAILED!\n")
                    log_file.write("="*50 + "\n")
                    log_file.write(f"🔥 Exit code: {return_code}\n")
                    log_file.write(f"⏰ Failure time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    log_file.write("="*50 + "\n")
                    
            except subprocess.TimeoutExpired:
                if current_process:
                    current_process.terminate()
                    try:
                        current_process.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        current_process.kill()
                        
                log_file.write(f"\n⏰ PROCESS TIMED OUT!\n")
                log_file.write("="*50 + "\n")
                log_file.write(f"🕐 Timeout after 30 minutes\n")
                log_file.write(f"⏰ Timeout time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                log_file.write("="*50 + "\n")
                
    except Exception as e:
        logger.error(f"Automation process error: {e}")
        try:
            with open('automation.log', 'a', encoding='utf-8') as log_file:
                log_file.write(f"\nError: {str(e)}\n")
        except:
            pass
    finally:
        if current_process and current_process.poll() is None:
            try:
                current_process.terminate()
            except:
                pass

@app.route('/process', methods=['POST'])
def process():
    """Process automation request."""
    try:
        clear_log_file()
        
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'No data provided'}), 400
        
        selected_rows = data.get('selected_rows', [])
        selected_indices = data.get('selected_indices', [])
        mode = data.get('mode', 'IKH')
        selected_date = data.get('selected_date', '')
        selected_shift = data.get('selected_shift', 1)
        
        # Determine CSV path based on mode
        if mode.startswith('IKK-'):
            category = mode.replace('IKK-', '').lower().replace('_', '-')
            csv_path = get_category_csv_path(f'ikk-{category}')
        elif mode == 'IKH':
            csv_path = get_category_csv_path('ikh')
        else:
            csv_path = get_csv_path()
        
        # Validation
        if not selected_rows and not selected_indices:
            return jsonify({'status': 'error', 'message': 'No rows selected'}), 400
        
        if not csv_path or not os.path.exists(csv_path):
            return jsonify({'status': 'error', 'message': 'No valid CSV file found'}), 400
        
        script_path = f"static/{'ikh' if mode == 'IKH' else 'ikk'}_automation.py"
        if not os.path.exists(script_path):
            return jsonify({'status': 'error', 'message': f'Automation script not found: {script_path}'}), 500
        
        # Submit to thread pool
        executor.submit(run_automation_process, script_path, csv_path, selected_indices, selected_date, selected_shift, mode)
        
        return jsonify({'status': 'success', 'message': 'Automation started successfully'}), 200
        
    except Exception as e:
        logger.error(f"Process start failed: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to start automation'}), 500

@app.route('/stop_process', methods=['POST'])
def stop_process():
    """Stop the currently running automation process."""
    global current_process
    try:
        if current_process and current_process.poll() is None:
            current_process.terminate()
            try:
                current_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                current_process.kill()
                current_process.wait()
            
            logger.info("Automation process stopped by user")
            
            try:
                with open('automation.log', 'a', encoding='utf-8') as log_file:
                    log_file.write('\nProcess stopped by user\n')
            except Exception as e:
                logger.error(f"Error writing stop message: {e}")
            
            return jsonify({'status': 'success', 'message': 'Process stopped successfully'})
        else:
            return jsonify({'status': 'info', 'message': 'No process running'})
    except Exception as e:
        logger.error(f"Error stopping process: {e}")
        return jsonify({'status': 'error', 'message': f'Error stopping process: {str(e)}'}), 500

@app.route('/get_log', methods=['GET'])
def get_log():
    """Get automation log."""
    try:
        with open('automation.log', 'r', encoding='utf-8') as log_file:
            content = log_file.read()
            return content if content else 'Starting...'
    except FileNotFoundError:
        return 'Waiting...'
    except Exception as e:
        logger.error(f"Error reading log: {e}")
        return 'Error reading log'

# --- Notification Parsing Helper ---
def parse_notification_from_log(log_content):
    notification_message = None
    for line in log_content.splitlines():
        if "Notification message:" in line:
            notification_message = line.split("Notification message:",1)[-1].strip()
        elif "SUCCESS NOTIFICATION DETECTED" in line and not notification_message:
            notification_message = "IKK telah berhasil disubmit"
    # Fallback: jika ada baris 'IKK-API COMPLETED SUCCESSFULLY!' tapi tidak ada notifikasi lain
    if not notification_message:
        for line in log_content.splitlines():
            if "IKK-API COMPLETED SUCCESSFULLY!" in line:
                notification_message = "IKK-API COMPLETED SUCCESSFULLY!"
    return notification_message

@app.route('/check_completion', methods=['GET'])
def check_completion():
    """Check if automation process is completed."""
    try:
        # Check process status file
        status_file = "process_status.json"
        if os.path.exists(status_file):
            with open(status_file, 'r') as f:
                status = json.load(f)
            return jsonify(status)
        

        # Fallback: check automation log
        log_file = "automation.log"
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()

            completion_indicators = [
                "completed successfully",
                "AUTOMATION COMPLETE",
                "SUCCESS",
                "BERHASIL"
            ]
            is_completed = any(indicator in content for indicator in completion_indicators)

            # Parse notification message (IKK)
            notification_message = parse_notification_from_log(content)

            return jsonify({
                "process_running": False,
                "process_completed": is_completed,
                "completion_time": time.time() if is_completed else None,
                "last_update": time.time(),
                "notification_message": notification_message
            })

        return jsonify({
            "process_running": False,
            "process_completed": False,
            "completion_time": None,
            "last_update": time.time(),
            "notification_message": None
        })
        
    except Exception as e:
        logger.error(f"Error checking completion: {e}")
        return jsonify({
            "error": str(e),
            "process_running": False,
            "process_completed": False
        }), 500

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'status': 'error', 'message': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

if __name__ == '__main__':
    ensure_upload_dir()
    
    app.run(
        host='0.0.0.0', 
        port=int(os.environ.get('PORT', 5000)), 
        debug=os.environ.get('FLASK_ENV') == 'development',
        threaded=True
    )
