from setuptools import setup, find_packages
import os
from shutil import copyfile
import subprocess

# Required packages for steamcontrollerautostart.py
try:
    from PyInstaller import __main__ as pyi
except ImportError:
    subprocess.check_call(['pip', 'install', 'PyInstaller'])
    from PyInstaller import __main__ as pyi

try:
    import psutil
except ImportError as e:
    try:
        subprocess.check_call(['pip', 'install', 'psutil'])
        import psutil
    except Exception as install_error:
        print(f"Error installing module: {install_error}")

try:
    import pygame
except ImportError as e:
    try:
        subprocess.check_call(['pip', 'install', 'pygame'])
        import pygame
    except Exception as install_error:
        print(f"Error installing module: {install_error}")

working_directory = os.path.join(os.getcwd())

setup(
    name='SteamControllerAutoStart',
    version='1.0',
    description='SteamControllerAutoStart Script',
    author='Andrew S',
    packages=find_packages(),
    executables=[
        pyi.run([
            'steamcontrollerautostart.py',
            '--onefile',
            '--distpath', 'release',
            '--name', 'SteamControllerAutoStart.exe',
            '--noconsole'
        ])
    ]
)

# Copy the README.md to the release folder
copyfile(os.path.join(working_directory, 'README.md'),
         os.path.join(working_directory, 'release', 'README.md'))

setup(
    name='SteamControllerAutoStart_Installer',
    version='1.0',
    description='SteamControllerAutoStart Installer',
    author='Andrew S',
    packages=find_packages(),
    executables=[
        pyi.run([
            'install.py',
            '--onefile',
            '--distpath', 'release',
            '--name', 'install.exe',
            '--console'
        ])
    ]
)
