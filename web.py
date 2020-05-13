from api_key import key
import actions
import requests
import json
import time
import websocket

SUBSCRIPTION_NAME = "LENOVO-TIM"
recent_time = time.time()


def on_message(ws, message):
    global recent_time
    content = json.loads(message)
    sub = content.get("subtype")
    if sub == "push":
        response = grab_push()
        title = response[0]
        body = response[1]
        time = response[2]
        dismissed = response[3]
        sender = response[4]

        if (
            title == SUBSCRIPTION_NAME
            and body is not None
            and not dismissed
            and sender == "IFTTT"
        ):
            actions.write_log("command: " + body)
            recent_time = time
            process_command(body)


def grab_push():
    url = "https://api.pushbullet.com/v2/pushes"
    headers = {
        "Access-Token": key(),
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
    elif command == "open vnc":
        actions.open_vnc()
    elif command == "lock":
        actions.lock()


def on_error(ws, error):
    print(error)
    actions.write_log(str(error))


def on_close(ws):
    actions.write_log("closed")


def on_open(ws):
    actions.write_log("opened")


def main():
    actions.write_log("web.py main")
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        "wss://stream.pushbullet.com/websocket/" + key(),
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.on_open = on_open
    ws.run_forever()


if __name__ == "__main__":
    main()
