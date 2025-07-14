from flask import Flask, render_template, request, redirect, url_for, jsonify, session, send_file

import csv
import subprocess
import os
import sys
import uuid
import logging
import signal
from werkzeug.utils import secure_filename
from functools import lru_cache
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from datetime import date
import json
import time

# Ultra-fast logging: WARNING level only for production speed
logging.basicConfig(
    level=logging.WARNING,  # Reduced from INFO for speed
    format='%(levelname)s - %(message)s',  # Simplified format
    handlers=[
        logging.StreamHandler(sys.stdout)  # Removed file handler for speed
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Robust configuration with environment variable support
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production-' + str(uuid.uuid4()))
app.config.update(
    UPLOAD_FOLDER=os.environ.get('UPLOAD_FOLDER', 'uploads'),
    MAX_CONTENT_LENGTH=int(os.environ.get('MAX_FILE_SIZE', 5 * 1024 * 1024)),  # 5MB default
    ALLOWED_EXTENSIONS={'csv'},
    JSON_SORT_KEYS=False,
    JSONIFY_PRETTYPRINT_REGULAR=False,
    SEND_FILE_MAX_AGE_DEFAULT=31536000,  # 1 year cache for static files
    SESSION_COOKIE_SECURE=os.environ.get('FLASK_ENV') == 'production',
    SESSION_COOKIE_HTTPONLY=True,
    PERMANENT_SESSION_LIFETIME=3600,  # 1 hour
    # Ultra-fast Flask optimizations
    TEMPLATES_AUTO_RELOAD=False,  # Disable template auto-reload
    EXPLAIN_TEMPLATE_LOADING=False,  # Disable template debugging
    PREFERRED_URL_SCHEME='http',  # Faster than https in dev
    PROPAGATE_EXCEPTIONS=False  # Faster error handling
)


# Ultra-optimized thread pool: auto-scale with CPU, min 4, max 16
import multiprocessing
cpu_count = max(4, min(16, multiprocessing.cpu_count() * 2))
executor = ThreadPoolExecutor(max_workers=int(os.environ.get('MAX_WORKERS', cpu_count)))

# Global variable to track current automation process
current_process = None

def cleanup_resources():
    """Cleanup resources on shutdown."""
    try:
        executor.shutdown(wait=True)  # Removed timeout parameter for compatibility
        logger.info("Resources cleaned up successfully")
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")

# Register cleanup on shutdown
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

@lru_cache(maxsize=32)  # Increased cache size
def get_csv_files_cached(cache_key):
    """Cached CSV file discovery with cache key for invalidation. Ultra-fast with scandir."""
    csv_files = []
    uploads_dir = app.config['UPLOAD_FOLDER']
    
    # Pre-build file paths for speed
    ikk_files = [
        ('personnel_list_IA.csv', 'IKK Api (IA)', 'ikk-api'),
        ('personnel_list_IR.csv', 'IKK Ruang Terbatas (IR)', 'ikk-ruang-terbatas'),
        ('personnel_list_IK.csv', 'IKK Ketinggian (IK)', 'ikk-ketinggian')
    ]
    
    # Check for IKH personnel list first
    if os.path.exists('personnel_list_ALL.csv'):
        csv_files.append({'name': 'personnel_list_ALL.csv (IKH - All Personnel)', 'path': 'personnel_list_ALL.csv', 'category': 'ikh'})
    
    # Check default CSV  
    if os.path.exists('personnel_list.csv'):
        csv_files.append({'name': 'personnel_list.csv (Default)', 'path': 'personnel_list.csv', 'category': 'default'})
    
    # Batch check IKK files using list comprehension (faster)
    csv_files.extend([
        {'name': name, 'path': file, 'category': category}
        for file, name, category in ikk_files if os.path.exists(file)
    ])
    
    # Ultra-fast uploads directory scan
    ensure_upload_dir()
    try:
        # Use list comprehension for speed
        upload_files = [
            {'name': entry.name.replace(entry.name.split('_')[0] + '_', '') if '_' in entry.name else entry.name,
             'path': os.path.join(uploads_dir, entry.name), 'category': 'uploaded'}
            for entry in os.scandir(uploads_dir) if entry.is_file() and entry.name.endswith('.csv')
        ]
        csv_files.extend(upload_files)
    except OSError:
        pass  # Removed logging for speed
    
    return csv_files

def get_available_csv_files():
    """Get available CSV files with ultra-fast cache invalidation."""
    import time
    cache_key = int(time.time() / 30)  # Cache for 30 seconds (faster refresh)
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

@lru_cache(maxsize=64)  # Increased cache size for more speed
def read_csv_data_cached(csv_path, file_mtime):
    """Cached CSV reading with file modification time for invalidation. LIGHTNING-FAST optimized."""
    try:
        with open(csv_path, 'r', encoding='utf-8', newline='') as f:
            # Ultra-fast CSV reading: limit rows, use list comprehension
            reader = csv.reader(f)
            header = next(reader, None)  # Get header first
            data = [header] if header else []
            
            # Read max 50 rows for lightning-fast preview
            data.extend([row for i, row in enumerate(reader) if i < 49])
            return data
    except Exception:
        return []  # Silent fail for maximum speed

def read_csv_data(csv_path):
    """Ultra-fast CSV data reader with intelligent caching."""
    if not csv_path or not os.path.exists(csv_path):
        return []
    
    try:
        # Use file modification time for cache invalidation
        file_mtime = int(os.path.getmtime(csv_path))
        return read_csv_data_cached(csv_path, file_mtime)
    except Exception:
        return []  # Silent fail for speed
    """Read CSV data with caching based on file modification time. Ultra-fast."""
    if not csv_path or not os.path.exists(csv_path):
        return []
    
    try:
        file_mtime = os.path.getmtime(csv_path)
        return read_csv_data_cached(csv_path, file_mtime)
    except Exception:
        return []  # Removed logging for speed

# --- ROUTES ---

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/upload', methods=['POST'])
def upload():
    """Handle file upload with robust error handling and category support."""
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file provided'}), 400
    
    file = request.files['file']
    category = request.form.get('category', 'uploaded')  # Get category from form
    
    if not file.filename or not allowed_file(file.filename):
        return jsonify({'status': 'error', 'message': 'Invalid file type. Please upload a CSV file.'}), 400
    
    try:
        ensure_upload_dir()
        filename = secure_filename(file.filename)
        
        # Handle category-specific uploads
        if category in ['ikk-api', 'ikk-ruang-terbatas', 'ikk-ketinggian']:
            # Replace the existing IKK category file
            category_mapping = {
                'ikk-api': 'personnel_list_IA.csv',
                'ikk-ruang-terbatas': 'personnel_list_IR.csv',
                'ikk-ketinggian': 'personnel_list_IK.csv'
            }
            file_path = category_mapping[category]
        elif category == 'ikh':
            # Replace default IKH file
            file_path = 'personnel_list.csv'
        else:
            # Regular upload to uploads folder
            unique_name = f"{uuid.uuid4().hex}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
        
        file.save(file_path)
        session['csv_path'] = file_path
        
        # Clear caches instantly
        get_csv_files_cached.cache_clear()
        read_csv_data_cached.cache_clear()
        
        # Ultra-fast response without content-type check
        return jsonify({'status': 'success', 'message': 'File uploaded successfully'})
            
    except Exception:
        # Ultra-fast error response
        return jsonify({'status': 'error', 'message': 'Upload failed'}), 500

@app.route('/shift_test.html')
def shift_test():
    return send_file('shift_test.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard with optimized CSV preview."""
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
    """IKH automation page with optimized data loading."""
    # Force use IKH default CSV - always use personnel_list.csv for IKH
    csv_path = get_ikh_csv_path()
    if csv_path:
        session['csv_path'] = csv_path  # Update session to IKH file
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
    """IKK categories page - landing page for all IKK types."""
    return render_template('ikk_categories.html')

@app.route('/ikk/api')
def ikk_api():
    """IKK Api automation page."""
    # Force use IKK Api CSV
    csv_path = get_ikk_csv_path('api')
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
    # Force use IKK Ruang Terbatas CSV
    csv_path = get_ikk_csv_path('ruang-terbatas')
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
    # Force use IKK Ketinggian CSV
    csv_path = get_ikk_csv_path('ketinggian')
    if csv_path:
        session['csv_path'] = csv_path
    csv_data = read_csv_data(csv_path) if csv_path else []
    today_date = date.today().strftime('%Y-%m-%d')
    
    return render_template('ikk_ketinggian.html', 
                         csv_data=csv_data, 
                         today_date=today_date)

@app.route('/select_csv', methods=['POST'])
def select_csv():
    """Select CSV file with validation and category support."""
    try:
        data = request.get_json()
        selected_path = data.get('csv_path') if data else None
        category = data.get('category', 'default') if data else 'default'
        
        if not selected_path:
            return jsonify({'status': 'error', 'message': 'No file path provided'}), 400
        
        available_files = get_available_csv_files()
        valid_paths = [f['path'] for f in available_files]
        
        if selected_path in valid_paths:
            session['csv_path'] = selected_path
            # Store category-specific CSV path in session if needed
            if category.startswith('ikk-'):
                session[f'{category}_csv_path'] = selected_path
            elif category == 'ikh':
                session['ikh_csv_path'] = selected_path
                
            read_csv_data_cached.cache_clear()
            return jsonify({'status': 'success', 'message': f'CSV file selected successfully for {category}'})
        else:
            return jsonify({'status': 'error', 'message': 'Invalid CSV file selected'}), 400
    except Exception:
        return jsonify({'status': 'error', 'message': 'Selection failed'}), 500

def clear_log_file():
    """Clear automation log file ultra-fast."""
    try:
        open('automation.log', 'w').close()  # Fastest way to clear
    except Exception:
        pass  # Silent fail for speed

def run_automation_process(script_path, csv_path, selected_indices, selected_date, selected_shift, mode):
    """LIGHTNING-FAST automation process with minimal overhead."""
    global current_process
    try:
        env = os.environ.copy()
        env['DISPLAY'] = os.environ.get('DISPLAY', ':0')
        env['PYTHONUNBUFFERED'] = '1'
        
        # ULTRA-FAST command building based on script type
        if 'ikk_automation.py' in script_path:
            # Lightning IKK automation: python ikk_automation.py <category> [date] [description] [shift]
            category_map = {
                'IKK-API': 'IA',
                'IKK-RUANG-TERBATAS': 'IR', 
                'IKK-KETINGGIAN': 'IK'
            }
            category = category_map.get(mode, 'IA')
            
            process_args = [
                '/home/dan/Portal/.venv/bin/python', 
                script_path, 
                category,
                selected_date or '30',  # Default to day 30 if no date
                'MELTING REPAIR',  # Default description
                str(selected_shift or 1)  # Add shift parameter
            ]
            
            # DEBUG: Log the exact command that will be executed
            print(f"🔍 EXACT COMMAND TO RUN: {' '.join(process_args)}")
            print(f"🔍 SHIFT PARAMETER: {selected_shift} (type: {type(selected_shift)})")
                
        else:
            # Legacy script format (for IKH) - minimal changes
            process_args = [
                '/home/dan/Portal/.venv/bin/python', 
                script_path, 
                csv_path
            ]
            
            if selected_indices:
                process_args.extend([str(i) for i in selected_indices])
            
            if selected_date:
                process_args.append(f"--date={selected_date}")
                
            if selected_shift:
                process_args.append(f"--shift={selected_shift}")
        
        logger.warning(f"🚀 LIGHTNING {mode}: Starting...")  # Changed to WARNING level for speed
        
        # INSTANT log initialization - minimal writes
        log_path = 'automation.log'
        with open(log_path, 'w', encoding='utf-8', buffering=1) as log_file:  # Line buffering for speed
            log_file.write(f"🚀 {mode} LIGHTNING automation started\n")
        
        # LIGHTNING process start with minimal overhead
        global current_process
        with open(log_path, 'a', encoding='utf-8', buffering=1) as log_file:  # Line buffering
            current_process = subprocess.Popen(
                process_args, 
                stdout=log_file, 
                stderr=subprocess.STDOUT, 
                text=True, 
                env=env,
                bufsize=0,  # Unbuffered for immediate output
                universal_newlines=True
            )
            
            # LIGHTNING-FAST process execution with reduced timeout
            try:
                return_code = current_process.wait(timeout=900)  # 15 minutes (faster timeout)
                
                # Minimal completion logging
                if return_code == 0:
                    log_file.write(f"\n✅ {mode} completed!\n")
                else:
                    log_file.write(f"\n❌ Failed: {return_code}\n")
                    
            except subprocess.TimeoutExpired:
                if current_process:
                    current_process.terminate()
                    try:
                        current_process.wait(timeout=5)  # Faster termination
                    except subprocess.TimeoutExpired:
                        current_process.kill()
                        
                log_file.write(f"\n⏰ Timeout\n")
                
    except Exception:
        # Ultra-fast error handling
        try:
            with open('automation.log', 'a', encoding='utf-8') as log_file:
                log_file.write(f"\n❌ Error\n")
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
    """Process automation request with robust validation and error handling."""
    try:
        # Clear log before starting
        clear_log_file()
        
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'No data provided'}), 400
        
        selected_rows = data.get('selected_rows', [])
        selected_indices = data.get('selected_indices', [])
        mode = data.get('mode', 'IKH')
        selected_date = data.get('selected_date', '')
        selected_shift = data.get('selected_shift', 1)  # Default shift 1
        
        # DEBUG: Log received shift value
        print(f"🔍 Backend received shift: {selected_shift} (type: {type(selected_shift)})")
        
        # Determine CSV path based on mode
        if mode.startswith('IKK-'):
            # Extract category from mode (e.g., 'IKK-API' -> 'api')
            category = mode.replace('IKK-', '').lower().replace('_', '-')
            csv_path = get_ikk_csv_path(category)
        elif mode == 'IKH':
            # Always use IKH default CSV
            csv_path = get_ikh_csv_path()
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
        
        # Submit to thread pool for execution
        executor.submit(run_automation_process, script_path, csv_path, selected_indices, selected_date, selected_shift, mode)
        
        return jsonify({'status': 'success', 'message': 'Automation started successfully'}), 200
        
    except Exception:
        return jsonify({'status': 'error', 'message': 'Failed to start automation'}), 500

@app.route('/stop_process', methods=['POST'])
def stop_process():
    """Stop the currently running automation process."""
    global current_process
    try:
        if current_process and current_process.poll() is None:
            # Terminate the process
            current_process.terminate()
            try:
                # Wait a bit for graceful termination
                current_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # Force kill if still running
                current_process.kill()
                current_process.wait()
            
            logger.info("Automation process stopped by user")
            
            # Add stop message to log
            try:
                with open('automation.log', 'a', encoding='utf-8') as log_file:
                    log_file.write('\n🛑 Process stopped by user\n🔄 Cleanup completed\n')
            except Exception as e:
                logger.error(f"Error writing stop message to log: {e}")
            
            return jsonify({'status': 'success', 'message': 'Process stopped successfully'})
        else:
            return jsonify({'status': 'info', 'message': 'No process running'})
    except Exception as e:
        logger.error(f"Error stopping process: {e}")
        return jsonify({'status': 'error', 'message': f'Error stopping process: {str(e)}'}), 500

@app.route('/get_log', methods=['GET'])
def get_log():
    """Get automation log ultra-fast."""
    try:
        with open('automation.log', 'r', encoding='utf-8') as log_file:
            content = log_file.read()
            return content if content else '💭 Starting...'
    except FileNotFoundError:
        return '💭 Waiting...'
    except Exception:
        return '❌ Error reading log'

@app.route('/check_completion', methods=['GET'])
def check_completion():
    """Check if automation process is completed - fixes frontend-backend sync"""
    try:
        # Check process status file
        status_file = "/home/dan/Portal/process_status.json"
        if os.path.exists(status_file):
            with open(status_file, 'r') as f:
                status = json.load(f)
            return jsonify(status)
        
        # Fallback: check automation log
        log_file = "/home/dan/Portal/automation.log"
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            completion_indicators = [
                "✅ IKK AUTOMATION COMPLETED SUCCESSFULLY!",
                "🎉 AUTOMATION SELESAI! Tekan Enter untuk menutup browser...",
                "IKK AUTOMATION SUCCESS",
                "BERHASIL SUBMIT IKK!"
            ]
            
            is_completed = any(indicator in content for indicator in completion_indicators)
            
            return jsonify({
                "process_running": False,
                "process_completed": is_completed,
                "completion_time": time.time() if is_completed else None,
                "last_update": time.time()
            })
        
        return jsonify({
            "process_running": False,
            "process_completed": False,
            "completion_time": None,
            "last_update": time.time()
        })
        
    except Exception as e:
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

def get_ikh_csv_path():
    """Get CSV path specifically for IKH - use personnel_list_ALL.csv as default."""
    default_csv = 'personnel_list_ALL.csv'  # Use ALL personnel list for IKH
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), default_csv)
    return csv_path if os.path.exists(csv_path) else None

def get_ikk_csv_path(category):
    """Get CSV path for specific IKK category."""
    csv_mapping = {
        'api': 'personnel_list_IA.csv',
        'ruang-terbatas': 'personnel_list_IR.csv', 
        'ketinggian': 'personnel_list_IK.csv'
    }
    
    csv_file = csv_mapping.get(category)
    if not csv_file:
        return None
        
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), csv_file)
    return csv_path if os.path.exists(csv_path) else None

if __name__ == '__main__':
    # Ensure upload directory exists
    ensure_upload_dir()
    
    # Ultra-fast production settings
    app.run(
        host='0.0.0.0', 
        port=int(os.environ.get('PORT', 5000)), 
        debug=False,  # Always false for speed
        threaded=True,
        use_reloader=False,  # Disable reloader for speed
        use_debugger=False   # Disable debugger for speed
    )