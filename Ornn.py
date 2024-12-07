import threading
import asyncio
import nest_asyncio

from lcu_driver import Connector

import os
import sys

import logging

from tkinter import Tk, messagebox

from sys_tray import setup_tray
from flask_web_ui import start_flask_server, settings

from config import *
from utils import check_running_instance, cleanup_lock_file

logger = logging.getLogger(__name__)

# Set logging format
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

# Patch asyncio to allow nested event loops
nest_asyncio.apply()

# Initialize LCU Connector
connector = Connector()

def show_dialog():
    root = Tk()
    root.withdraw()  # Hide the root window
    messagebox.showerror("Another Ornn is running", "Another instance of Ornn is already running!")
    root.destroy()

# LCU Connector event handlers
@connector.ready
async def connect(connection):
    logger.info('LCU Client Attached')

@connector.ws.register('/lol-matchmaking/v1/search', event_types=('CREATE',))
async def matchmaking_started(connection, event):
    logger.debug("Matchmaking started.")

@connector.ws.register('/lol-matchmaking/v1/ready-check', event_types=('UPDATE', ))
async def matchmaking_ready_check(connection, event):
    # This update event is triggered every second
    # So I want to cut down the amount of logs
    if settings["auto_accept_enabled"]:
        # Ready check data has the following format
        # {
        #     'declinerIds': [],
        #     'dodgeWarning': 'None',
        #     'playerResponse': 'Declined',
        #     'state': 'InProgress',
        #     'suppressUx': False,
        #     'timer': 4.0
        # }

        # We only care about playerResponse and state
        if event.data["playerResponse"] == "Accepted":
            # Don't do anything
            logger.debug("Matchmaking accepted already.")
            return

        if event.data['state'] == 'InProgress' and event.data['playerResponse'] == 'None':
            await asyncio.sleep(1)  # Sleep for 1 second to ensure the ready check is fully loaded
            res = await connection.request("post", "/lol-matchmaking/v1/ready-check/accept")

            if res.status == 200:
                logger.info("Matchmaking accepted.")
            else:
                logger.error("Failed to accept matchmaking.")
    else:
        logger.debug("Auto accept is disabled.")


# Run LCU Connector and Flask concurrently
async def main():
    if check_running_instance():
        show_dialog()
        sys.exit(0)

    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=start_flask_server, daemon=True)
    flask_thread.start()

    # Start the system tray in a separate thread
    tray_thread = threading.Thread(target=setup_tray, daemon=True)
    tray_thread.start()

    try:
        # Wait for LCU Connector
        connector.start()
    finally:
        cleanup_lock_file()

if __name__ == "__main__":
    asyncio.run(main())
