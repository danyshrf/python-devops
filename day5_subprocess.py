#!/usr/bin/env python3
"""
Day 5 — subprocess
This is your Bash brain in Python.
Run any shell command, capture output, check exit codes.
"""

import subprocess
import sys

# ─── BASIC RUN ────────────────────────────────────────────────────────────────
# Bash: hostname
# subprocess.run() = fire a command and wait for it to finish
result = subprocess.run(["hostname"], capture_output=True, text=True)
print(f"Hostname : {result.stdout.strip()}")
print(f"Exit code: {result.returncode}")   # 0 = success, anything else = failure

# ─── CAPTURE OUTPUT ───────────────────────────────────────────────────────────
# Bash: uptime
result = subprocess.run(["uptime"], capture_output=True, text=True)
print(f"\nUptime: {result.stdout.strip()}")

# ─── CHECK EXIT CODE (like $? in Bash) ────────────────────────────────────────
# Bash: ping -c1 google.com; if [ $? -eq 0 ]; then ...
def host_reachable(host):
    result = subprocess.run(
        ["ping", "-c", "1", "-W", "2", host],
        capture_output=True,
        text=True
    )
    return result.returncode == 0   # True if ping succeeded

print("\n--- Ping check ---")
for host in ["8.8.8.8", "localhost", "192.168.255.254"]:
    status = "UP" if host_reachable(host) else "DOWN"
    print(f"  {host:<20} {status}")

# ─── SHELL=TRUE (pipe-friendly, use carefully) ────────────────────────────────
# Bash: df -h | grep -v tmpfs
# shell=True lets you use pipes and shell syntax directly
result = subprocess.run(
    "df -h | grep -v tmpfs",
    shell=True, capture_output=True, text=True
)
print(f"\n--- Disk (no tmpfs) ---\n{result.stdout.strip()}")

# ─── CAPTURE STDERR TOO ───────────────────────────────────────────────────────
# Bash: command 2>&1
result = subprocess.run(
    ["ls", "/nonexistent/path"],
    capture_output=True, text=True
)
print(f"\nstdout: '{result.stdout.strip()}'")
print(f"stderr: '{result.stderr.strip()}'")
print(f"exit  : {result.returncode}")

# ─── check=True: AUTO RAISE ON FAILURE ────────────────────────────────────────
# Bash: set -e  (exit on any error)
# check=True raises CalledProcessError if exit code != 0
print("\n--- check=True demo ---")
try:
    subprocess.run(["ls", "/nonexistent"], capture_output=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"Command failed (exit {e.returncode}): {e.stderr.strip()}")

# ─── RUN AND GET OUTPUT AS STRING ─────────────────────────────────────────────
# Bash: FREE=$(free -m | awk '/Mem/{print $4}')
def get_free_memory_mb():
    result = subprocess.run(
        "free -m | awk '/^Mem/{print $4}'",
        shell=True, capture_output=True, text=True
    )
    return int(result.stdout.strip())

free_mb = get_free_memory_mb()
print(f"\nFree memory: {free_mb} MB")

# ─── REAL DEVOPS USE CASE 1: SERVICE STATUS ───────────────────────────────────
# Bash: systemctl is-active nginx
def service_status(service):
    result = subprocess.run(
        ["systemctl", "is-active", service],
        capture_output=True, text=True
    )
    return result.stdout.strip()   # "active", "inactive", "failed", "unknown"

print("\n--- Service status ---")
for svc in ["ssh", "cron", "nginx", "docker"]:
    status = service_status(svc)
    icon = "✓" if status == "active" else "✗"
    print(f"  {icon} {svc:<10} {status}")

# ─── REAL DEVOPS USE CASE 2: DISK MONITOR ─────────────────────────────────────
# Bash: df -h --output=target,pcent | awk 'NR>1'
def disk_monitor(threshold=80):
    result = subprocess.run(
        "df -h --output=target,pcent",
        shell=True, capture_output=True, text=True
    )
    lines = result.stdout.strip().split("\n")[1:]  # skip header
    alerts = []
    for line in lines:
        parts = line.split()
        if len(parts) == 2:
            mount, percent = parts
            usage = int(percent.replace("%", ""))
            if usage > threshold:
                alerts.append(f"WARNING: {mount} is {percent} full")
    return alerts

print("\n--- Disk monitor (threshold=5%) ---")
alerts = disk_monitor(threshold=5)   # low threshold so it triggers
if alerts:
    for a in alerts:
        print(f"  {a}")
else:
    print("  All disks OK")

# ─── REAL DEVOPS USE CASE 3: RUN MULTIPLE COMMANDS ───────────────────────────
# Bash: for cmd in "cmd1" "cmd2"; do $cmd; done
def run_commands(commands):
    results = {}
    for cmd in commands:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        results[cmd] = {
            "output": result.stdout.strip(),
            "exit"  : result.returncode,
            "ok"    : result.returncode == 0
        }
    return results

print("\n--- Batch command run ---")
commands = ["whoami", "uname -r", "date +%Y-%m-%d", "cat /nonexistent 2>&1"]
results = run_commands(commands)
for cmd, res in results.items():
    status = "OK" if res["ok"] else "FAIL"
    print(f"  [{status}] $ {cmd}")
    print(f"         → {res['output'][:60]}")



def system_report():
    commands = {
        "OS"       : "grep PRETTY_NAME /etc/os-release | cut -d= -f2 | tr -d '\"'",
        "Kernel"   : "uname -r",
        "Uptime"   : "uptime -p",
        "CPUs"     : "nproc",
        "Free RAM" : "free -m | awk '/^Mem/{print $4}'",
        "Disk /"   : "df -h / | awk 'NR==2{print $5}'",
    }

    print("\n=== System Report ===")
    for label, cmd in commands.items():
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        value = result.stdout.strip() if result.returncode == 0 else "ERROR"
        print(f"  {label}: {value}")

system_report()