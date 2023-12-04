import time
import subprocess
import pygame
import psutil
import sys
import os


def is_controller_connected():
    pygame.init()
    time.sleep(1)
    joystick_count = pygame.joystick.get_count()
    pygame.quit()
    return joystick_count > 0


def launch_steam_big_picture(steam_path):
    try:
        subprocess.Popen([steam_path, "-bigpicture"])
    except Exception as e:
        print(f"Error launching Steam: {e}")


def is_steam_running():
    return any(process.info['name'] == 'steam.exe' for process in psutil.process_iter(['pid', 'name']))


def find_steam_exe():
    connected_drives = [drive.device for drive in psutil.disk_partitions()]
    for drive in connected_drives:
        for foldername, _, filenames in os.walk(os.path.join(drive, '')):
            if os.path.basename(foldername) == "Steam" and "steam.exe" in filenames:
                return os.path.join(foldername, "steam.exe")
    raise FileNotFoundError("Steam.exe not found")


def main():
    controller_connected_flag = False
    polling_interval = 5

    try:
        steam_path = find_steam_exe()
    except FileNotFoundError as e:
        print(e)
        sys.exit()

    while True:
        # Launch Big Picture if controller connected > 0
        if is_controller_connected():
            launch_steam_big_picture(steam_path)
            controller_connected_flag = True

        # Monitor Steam process and exit while loop when closed
        while is_steam_running():
            if not controller_connected_flag:
                # Steam was already on prior to the controller being connected
                controller_connected_flag = True
            time.sleep(polling_interval)

        # Wait until all controllers have been turned off
        while controller_connected_flag and is_controller_connected():
            pass
        controller_connected_flag = False


if __name__ == "__main__":
    main()
