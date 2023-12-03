import os
import shutil
from subprocess import call, check_output, check_call
import importlib

try:
    import psutil
except:
    check_call(['pip', 'install', 'psutil'])
    import psutil


def check_and_install_package(package_name):
    try:
        module = importlib.import_module(package_name)
        print(
            f"{package_name} is installed. Version: {getattr(module, '__version__', 'N/A')}")
    except ImportError:
        print(f"{package_name} is not installed. Installing...")
        install_python_package(package_name)
        print(f"{package_name} has been installed successfully.")


def identify_missing_packages(packages_to_check):
    for package in packages_to_check:
        check_and_install_package(package)


def install_python_package(module_name):
    check_call(['pip', 'install', module_name])


def task_exists(task_name):
    try:
        check_output(['schtasks', '/query', '/tn', task_name])
        print("## Existing task found in Task Scheduler ##")
        return True
    except Exception:
        return False


def remove_task(task_name):
    call(['schtasks', '/delete', '/tn', task_name, '/f'])
    print("## Removing existing task found in Task Scheduler ##")


def cleanup_build_folders(folders_to_delete):
    for folder in folders_to_delete:
        folder_path = os.path.join(os.path.dirname(__file__), folder)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            print(f"Deleted: {folder_path}")
        else:
            print(f"{folder} does not exist.")


def terminate_process(process_name):
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == process_name:
            try:
                pid = process.info['pid']
                p = psutil.Process(pid)
                p.terminate()
                print(f"Terminated process {process_name} with PID {pid}")
            except Exception as e:
                print(f"Error terminating process {process_name}: {e}")


def main():
    # List of packages to check
    packages_to_check = ['PyInstaller', 'pygame', 'psutil']

    # Check for missing python packages required for steamcontrollerautostart.py
    identify_missing_packages(packages_to_check)

    process_name_to_terminate = "SteamControllerAutoStart.exe"
    terminate_process(process_name_to_terminate)

    script_directory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_directory)

    script_name = 'steamcontrollerautostart.py'
    executable_name = 'SteamControllerAutoStart.exe'
    installation_path = 'C:\\Program Files\\SteamControllerAutoStart'
    task_name = 'SteamControllerAutoStartTask'

    # List of folders to delete
    folders_to_delete = ['build', 'dist']

    # Remove existing task if it exists
    if task_exists(task_name):
        remove_task(task_name)

    # Build the executable using PyInstaller
    call(['python', '-m', 'PyInstaller', '--onefile', '--noconsole', '--name',
          os.path.splitext(executable_name)[0], os.path.join(script_directory, script_name)])

    # Identify the correct path to the executable
    dist_directory = os.path.join(script_directory, 'dist')
    executable_path = os.path.join(dist_directory, executable_name)

    if not os.path.exists(executable_path):
        # Try an alternative path if 'dist' is not found
        executable_path = os.path.join(script_directory, executable_name)

    if not os.path.exists(executable_path):
        raise FileNotFoundError(f"Executable not found: {executable_path}")

    # Create the destination directory if it doesn't exist
    os.makedirs(installation_path, exist_ok=True)

    # Copy the executable to the installation directory using shutil
    shutil.copy(executable_path, os.path.join(
        installation_path, executable_name))

    # Add task to Windows Task Scheduler
    call(['schtasks', '/create', '/tn', task_name, '/tr',
          f'"{installation_path}\\{executable_name}"', '/sc', 'onlogon'])

    # Remove all build folders
    cleanup_build_folders(folders_to_delete)

    # Prompt the user to restart their PC
    restart_confirmation = input(
        "Installation complete. Do you want to restart your PC now? (y/n): ").lower()

    if restart_confirmation == 'y':
        call(['shutdown', '/r', '/t', '1'])
    else:
        print("Please restart your PC manually to apply changes.")


if __name__ == "__main__":
    main()
