import ctypes
import sys
import web


def main():
    if ctypes.windll.shell32.IsUserAnAdmin() != 0:
        web.main()
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )


if __name__ == "__main__":
    main()
