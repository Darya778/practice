import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.join(current_dir, '../log'))
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
    return {"message": "Subscribed to topics", "topics": subscriptions}

@app.get("/subscriptions/")
async def get_subscriptions():
    return {"subscriptions": subscriptions}

@app.get("/receivers/")
async def get_receivers():
    file_path = "/home/dasha/wotiwan/orchestrator/daemons_to_load.txt"
    try:
        with open(file_path, "r") as file:
            receivers = [line.strip() for line in file.readlines()]
        return {"receivers": receivers}
    except FileNotFoundError:
        return {"error": "Receivers file not found"}, 404

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8010)
