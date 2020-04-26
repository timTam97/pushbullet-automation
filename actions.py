import ctypes
import sys
import subprocess
import datetime


def hibernate():
    if sys.platform == "win32":
        subprocess.run(["psshutdown", "-h", "-t", "0"])
    elif sys.platform == "linux":
        subprocess.run(["systemctl", "hibernate"])  # untested


def sleep():
    if sys.platform == "win32":
        subprocess.run(["psshutdown", "-d", "-t", "0"])
    elif sys.platform == "linux":
        subprocess.run(["systemctl", "suspend"])


def shut_down():
    if sys.platform == "win32":
        subprocess.run(["shutdown", "/s", "/t", "0"])
    elif sys.platform == "linux":
        subprocess.run(["systemctl", "poweroff"])  # untested


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


def write_log(event):
    with open("run.log", "a") as f:
        to_write = "[" + str(datetime.datetime.today()) + "] "
        to_write += event + "\n"
        f.write(to_write)


def lock():
    if sys.platform == "win32":
        ctypes.windll.user32.LockWorkStation()
    elif sys.platform == "linux":
        subprocess.run(["gnome-screensaver-command", "-l"])
