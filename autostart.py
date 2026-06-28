import winreg
import sys
from pathlib import Path

APP_NAME = "FileOrganizer"

def enable_autostart():
    if getattr(sys, 'frozen', False):
        exe_path = sys.executable
    else:
        exe_path = str(Path(__file__).parent / "dist" / "organizer.exe")

    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0,
        winreg.KEY_SET_VALUE
    ) as key:
        winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, exe_path)
    print(f"Autostart Enabled: {exe_path}")



def disable_autostart():
    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0,
        winreg.KEY_SET_VALUE
    ) as key:
        try:
            winreg.DeleteValue(key, APP_NAME)
            print("Autostart Disabled")
        except FileNotFoundError:
            print("Autostart Did Not Got Disabled")

if __name__ == "__main__":
    enable_autostart()