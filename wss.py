from api_key import get_key
import requests
import json
import time
import websocket
import time
import subprocess
import sys

SUBSCRIPTION_NAME = "Push2Run LENOVO-TIM"
recent_time = time.time()


def on_message(ws, message):
    global recent_time
    # print("message")
    # print(message)
    content = json.loads(message)
    sub = content.get("subtype")
    if sub == "push":
        response = grab_push()
        title = response[0]
        body = response[1]
        time = response[2]
        dismissed = response[3]

        if title == SUBSCRIPTION_NAME and body is not None and not dismissed:
            recent_time = time
            process_command(body)


def grab_push():
    url = "https://api.pushbullet.com/v2/pushes"
    headers = {
        "Access-Token": get_key(),
    }
    # fmt: off
    params = {
        "active": "true", 
        "modified_after": recent_time
    }
    # fmt: on
    r = requests.get(url, headers=headers, params=params).json()
    return (
        r.get("pushes")[0].get("title"),
        r.get("pushes")[0].get("body"),
        r.get("pushes")[0].get("modified"),
        r.get("pushes")[0].get("dismissed"),
    )


def process_command(command):
    if command == "sleep":
        if sys.platform == "win32":
            # print("sleep")
            subprocess.run(["psshutdown", "-d", "-t", "0"])
        elif sys.platform == "linux":
            subprocess.run(["systemctl", "suspend"])
    elif command == "hibernate":
        if sys.platform == "win32":
            # print("hibernate")
            subprocess.run(["psshutdown", "-h", "-t", "0"])
        elif sys.platform == "linux":
            pass  # idk how to hibernate on linux
    elif command == "shut down":
        if sys.platform == "win32":
            # print("sdwn")
            subprocess.run(["shutdown", "/s", "/t", "0"])
        elif sys.platform == "linux":
            subprocess.run(["systemctl", "suspend"])


def on_error(ws, error):
    # print("error")
    print(error)


def on_close(ws):
    print("closed.")


def on_open(ws):
    pass
    # print("open")


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
