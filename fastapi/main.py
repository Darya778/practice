import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.join(current_dir, '../log'))
from log import log_message
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class SubscriptionRequest(BaseModel):
    topics: List[str]

subscriptions = []

@app.post("/subscribe/")
async def subscribe(request: SubscriptionRequest):
    global subscriptions
    subscriptions.extend(request.topics)
    subscriptions = list(set(subscriptions))
    log_message("info", "200 OK Subscribed to topics", "fastapi/main.py")
    return {"message": "Subscribed to topics", "topics": subscriptions}

@app.get("/subscriptions/")
async def get_subscriptions():
    log_message("info", "200 OK Get subscriptions", "fastapi/main.py")
    return {"subscriptions": subscriptions}

@app.get("/receivers/")
async def get_receivers():
    file_path = "/home/dasha/wotiwan/orchestrator/daemons_to_load.txt"
    try:
        with open(file_path, "r") as file:
            receivers = [line.strip() for line in file.readlines()]
            log_message("info", "200 OK Get receivers", "fastapi/main.py")
        return {"receivers": receivers}
    except FileNotFoundError:
        log_message("error", "404 - Receivers file not found", "fastapi/main.py")
        return {"error": "Receivers file not found"}, 404

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8010)
