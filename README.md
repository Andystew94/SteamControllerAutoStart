# SteamControllerAutoStart

SteamControllerAutoStart will start big picture mode whenever you connect a controller to the PC!
If Steam is already open, no action will take place.
If Steam is closed, the script will not reset until one or all controllers is disconnected.

NOTE: Windows Only.

## Building the EXE from the source

```bash
python setup.py build
```

## Installing the script

Run the install.exe as an admin. This will both copy the EXE and all associated files to the local drive ('C:\EmulationTools\SteamControllerAutoStart'), as well as add the script to the Windows Task Scheduler.

Note: This script will run at PC logon and continue running until stopped manually.

Alternative you can copy and paste the SteamControllerAutoStart.exe into its own folder, in a location you prefer. However if you do this, you will need to manually set up the script in the Windows Task Scheduler.
