# System Monitor (GUI)

A lightweight, cross-platform system monitoring tool built with Python. It provides a modern, dark-themed dashboard to visualize real-time system resources.

## Features
- **CPU Usage**: Real-time percentage tracking.
- **Memory (RAM)**: Visualizes used vs. total memory with a progress bar.
- **Storage**: Monitors disk usage for the root partition.
  - *Smart Calculation*: automatically adapts unit sizing for macOS (Base-10 GB) vs. Linux (Base-2 GiB) to match native system reporting.
- **Modern UI**: Uses `ttkbootstrap` 'superhero' theme for a clean, professional look.

## Prerequisites
You need **Python 3.x** installed on your system.

### Dependencies
The project relies on two external libraries:
- `psutil`: For fetching system metrics.
- `ttkbootstrap`: For the modern GUI themes.

## Installation & Usage

### 1. Setup (First Time Only)
Open your terminal and navigate to the project folder. Then run these commands to create a virtual environment (sandbox) and install the libraries:
```bash
# Create a virtual environment named 'venv'
python3 -m venv venv

# Activate the environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install the required libraries
pip install psutil ttkbootstrap
```

### 2. Run the Application
Whenever you want to use the monitor, make sure you are in the project folder and run:

**Option A (Recommended)**: Run directly using the virtual environment python:
```bash
./venv/bin/python systemmonitor.py
```

**Option B**: Activate the environment first, then run:
```bash
source venv/bin/activate
python systemmonitor.py
```

## Compatibility
- **macOS**: Fully supported (tested).
- **Linux**: Fully supported.
- **Windows**: Should work, but disk pathing logic (`/`) may require minor tweaking for specific drive letters (e.g., `C:\`).
