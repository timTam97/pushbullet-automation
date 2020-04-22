import ctypes
import sys
import subprocess


def hibernate():
    if sys.platform == "win32":
        subprocess.run(["psshutdown", "-h", "-t", "0"])
    elif sys.platform == "linux":
        pass  # idk how to hibernate on linux


def sleep():
    if sys.platform == "win32":
        subprocess.run(["psshutdown", "-d", "-t", "0"])
    elif sys.platform == "linux":
        subprocess.run(["systemctl", "suspend"])


def shut_down():
    if sys.platform == "win32":
        subprocess.run(["shutdown", "/s", "/t", "0"])
    elif sys.platform == "linux":
        subprocess.run(["systemctl", "suspend"])


def open_vnc():
    if sys.platform == "win32":
        if ctypes.windll.shell32.IsUserAnAdmin() != 0:
            subprocess.run(
                [
                    "C:",
                    "&&",
                    "cd",
                    "C:\Program Files\RealVNC\VNC Server\\",
                    "&&",
                    "vncserver.exe",
                    "-start",
                ],
                shell=True,
            )


def lock():
    if sys.platform == "win32":
        ctypes.windll.user32.LockWorkStation()
    elif sys.platform == "linux":
        pass  # TODO
