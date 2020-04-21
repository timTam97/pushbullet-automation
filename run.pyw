import ctypes
import sys
import wss
import websocket
from api_key import get_key

if __name__ == "__main__":
    if ctypes.windll.shell32.IsUserAnAdmin() != 0:
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(
            "wss://stream.pushbullet.com/websocket/" + get_key(),
            on_message=wss.on_message,
            on_error=wss.on_error,
            on_close=wss.on_close,
        )
        ws.on_open = wss.on_open
        ws.run_forever()
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
