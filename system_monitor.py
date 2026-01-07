from flask import Flask, render_template
import psutil
import platform
from datetime import datetime
import os

app = Flask(__name__)

# ---------------- SYSTEM INFO ----------------
def get_system_info():
    return {
        "os": platform.system(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor()
    }

# ---------------- SYSTEM STATUS ----------------
def get_system_status():
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent

    battery = None
    charging = None
    if hasattr(psutil, "sensors_battery"):
        b = psutil.sensors_battery()
        if b:
            battery = b.percent
            charging = b.power_plugged

    # Get all processes
    processes = [p.info for p in psutil.process_iter(['pid', 'name', 'cpu_percent'])]
    processes.sort(key=lambda x: x['cpu_percent'], reverse=True)

    return {
        "cpu": cpu,
        "ram": ram,
        "battery": battery,
        "charging": charging,
        "processes": processes
    }

# ---------------- DASHBOARD ROUTE ----------------
@app.route("/")
def dashboard():
    info = get_system_info()
    status = get_system_status()
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return render_template(
        "dashboard.html",
        info=info,
        status=status,
        time=time_now
    )

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="127.0.0.1", port=port, debug=False)
