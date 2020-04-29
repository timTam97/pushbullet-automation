import ctypes
import sys
import web


def main():
    if sys.platform == "win32":
        if ctypes.windll.shell32.IsUserAnAdmin() != 0:
            while True:
                web.main()
        else:
            # Re-run with admin rights
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
    elif sys.platform == "linux":
        while True:
            web.main()


if __name__ == "__main__":
    main()
