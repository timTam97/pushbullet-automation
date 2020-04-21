import ctypes
import sys
import wss

if __name__ == "__main__":
    if ctypes.windll.shell32.IsUserAnAdmin() != 0:
        wss.main()
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
