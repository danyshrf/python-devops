#!/usr/bin/env python3

import os
import sys
import shutil

def read_config(filepath):
    try:
        with open(filepath, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        return None
    except PermissionError:
        print(f"Error: Permission denied: {filepath}")
        return None
    except Exception as e:
        print(f"Error: Unexpected: {e}")
        return None
    
print("---Config Reading---")
print(f"Hostname: {read_config('/etc/hostname')}")
print(f"Result: {read_config('/nonexistant/file.conf')}")

# ----Custom Exceptions----
class ServerUnreachableError(Exception):
    pass

class DiskFullError(Exception):
    pass

def check_disk_space(path, threshold=90):
    total, used, free = shutil.disk_usage(path)
    percent_used = (used / total) * 100
    if percent_used > threshold:
        raise DiskFullError(f"{path} is {percent_used:.1f}% full - threshold is {threshold}%")
    return percent_used

print("\n----- Disk Check ----")
try:
    usage = check_disk_space("/", threshold=99)
    print(f"OK: Disk at {usage:.1f}%")
except DiskFullError as e:
    print(f"ALERT: {e}")

try:
    usage = check_disk_space("/", threshold=5)
    print(f"OK: Disk at {usage:.1f}%")
except DiskFullError as e:
    print(f"ALERT: {e}")


# --- FINALLY --- always runs, like a cleanup trap in Bash
# Bash: trap "rm -f /tmp/lockfile" EXIT

def risky_operation(filepath):
    print(f"\nOpening {filepath}....")
    try:
        f = open(filepath, "r")
        data = f.read()
        return data
    except FileNotFoundError:
        print("File Missing - handled")
        return None
    finally:
        print("cleanup ran (finally always executes)")

risky_operation("/etc/hostname")
risky_operation("/no/such/file")

def parse_port(value):
    try:
        port = int(value)
        if not(1 <= port <= 65535):
            raise ValueError(f"{port} is out of valid port range")
        return f"valid {port}"
    except (ValueError, TypeError) as e:
        print(f"invalid port '{value}': {e}")
        return None
    
print("\n--- Port Validation ---")
print(parse_port("22"))
print(parse_port("99999"))
print(parse_port("ssh"))
print(parse_port(None))

# --- REAL PATTERN: validate env vars and exit cleanly ---
# Bash: [ -z "$SSH_HOST" ] && echo "ERROR" && exit 1

def require_vars(var_names):
    missing = [v for v in var_names if not os.environ.get(v)]
    if missing:
        print(f"\nError: Missing required env vars: {missing}")
        sys.exit(1)