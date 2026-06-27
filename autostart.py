import winreg
import sys
from pathlib import Path

APP_NAME = "FileOrganizer"

def enable_autostart():
    if getattr(sys, 'frozen', False):
        exe_path = sys.executable
    else:
        exe_path = str(Path(__file__).parent / "dist" / "organizer.exe")

    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0,
        winreg.KEY_SET_VALUE
    )
    winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, exe_path)
    winreg.CloseKey(key)
    print(f"Autostart enabled: {exe_path}")


def disable_autostart():
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0,
        winreg.KEY_SET_VALUE
    )
    try:
        winreg.DeleteValue(key, APP_NAME)
        print("Autostart disabled.")
    except FileNotFoundError:
        print("Autostart was not enabled.")
    winreg.CloseKey(key)


if __name__ == "__main__":
    enable_autostart()