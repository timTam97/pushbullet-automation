from api_key import get_key
import requests
import json
import time
import websocket
import time
import subprocess

SUBSCRIPTION_NAME = "Push2Run LENOVO-TIM"


def on_message(ws, message):
    print("message")
    print(message)
    content = json.loads(message)
    sub = content.get("subtype")
    if sub == "push":
        response = grab_push()
        title = response[0]
        body = response[1]
        if title == SUBSCRIPTION_NAME and body is not None:
            process_command(body)


def grab_push():
    url = "https://api.pushbullet.com/v2/pushes"
    headers = {
        "Access-Token": get_key(),
    }
    # fmt: off
    params = {
        "active": "true", 
        "modified_after": int(time.time()) - 10
    }
    # fmt: on
    r = requests.get(url, headers=headers, params=params).json()
    return r.get("pushes")[0].get("title"), r.get("pushes")[0].get("body")


def process_command(command):
    if command == "sleep":
        subprocess.run(["systemctl", "suspend"])
    elif command == "hibernate":
        pass  # idk how to hibernate on linux
    elif command == "shut down":
        subprocess.run(["poweroff"])  # untested


def on_error(ws, error):
    print("error")
    print(error)


def on_close(ws):
    print("closed.")


def on_open(ws):
    print("open")


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        "wss://stream.pushbullet.com/websocket/" + get_key(),
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.on_open = on_open
    ws.run_forever()
