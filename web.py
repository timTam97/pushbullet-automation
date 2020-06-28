import json
import time

import requests
import websocket

import actions
import auth

recent_time = time.time()


def on_message(ws, message):
    global recent_time
    content = json.loads(message)
    sub = content.get("subtype")
    if sub == "push":
        title, body, time_inbound, dismissed, sender = grab_push()
        if (
            title == auth.SUBSCRIPTION_NAME
            and body is not None
            and not dismissed
            and sender == "IFTTT"
        ):
            actions.write_log("command: " + body)
            recent_time = time_inbound
            process_command(body)


def grab_push():
    url = "https://api.pushbullet.com/v2/pushes"
    headers = {
        "Access-Token": auth.key(),
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
        r.get("pushes")[0].get("sender_name"),
    )


def process_command(command):
    if command == "sleep":
        actions.sleep()
    elif command == "hibernate":
        actions.hibernate()
    elif command == "shut down":
        actions.shut_down()
    elif command.lower == "open vnc":
        actions.open_vnc()
    elif command == "lock":
        actions.lock()


def on_error(ws, error):
    actions.write_log(str(error))


def on_close(ws):
    actions.write_log("closed")


def on_open(ws):
    actions.write_log("opened")


def main():
    actions.write_log("web.py main")
    ws = websocket.WebSocketApp(
        "wss://stream.pushbullet.com/websocket/" + auth.key(),
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.on_open = on_open
    ws.run_forever()


if __name__ == "__main__":
    main()
