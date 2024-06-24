import subprocess


daemons = open("daemons_to_load.txt", "r")
services = []

user_action = input("What action do you want to do? Type 1 for start and 2 for stop the daemons, 3 for check status:\n")

for i in daemons:
    services.append(i.rstrip())


def check_service_status(service):
    result = subprocess.run(["systemctl", "is-active", service], capture_output=True, text=True)
    return result.stdout.strip() == "active"


def start_services():
    for service in services:
        subprocess.run(["sudo", "systemctl", "start", service], check=True)
        if check_service_status(service):
            print(f"Successfully started {service}")
        else:
            print(f"Failed to start {service}")


def stop_services():
    for service in services:
        subprocess.run(["sudo", "systemctl", "stop", service], check=True)
        print(f"Stopped {service}")


def check_all_services():
    for service in services:
        if check_service_status(service):
            print(f"Service {service} is running")
        else:
            print(f"Service {service} is stopped!")

if user_action == "1":
    start_services()
elif user_action == "2":
    stop_services()
elif user_action == "3":
    check_all_services()
else:
    print("Incorrect input!")
