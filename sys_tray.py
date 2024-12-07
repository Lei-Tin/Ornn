from pystray import Icon, Menu, MenuItem
from PIL import Image

import webbrowser
import os
import logging

from config import *
from utils import resource_path, cleanup_lock_file

logger = logging.getLogger(__name__)

# Set logging format
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

# Function to create the tray icon
def load_icon():
    return Image.open(resource_path("static/images/ornn.jpg"))

# Open the Flask UI in the default browser
def open_config():
    logger.debug("Opening config in browser")
    webbrowser.open(f"http://localhost:{PORT}")

# Stop the entire application
def stop_application(icon):
    icon.stop()
    cleanup_lock_file()
    logger.debug("Exiting application")
    os._exit(0)

# Setup the system tray icon
def setup_tray():
    icon = Icon(
        "Ornn",
        load_icon(),
        title="Ornn",
        menu=Menu(
            MenuItem('Ornn v1.0', lambda: logger.debug('How did you even trigger this?'), enabled=False),
            MenuItem("Open Config", lambda: open_config()),
            MenuItem("Exit", lambda: stop_application(icon))
        )
    )
    icon.run()