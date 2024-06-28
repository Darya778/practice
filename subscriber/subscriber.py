import time
import threading
import paho.mqtt.client as mqtt
import requests
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.join(current_dir, '../log'))

message_timer = None


def reset_timer():
    global message_timer
    if message_timer:
        message_timer.cancel()
    message_timer = threading.Timer(60, on_timeout)
    message_timer.start()


def on_message(client, userdata, message):
    print(f"Received message on topic {message.topic}: {message.payload.decode()}")
    reset_timer()

def subscribe_to_topics(topics):
    mqtt_client = mqtt.Client()
    mqtt_client.on_message = on_message
    mqtt_client.connect("localhost", 1884, 60)
    mqtt_client.subscribe([(topic, 0) for topic in topics])
    reset_timer()  # Запуск таймера при подключении к теме
    mqtt_client.loop_forever()
    
def get_receivers():
    try:
        url = "http://localhost:8010/receivers/"
        response = requests.get(url)
        if response.status_code == 200:
            receivers = response.json().get("receivers", [])
            log_message("info", "200 OK Get receivers")
            return receivers
        else:
            print(f"Failed to get receivers: {response.text}")
            log_message("error", f"Failed to get receivers: {response.text}")
            return []
    except Exception as e:
        log_message("error",f"Error occurred while fetching receivers: {e}")
        print(f"Error occurred while fetching receivers: {e}")
        return []

if __name__ == "__main__":
    log_message("info", "200 OK")
    get_receivers_choice = input("Do you want to get the list of receivers? (yes/no): ").strip().lower()
    if get_receivers_choice == 'yes':
        receivers = get_receivers()
        if receivers:
            log_message("info", "200 OK Get available receivers")
            print(f"Available receivers: {', '.join(receivers)}")
        else:
            log_message("error", "No receivers found or failed to fetch receivers")
            print("No receivers found or failed to fetch receivers.")

    user_input = input("Enter the topics you want to subscribe to, separated by commas: ")
    topics = [topic.strip() for topic in user_input.split(',')]

    try:
        url = "http://localhost:8010/subscribe/"
        response = requests.post(url, json={"topics": topics})
        if response.status_code == 200:
            log_message("info", f"200 OK Subscribed to topics via HTTP: {topics}")
            print(f"Subscribed to topics via HTTP: {topics}")
        else:
            log_message("error", f"Failed to subscribe via HTTP: {response.text}")
            print(f"Failed to subscribe via HTTP: {response.text}")

        subscribe_to_topics(topics)

    except Exception as e:
        log_message("error", f"Error occurred: {e}")
        print(f"Error occurred: {e}")
