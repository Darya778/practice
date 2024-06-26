import paho.mqtt.client as mqtt
import requests

def on_message(client, userdata, message):
    print(f"Received message on topic {message.topic}: {message.payload.decode()}")

def subscribe_to_topics(topics):
    mqtt_client = mqtt.Client()
    mqtt_client.on_message = on_message
    mqtt_client.connect("localhost", 1884, 60)
    mqtt_client.subscribe([(topic, 0) for topic in topics])
    mqtt_client.loop_forever()

def get_receivers():
    try:
        url = "http://localhost:8010/receivers/"
        response = requests.get(url)
        if response.status_code == 200:
            receivers = response.json().get("receivers", [])
            return receivers
        else:
            print(f"Failed to get receivers: {response.text}")
            return []
    except Exception as e:
        print(f"Error occurred while fetching receivers: {e}")
        return []

if __name__ == "__main__":
    get_receivers_choice = input("Do you want to get the list of receivers? (yes/no): ").strip().lower()
    if get_receivers_choice == 'yes':
        receivers = get_receivers()
        if receivers:
            print(f"Available receivers: {', '.join(receivers)}")
        else:
            print("No receivers found or failed to fetch receivers.")

    user_input = input("Enter the topics you want to subscribe to, separated by commas: ")
    topics = [topic.strip() for topic in user_input.split(',')]

    try:
        url = "http://localhost:8010/subscribe/"
        response = requests.post(url, json={"topics": topics})
        if response.status_code == 200:
            print(f"Subscribed to topics via HTTP: {topics}")
        else:
            print(f"Failed to subscribe via HTTP: {response.text}")

        subscribe_to_topics(topics)

    except Exception as e:
        print(f"Error occurred: {e}")
