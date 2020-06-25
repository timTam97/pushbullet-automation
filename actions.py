import ctypes
import sys
import subprocess
import datetime


def hibernate():
    if sys.platform == "win32":
        ctypes.windll.PowrProf.SetSuspendState(True, False, False)


def sleep():
    if sys.platform == "win32":
        ctypes.windll.PowrProf.SetSuspendState(False, False, False)
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
                    "C:\\Program Files\\RealVNC\\VNC Server\\",
                    "&&",
                    "vncserver.exe",
                    "-start",
                ],
                shell=True,
            )


def write_log(event):
    with open("run.log", "a") as f:
        to_write = "[" + str(datetime.datetime.today())[:-7] + "] "
        to_write += str(event) + "\n"
        f.write(to_write)


def lock():
    if sys.platform == "win32":
        ctypes.windll.user32.LockWorkStation()
    elif sys.platform == "linux":
        subprocess.run(["gnome-screensaver-command", "-l"])


def get_comp_name():
    if sys.platform == "win32":
        strbuf = ctypes.create_unicode_buffer(16)
        size = ctypes.byref(ctypes.c_int(len(strbuf)))
        # username: Advapi32.GetUserNameW
        if ctypes.windll.kernel32.GetComputerNameW(strbuf, size) == 0:
            raise RuntimeError("GetComputerName failed")
        return strbuf.value
    elif sys.platform == "linux":
        return (
            subprocess.run(["uname", "-n"], stdout=subprocess.PIPE)
            .stdout.decode()
            .rstrip()
        )


def check_pythonw():
    if sys.platform == "win32":
        proc = subprocess.Popen(
            'tasklist | findstr "pythonw.exe"', shell=True, stdout=subprocess.PIPE,
        )
        if "pythonw.exe" in proc.communicate()[0].decode("ascii"):
            ctypes.windll.User32.MessageBoxW(
                None,
                "Pushbullet Automation is already running",
                None,
                0x00000000 | 0x00000030,
            )
            return True
        return False
    elif sys.platform == "linux":
        return False  # TODO
