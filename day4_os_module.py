#!/usr/bin/env python3
"""
Day 4 — os, sys, shutil
Everything you do with cd, ls, mkdir, cp, mv, rm, df, env in Bash
"""

import os 
import shutil 
import sys

# ─── os: NAVIGATION & PATHS ───────────────────────────────────────────────────
# Bash: pwd
print(f"Current dir: {os.getcwd()}")

# bash: echo #HOME
print(f"Home dir: {os.path.expanduser('-')}")

# Bash: dirname $0  /  basename $0
print(f"Script path: {os.path.abspath(__file__)}")
print(f"Script name: {os.path.basename(__file__)}")
print(f"Script dir: {os.path.dirname(os.path.abspath(__file__))}")

# ─── os: LIST DIRECTORY ───────────────────────────────────────────────────────
# Bash: ls -lh
print("\n---Files in the current dir---")
for item in sorted(os.listdir(".")):
    full = os.path.join(".", item)
    size = os.path.getsize(full)
    kind = "DIR" if os.path.isdir(full) else "FILE"
    print(f" [{kind}] {item:<30} {size} {bytes}")

# ─── os: CREATE DIRECTORIES ───────────────────────────────────────────────────
# Bash: mkdir -p workspace/logs/archive
os.makedirs("workspace/logs/archive", exist_ok=True)
os.makedirs("workspace/Backups", exist_ok="true")
print("\nCreated: workspace/logs/archieve, workspace/Backup")

# ─── os.path: PATH OPERATIONS ─────────────────────────────────────────────────
# Bash: [ -f file ] / [ -d dir ]
paths_to_check = ["/etc/hostname", "/etc/passws", "/nonexistant", "workspace"]
print("\n--- Path checks---")
for p in paths_to_check:
    exists = os.path.exists(p)
    is_file = os.path.isfile(p)
    is_dir = os.path.isdir(p)
    print(f" {p:<20} exists={exists} file={is_file} dir={is_dir}")

    # ─── os: ENVIRONMENT VARIABLES ────────────────────────────────────────────────
# Bash: echo $USER / echo $PATH / export MYVAR="value"
print("\n-----Enviornment Variables----")
user = os.environ.get("USER", "unknown")
home = os.environ.get("HOME", "not set")
shell = os.environ.get("SHELL", "not set")
path = os.environ.get("PATH", "").split(":")

print(f" USER: {user}")
print(f" HOME: {home}")
print(f" SHELL: {shell}")
print(f" PATH entries: {len(path)}")
print(f"  First PATH  : {path[0]}")

# Set an env var for child processes (doesn't affect parent shell, same as Bash)
os.environ["MY_SCRIPT_ENV"] = "Production"
print(f" MY_SCRIPT_ENV: {os.environ.get('MY_SCRIPT_ENV')}")

# ─── shutil: COPY / MOVE / DELETE ─────────────────────────────────────────────
# Create a test file to work with
with open("workspace/test.conf", "w") as f:
    f.write("[server]\nhost=web-01\nport=22\n")

# Bash: cp workspace/test.conf workspace/backups/test.conf.bak
shutil.copy("workspace/test.conf", "workspace/backups/test.conf.bak")
print("\nCopied: test.conf → backups/test.conf.bak")

# Bash: cp -r workspace/logs workspace/logs_copy
shutil.copytree("workspace/logs", "workspace/logs_copy")
print("Copied dir: logs → logs_copy")

# Bash: mv workspace/test.conf workspace/logs/test.conf
shutil.move("workspace/test.conf", "workspace/logs/test.conf")
print("Moved: test.conf → logs/test.conf")

# ─── shutil: DISK USAGE ───────────────────────────────────────────────────────
# Bash: df -h /
print("\n--- Disk usage: / ---")
total, used, free = shutil.disk_usage("/")
gb = 2**30
print(f" Total: {total // gb} GB")
print(f" Used: {used // gb} GB ({(used/total)*100:.1f}%)")
print(f" Free: {free // gb} GB")

# ─── sys: SCRIPT ARGUMENTS & EXIT ─────────────────────────────────────────────
# Bash: $0 $1 $2 ... / $# / exit 1
print(f"\n--- sys info ---")
print(f" Python Version:  {sys.version.split()[0]}")
print(f" Platform  : {sys.platform}")
print(f" Args Passed:  {sys.argv}")
print(f" Arg count   : {len(sys.argv)-1}")

# ─── os.walk: RECURSIVE DIRECTORY TREE ───────────────────────────────────────
# Bash: find workspace -type f
print("\n--- All files under workspace/ ---")
for dirpath, dirnames, filenames in os.walk("workspace"):
    for filename in filenames:
        full_path = os.path.join(dirpath, filename)
        size = os.path.getsize(full_path)
        print(f"  {full_path} ({size} bytes)")


# ─── CLEANUP ──────────────────────────────────────────────────────────────────
# Bash: rm -rf workspace
shutil.rmtree("workspace")
print("\nCleaned up workspace")

def audit_directory(path):
    file_count = 0
    dir_count = 0
    total_size = 0
    largest = ("", 0)

    for dirpath, dirname, filename in os.walk(path):
        dir_count += len(dirname)
        for fname in filenames:
            fpath = os.path.join(dirpath, fname)
            try:
                size = os.path.getsize(fpath)
                file_count += 1
                total_size += size
                if size > largest[1]:
                    largest = (fpath, size)
            except (OSError, PermissionError):
                pass
    
    print(f"\n --- Audit: {path} ---")
    print(f"  Files  : {file_count}")
    print(f"  Directories: {dir_count}")
    print(f"  Total size: {total_size:,} bytes ({total_size // 1024} KB) ")
    print(f" Lrgest : {largest[0]} ({largest[1]:,} bytes)")


audit_directory(os.path.expanduser("~/devops-python"))