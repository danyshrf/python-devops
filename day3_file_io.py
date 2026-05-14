#!/usr/bin/env python3
"""
Day 3 — File I/O
Bash: cat, echo, >>, grep, wc -l
Python: open(), read(), write(), readlines()
"""

import os
from collections import Counter

# --- WRITE A FILE ---
# Bash: echo "text" > file.log  or  cat > file.log << EOF
sample_logs = """2024-01-15 08:05:44 INFO  Server web-01 started
2024-01-15 08:06:01 INFO  Health check passed
2024-01-15 08:10:12 WARNING High memory on web-01: 87%
2024-01-15 08:15:33 ERROR Failed to connect to db-01
2024-01-15 08:16:00 ERROR Timeout reaching 10.0.0.5
2024-01-15 08:18:44 INFO  Retrying connection...
2024-01-15 08:20:01 ERROR Disk space low: /var/log at 95%
2024-01-15 08:21:10 WARNING CPU spike on web-02: 91%
2024-01-15 08:22:00 INFO  Backup completed successfully
2024-01-15 08:25:00 ERROR db-01 unreachable after 3 retries
"""

# "w" = write(overwrite), "a" = append, "r" = read

with open("sample.log", "w") as f:
    f.write(sample_logs)
    print(f"Current Working Directory: {os.getcwd()}")

print("Created sample.log")

# --- Read ENTIRE FILE ---
with open("sample.log", "r") as f:
    content = f.read()
print(f"\nTotal characters: {len(content)}")

# --- READ LINE BY LINE ---
# Bash: while IFS= read -r line; do ...; done < sample.log
print("\n--- ERROR lines only ---")
with open("sample.log", "r") as f:
    for line in f:
        if "ERROR" in line:
            print(f"  {line.strip()}")

# --- READLINES → list of lines ---
# Bash: mapfile -t lines < sample.log
with open("sample.log", "r") as f:
    lines = f.readline()

print(f"\nTotal lines: {len(lines)}")

# --- COUNT LOG LEVELS ---
# Bash: grep -c "ERROR" sample.log
levels = Counter()
with open("sample.log", "r") as f:
    for line in f:
        for level in ["INFO", "ERROR", "WARNING"]:
            if level in line:
                levels[level] += 1
                
print(f"\nLog level Counts: {dict(levels)}")

# --- EXTRACT SPECIFIC FIELDS ---
# Bash: awk '{print $1, $2}' sample.log
print("\n--- Timestamps + Level ---")
with open("sample.log", "r") as f:
    for line in f:
        parts = line.split()
        if len(parts) >= 3:
            date, time, level = parts[0], parts[1], parts[2]
            print(f" {date} {time} {level}")

# --- APPEND TO FILE ---
# Bash: echo "new line" >> sample.log
with open("sample.log", "a") as f:
    f.write("2026-01-15 08:30:00 INFO  Manual entry appended\n")

print("\nAppended a line to sample.log")

# --- WRITE SUMMARY REPORT ---
# Bash: echo "report" > report.txt
error_lines = []
with open("sample.log", "r") as f:
    for line in f:
        if "ERROR" in line:
            error_lines.append(line.strip())

report = f"""=== Log Analysis Report ===
Total lines : {len(lines)}
INFO        : {levels.get('INFO', 0)}
WARNING     : {levels.get('WARNING', 0)}
ERROR       : {levels.get('ERROR', 0)}
--- Error Details ---
"""

for e in error_lines:
    report += f" {e}\n"

with open("report.txt", "w") as f:
    f.write(report)

print("\nReport written to report.txt")
print("\n--- report.txt contents ---")
print(report)

# --- CHECK FILE EXISTS BEFORE OPENING ---
# Bash: [ -f file ] && cat file
for fname in ["report.txt", "missing.log"]:
    if os.path.exists(fname):
        size = os.path.getsize(fname)
        print(f" EXISTS: {fname} ({size} bytes)")
    else:
        print(f" MISSING: {fname}")

# --- CLEANUP ---
os.remove("sample.log")
os.remove("report.txt")
print("\n Cleaned up the temp files")
