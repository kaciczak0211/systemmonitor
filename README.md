# System Monitor (Web & Docker)

A lightweight, cross-platform system monitoring dashboard. It visualizes real-time CPU, Memory, and Disk usage in a clean web interface.

## Features
- **CPU**: Real-time percentage tracking.
- **Memory**: Visual used vs. total RAM.
- **Storage**: Monitors root partition disk usage (Smart Base-10 scaling for macOS).
- **Web Interface**: Auto-refreshing dashboard accessible from any browser.

## Quick Start (Docker)
The easiest way to run the monitor is using Docker.

1. **Build the image**:
   ```bash
   docker build -t system-monitor .
   ```
2. **Run the container**:
   ```bash
   docker run -p 5001:5001 system-monitor
   ```
3. **Open Dashboard**:
   Go to [http://localhost:5001](http://localhost:5001) in your browser.

## Manual Installation (No Docker)
If you prefer running it directly with Python:

1. **Clone the repo**:
   ```bash
   git clone https://github.com/kaciczak0211/systemmonitor.git
   cd systemmonitor
   ```

2. **Setup Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run**:
   ```bash
   python app.py
   ```
   Then open [http://localhost:5001](http://localhost:5001).

## Compatibility
- Works on macOS, Linux, and Windows.
- Optimized for Docker Desktop.
