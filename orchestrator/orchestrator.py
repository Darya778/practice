import subprocess
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.join(current_dir, '../log'))
import os
import time
import copy
import schedule
from datetime import datetime

daemons_file = "daemons_to_load.txt"
services = []
old_services = []

def load_services(file):
    with open(file, "r") as daemons:
        return [i.strip() for i in daemons]

services = load_services(daemons_file)
old_services = copy.deepcopy(services)

user_action = input("What action do you want to do? Type 1 for start, 2 for stop the daemons, 3 for check status:\n")

def create_service_file(service_name):
    with open("/home/dasha/wotiwan/orchestrator/templates/service_template.txt", "r") as f:
        service_template_file = f.read()
    service_template = service_template_file.format(service_name=service_name)
    service_file_path = f"/home/dasha/wotiwan/orchestrator/daemon_services/{service_name}.service"
    with open(service_file_path, "w") as service_file:
        service_file.write(service_template)

def create_python_file(service_name):
    with open("/home/dasha/wotiwan/orchestrator/templates/daemon_template.txt", "r") as f:
        python_template_file = f.read()
    python_template = python_template_file.format(service_name=service_name)
    python_file_path = f"/home/dasha/wotiwan/orchestrator/daemons/{service_name}.py"
    with open(python_file_path, "w") as python_file:
        python_file.write(python_template)

def check_service_status(service):
    result = subprocess.run(["systemctl", "is-active", service], capture_output=True, text=True)
    return result.stdout.strip() == "active"

def start_services():
    for service in services:
        create_service_file(service)
        create_python_file(service)
        subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True)
        subprocess.run(["sudo", "systemctl", "enable", f"/home/dasha/wotiwan/orchestrator/daemon_services/{service}.service"], check=True)
        subprocess.run(["sudo", "systemctl", "start", service], check=True)
        if check_service_status(service):
            print(f"Successfully started {service}")
        else:
            print(f"Failed to start {service}")
        time.sleep(2)

def stop_services():
    for service in services:
        subprocess.run(["sudo", "systemctl", "stop", service], check=True)
        subprocess.run(["sudo", "systemctl", "disable", service], check=True)
        service_file_path = f"/home/dasha/wotiwan/orchestrator/daemon_services/{service}.service"
        if os.path.exists(service_file_path):
            os.remove(service_file_path)
        python_file_path = f"/home/dasha/wotiwan/orchestrator/daemons/{service}.py"
        if os.path.exists(python_file_path):
            os.remove(python_file_path)
        print(f"Stopped and removed {service}")

def check_all_services():
    for service in services:
        if check_service_status(service):
            print(f"Service {service} is running")
        else:
            print(f"Service {service} is stopped!")

def update_services():
    global services
    global old_services
    new_services = load_services(daemons_file)
    for service in new_services:
        if service not in old_services:
            create_service_file(service)
            create_python_file(service)
            subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True)
            subprocess.run(["sudo", "systemctl", "enable", f"/home/dasha/wotiwan/orchestrator/daemon_services/{service}.service"], check=True)
            subprocess.run(["sudo", "systemctl", "start", service], check=True)
            if check_service_status(service):
                print(f"Successfully started {service}")
            else:
                print(f"Failed to start {service}")
    old_services = copy.deepcopy(new_services)

def remove_old_services():
    global services
    global old_services
    new_services = load_services(daemons_file)
    for service in old_services:
        if service not in new_services:
            subprocess.run(["sudo", "systemctl", "stop", service], check=True)
            subprocess.run(["sudo", "systemctl", "disable", service], check=True)
            service_file_path = f"/home/dasha/wotiwan/orchestrator/daemon_services/{service}.service"
            if os.path.exists(service_file_path):
                os.remove(service_file_path)
            python_file_path = f"/home/dasha/wotiwan/orchestrator/daemons/{service}.py"
            if os.path.exists(python_file_path):
                os.remove(python_file_path)
            print(f"Stopped and removed {service}")
    old_services = copy.deepcopy(new_services)


schedule.every().day.at("23:30").do(update_services)
schedule.every().day.at("00:00").do(remove_old_services)

if user_action == "1":
    start_services()
elif user_action == "2":
    stop_services()
elif user_action == "3":
    check_all_services()
else:
    print("Incorrect input!")

while True:
    schedule.run_pending()
    time.sleep(1)
