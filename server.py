#!/usr/bin/env python3
"""
server.py — Backend Flask pour le dashboard système Parrot OS
Lanse ak: python3 server.py
"""

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import psutil
import platform
import subprocess
import os
import time
import datetime

app = Flask(__name__, static_folder='.')
CORS(app)

def get_cpu():
    freq = psutil.cpu_freq()
    return {
        "percent": psutil.cpu_percent(interval=0.3),
        "cores_logical": psutil.cpu_count(logical=True),
        "cores_physical": psutil.cpu_count(logical=False),
        "freq_current": round(freq.current, 0) if freq else 0,
        "freq_max": round(freq.max, 0) if freq else 0,
        "per_core": psutil.cpu_percent(percpu=True, interval=0.3),
    }

def get_ram():
    vm = psutil.virtual_memory()
    sw = psutil.swap_memory()
    return {
        "total": vm.total,
        "used": vm.used,
        "available": vm.available,
        "percent": vm.percent,
        "swap_total": sw.total,
        "swap_used": sw.used,
        "swap_percent": sw.percent,
    }

def get_disk():
    disks = []
    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
            disks.append({
                "device": part.device,
                "mountpoint": part.mountpoint,
                "fstype": part.fstype,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent,
            })
        except PermissionError:
            continue
    io = psutil.disk_io_counters()
    return {
        "partitions": disks,
        "read_bytes": io.read_bytes if io else 0,
        "write_bytes": io.write_bytes if io else 0,
    }

def get_network():
    net = psutil.net_io_counters()
    addrs = psutil.net_if_addrs()
    interfaces = {}
    for iface, addr_list in addrs.items():
        for addr in addr_list:
            if addr.family == 2:  # AF_INET
                interfaces[iface] = addr.address
    return {
        "bytes_sent": net.bytes_sent,
        "bytes_recv": net.bytes_recv,
        "packets_sent": net.packets_sent,
        "packets_recv": net.packets_recv,
        "interfaces": interfaces,
    }

def get_processes():
    procs = []
    for p in sorted(psutil.process_iter(['pid','name','cpu_percent','memory_percent','status']),
                    key=lambda x: x.info['cpu_percent'] or 0, reverse=True)[:10]:
        procs.append(p.info)
    return procs

def get_system():
    boot = psutil.boot_time()
    uptime_sec = int(time.time() - boot)
    hours, rem = divmod(uptime_sec, 3600)
    minutes, seconds = divmod(rem, 60)

    # Température (si disponible)
    temps = {}
    try:
        sensors = psutil.sensors_temperatures()
        for name, entries in sensors.items():
            for e in entries:
                if e.current:
                    temps[name] = round(e.current, 1)
                    break
    except Exception:
        pass

    return {
        "hostname": platform.node(),
        "os": platform.system(),
        "distro": platform.version()[:60],
        "kernel": platform.release(),
        "arch": platform.machine(),
        "python": platform.python_version(),
        "uptime": f"{hours}h {minutes}m {seconds}s",
        "boot_time": datetime.datetime.fromtimestamp(boot).strftime("%d/%m/%Y %H:%M"),
        "temperatures": temps,
        "datetime": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    }

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/stats')
def stats():
    return jsonify({
        "cpu": get_cpu(),
        "ram": get_ram(),
        "disk": get_disk(),
        "network": get_network(),
        "processes": get_processes(),
        "system": get_system(),
    })

if __name__ == '__main__':
    print("\n🖥️  Parrot OS Dashboard")
    print("📡 Ouvri browser ou sou: http://localhost:5000\n")
    app.run(host='0.0.0.0', port=5000, debug=False)
