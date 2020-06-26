import ctypes
import sys
import web
import time
import actions


def main():
    if actions.check_pythonw():
        raise RuntimeError("Program already running")
    actions.write_log("run.pyw main")
    if sys.platform == "win32":
        if ctypes.windll.shell32.IsUserAnAdmin() != 0:
            while True:
                time.sleep(1.5)
                web.main()
        else:
            # Re-run with admin rights
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
    elif sys.platform == "linux":
        while True:
            time.sleep(1.5)
            web.main()


if __name__ == "__main__":
    main()
