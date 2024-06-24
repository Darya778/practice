import subprocess


daemons = open("daemons_to_load.txt", "r")
services = []

for i in daemons:
    services.append(i.rstrip())


def start_services():
    for service in services:
        subprocess.run(["sudo", "systemctl", "start", service], check=True)
        print(f"Started {service}")


def stop_services():
    for service in services:
        subprocess.run(["sudo", "systemctl", "stop", service], check=True)
        print(f"Stopped {service}")


stop_services()
