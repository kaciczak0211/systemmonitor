from flask import Flask, jsonify, render_template
import psutil
import platform

app = Flask(__name__)

# Helper to determine disk divisor (Base-10 for Mac, Base-2 for others)
IS_MACOS = platform.system() == "Darwin"
DISK_DIVISOR = 1000**3 if IS_MACOS else 1024**3

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/metrics')
def metrics():
    # CPU
    cpu = psutil.cpu_percent(interval=None)
    
    # Memory
    mem = psutil.virtual_memory()
    mem_percent = mem.percent
    mem_used_gb = round(mem.used / (1024**3), 2)
    mem_total_gb = round(mem.total / (1024**3), 2)
    
    # Disk
    disk = psutil.disk_usage('/')
    total_gb = disk.total / DISK_DIVISOR
    free_gb = disk.free / DISK_DIVISOR
    used_gb = total_gb - free_gb
    
    # Recalculate percent based on Used (Total - Free)
    disk_percent = round((used_gb / total_gb) * 100, 1)
    disk_used_gb = round(used_gb, 2)
    disk_total_gb = round(total_gb, 2)
    
    return jsonify({
        "cpu": cpu,
        "mem": {
            "percent": mem_percent,
            "used": mem_used_gb,
            "total": mem_total_gb
        },
        "disk": {
            "percent": disk_percent,
            "used": disk_used_gb,
            "total": disk_total_gb
        }
    })

if __name__ == '__main__':
    # Host='0.0.0.0' allows access from other devices on the network
    app.run(debug=True, host='0.0.0.0', port=5001)
