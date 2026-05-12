#!/usr/bin/env python3

# --- Varibles ---
#Bash: server="web-01"
#python

server = "web-01"
port = 22
cpu_threshold = 90
is_active = True


print(f"server: {server}, Port : {port}")

# --- List (Bash Arrays) ----
# BASH: servers=("web-01" "web-02" "db-01")
servers = ["web-01", "web-02", "db-01", "db-02"]

# --- FOR LOOP ---
# BASH: for server in "${servers[@]}"; do echo $server; done

print("\n --- ALL SERVERS ---")
for s in servers:
    print(f"Server: {s}")

# ---- IF STATEMENT ---
# BASH: if [ $cpu -gt $cpu_threshold ]; then echo  ....

cpu = 95
if cpu > 90:
    print(f"\nCritical: CPU usage is at {cpu}%")
elif cpu > 80:
    print(f"\nWarning: CPU usage is at {cpu}%")
else:
    print(f"\nOk: CPU is at {cpu}%")


# --- FUNCTIONS ---
# BASH: function check_server() { ... }
def check_server(name, cpu, threshold=90):
    """ Check if CPU is above threshold"""
    status = "CRITICAL" if cpu > threshold else "ok"
    return f"[{status}] {name}: CPU at {cpu}%"

print("\n--- CHECK SERVERS ---")

print(check_server("web-01", 95))
print(check_server("web-02", 60))
print(check_server("db-01", 85, threshold=80)) # custom threshold
                   
# --- DICTIONARIES ---
# BASH: declare -A server_info: server_info=( ["web-01"]="Linux" ["db-01"]="Windows" )

server_info = {
    "name" : "web-01",
    "ip" : "10.0.0.1",
    "cpu" : 72,
    "disk" : 45
}
print(f"\n{server_info['name']} at {server_info['ip']}")

# --- LIST COMPREHENSION (compact loops) ---
# Bash: for s in "${servers[@]}"; do if [[ $s == *"web"* ]]; then ...
web_servers = [s for s in servers if "web" in s]
print(f"\nWeb servers only: {web_servers}")       


def filter_web_servers(servers):
    return [s for s in servers if "web" in s]

result = filter_web_servers(["web-01", "web-02", "web-01", "db-02"])
print(f"Filtered web servers: {result}")