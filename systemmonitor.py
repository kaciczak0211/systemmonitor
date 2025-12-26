import ttkbootstrap as ttk  # A wrapper around tkinter that provides modern, flat themes (Bootstrap style).
from ttkbootstrap.constants import * # Imports layout constants like 'BOTH', 'LEFT', 'YES' to make code cleaner.
import psutil  # The 'process and system utilities' library. Used to fetch CPU, RAM, and Disk stats.
import time
import platform # For checking OS

class SystemMonitor:
    """
    Main class for the System Monitor application.
    It builds the UI and handles the periodic data refreshing.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("System Monitor")  # Set the window title.
        self.root.geometry("400x400")  # Set the default window size (width x height).
        
        # --- Main Layout ---
        # A main frame acts as a container for all other widgets, adding some padding around the edges.
        self.main_container = ttk.Frame(root, padding=20)
        self.main_container.pack(fill=BOTH, expand=YES)  # Fill the entire window.
        
        # --- Header ---
        # A large label at the top. 'bootstyle' applies the Bootstrap color theme (e.g., primary=blue).
        # Foreground='white' explicitly set.
        header = ttk.Label(self.main_container, text="System Dashboard", font=("Helvetica", 24, "bold"), bootstyle="primary", foreground="white")
        header.pack(pady=(0, 20))  # Add vertical padding (0 on top, 20 on bottom).

        # --- Metric Cards ---
        # We call a helper method `create_metric_card` to avoid repeating code for CPU, Memory, and Disk.
        self.create_metric_card("CPU Usage", "cpu")
        self.create_metric_card("Memory Usage", "mem")
        self.create_metric_card("Storage Usage", "disk")

        # --- Base-10 flag ---
        # macOS uses base-10 (1000^3) for Disk space since 10.6. Windows/Linux usually use base-2 (1024^3).
        self.is_macos = platform.system() == "Darwin"

        # --- Start Loop ---
        # Trigger the first update of the metrics.
        self.update_metrics()

    def create_metric_card(self, title, metric_type):
        """
        Helper function to create a visual 'card' for a single metric.
        It creates a LabelFrame (a frame with a title) and puts a progress bar inside.
        """
        # specialized frame with a border and a title text
        frame = ttk.Labelframe(self.main_container, text=title, padding=10, bootstyle="info")
        frame.pack(fill=X, pady=5)  # Pack vertically, filling the horizontal width (fill=X).
        
        # A sub-frame to hold the text label and the progress bar side-by-side
        content_frame = ttk.Frame(frame)
        content_frame.pack(fill=X)
        
        if metric_type == "cpu":
            # Create the percentage text label
            self.cpu_label = ttk.Label(content_frame, text="0%", font=("Helvetica", 12, "bold"), foreground="white")
            self.cpu_label.pack(side=RIGHT) # Place on the right side
            
            # Create the progress bar. 'striped' adds a visual texture.
            self.cpu_progress = ttk.Progressbar(content_frame, bootstyle="info-striped", maximum=100)
            self.cpu_progress.pack(side=LEFT, fill=X, expand=YES, padx=(0, 10))
            
        elif metric_type == "mem":
            self.mem_label = ttk.Label(content_frame, text="0%", font=("Helvetica", 12, "bold"), foreground="white")
            self.mem_label.pack(side=RIGHT)
            self.mem_progress = ttk.Progressbar(content_frame, bootstyle="warning-striped", maximum=100)
            self.mem_progress.pack(side=LEFT, fill=X, expand=YES, padx=(0, 10))
            
            # Extra detail label (e.g., "8 GB / 16 GB") placed below the bar
            self.mem_detail_label = ttk.Label(frame, text="", font=("Helvetica", 9), bootstyle="secondary", foreground="white")
            self.mem_detail_label.pack(anchor=W, pady=(5, 0)) # anchor=W means align West (Left)

        elif metric_type == "disk":
            self.disk_label = ttk.Label(content_frame, text="0%", font=("Helvetica", 12, "bold"), foreground="white")
            self.disk_label.pack(side=RIGHT)
            self.disk_progress = ttk.Progressbar(content_frame, bootstyle="success-striped", maximum=100)
            self.disk_progress.pack(side=LEFT, fill=X, expand=YES, padx=(0, 10))

            self.disk_detail_label = ttk.Label(frame, text="", font=("Helvetica", 9), bootstyle="secondary", foreground="white")
            self.disk_detail_label.pack(anchor=W, pady=(5, 0))

    def update_metrics(self):
        """
        Fetches the latest system stats and updates the UI.
        This function calls itself every 1000ms (1 second) to create a loop.
        """
        
        # --- 1. Update CPU ---
        # interval=None gets the average usage since the last call (non-blocking)
        cpu_percent = psutil.cpu_percent(interval=None)
        self.cpu_label.config(text=f"{cpu_percent}%")
        self.cpu_progress['value'] = cpu_percent
        
        # Dynamic color change: Turn red ('danger') if CPU usage is high (>80%)
        if cpu_percent > 80: self.cpu_progress.configure(bootstyle="danger-striped")
        else: self.cpu_progress.configure(bootstyle="info-striped")

        # --- 2. Update Memory ---
        mem = psutil.virtual_memory() # Returns an object with total, available, percent, used, etc.
        mem_percent = mem.percent
        # RAM is traditionally measured in binary GB (GiB) even on macOS
        mem_divisor = 1024**3
        mem_used_gb = round(mem.used / mem_divisor, 2)
        mem_total_gb = round(mem.total / mem_divisor, 2)
        
        self.mem_label.config(text=f"{mem_percent}%")
        self.mem_progress['value'] = mem_percent
        self.mem_detail_label.config(text=f"{mem_used_gb} GB used / {mem_total_gb} GB total")

        # --- 3. Update Storage ---
        disk = psutil.disk_usage('/') # Check the root directory '/'
        
        # Adjust divisor for macOS disk logic (System Settings uses 1000^3)
        # Windows/Linux usually stay with 1024^3
        disk_divisor = 1000**3 if self.is_macos else 1024**3
        
        # Fix for macOS/Shared Volumes: Calculate used based on Total - Free
        total_gb = disk.total / disk_divisor
        free_gb = disk.free / disk_divisor
        used_gb = total_gb - free_gb
        
        # Recalculate percent based on this new 'used' value
        recalc_percent = (used_gb / total_gb) * 100
        
        # Round for display
        disk_used_gb = round(used_gb, 2)
        disk_total_gb = round(total_gb, 2)
        disk_percent = round(recalc_percent, 1)

        self.disk_label.config(text=f"{disk_percent}%")
        self.disk_progress['value'] = disk_percent
        self.disk_detail_label.config(text=f"{disk_used_gb} GB used / {disk_total_gb} GB total")

        # --- 4. Schedule Next Update ---
        # root.after(ms, function) runs the function after the specified delay.
        # This keeps the GUI responsive while updating in the background.
        self.root.after(1000, self.update_metrics)

if __name__ == "__main__":
    # Create the main application window with the 'superhero' theme (a dark theme).
    root = ttk.Window(themename="superhero") 
    app = SystemMonitor(root)
    # Start the GUI event loop (waits for clicks, updates, etc.)
    root.mainloop()
