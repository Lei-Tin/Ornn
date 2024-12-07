# Ornn

Ornn is a script that utilizes LCU Driver to interact with the League of Legends client

The implementation is based of League of Legends Client being implicitly a server. The script sends requests to the client server to perform certain actions. 

**I am not responsible for any bans or penalties that may occur from using this script. Use at your own risk.**

A demo video  is available [here](https://youtu.be/kbaFEfyMxG0)

## Logo Credits
- Logo made by @nakiyande, [Twitter (X)](https://x.com/nakiyande)

## Features

### Current
- [x] Auto accept ready checks when you queue up
- [x] Customize settings using a web interface with Flask launched at `localhost:5000`
- [x] System tray icon to open settings and exit the application

### TODO
- [ ] Select from a list of champions to auto select when it is your turn
- [ ] Select from a list of champions to ban when it is your turn

## How to use (Run from source)

1. Get Python, the version I used is Python 3.11.10
2. Install the required packages using `pip install -r requirements.txt`
3. Run the script using `python ornn.py`
4. Check your system tray for the Ornn icon, right click to enter configuration or exit the application
5. Open your League of Legends client and enjoy from there!

## How to use (Run from executable)

1. Download the latest release from the releases tab
2. Run the executable
3. Enjoy!

## Compatibility

- Currently tested on Windows 11
- Not tested on Mac yet
- Executable is compiled using PyInstaller

## Build instructions

### Building on Windows with `pyinstaller`
- With running log `pyinstaller.exe --onefile --add-data "templates:templates" --add-data "static:static" --icon .\static\images\ornn.ico .\Ornn.py`
- Without running log `pyinstaller.exe --windowed --onefile --add-data "templates:templates" --add-data "static:static" --icon .\static\images\ornn.ico .\Ornn.py`