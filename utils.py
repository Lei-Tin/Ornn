import sys

import logging
import psutil

from config import *


logger = logging.getLogger(__name__)

# Set logging format
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Helper function to check if a process with a given PID exists
def pid_exists(pid):
    """Check if a process with a given PID exists."""
    try:
        psutil.Process(pid)  # Try to get process info using psutil
        return True
    except psutil.NoSuchProcess:
        return False
    except psutil.AccessDenied:
        return False
    except Exception as e:
        logger.error(f"Error while checking PID {pid}: {e}")
        return False

# Check if another instance is running
def check_running_instance():
    if os.path.exists(LOCK_FILE):
        try:
            with open(LOCK_FILE, "r") as f:
                pid = int(f.read().strip())

            if pid_exists(pid):
                return True
            else:
                # Stale lock file, remove it
                try:
                    os.remove(LOCK_FILE)
                except Exception as e:
                    logger.error(f"Failed to remove stale lock file: {e}")
                    return True
        except (ValueError, FileNotFoundError):
            # If lock file is corrupted or unreadable, remove it
            try:
                os.remove(LOCK_FILE)
            except Exception as e:
                logger.error(f"Failed to remove corrupted lock file: {e}")
                return True

    # Create a new lock file with the current PID
    try:
        with open(LOCK_FILE, "w") as f:
            f.write(str(os.getpid()))
    except Exception as e:
        logger.error(f"Failed to create lock file: {e}")
        return True
    return False

# Clean up the lock file when exiting
def cleanup_lock_file():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)