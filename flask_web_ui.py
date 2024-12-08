from flask import Flask, request, jsonify, render_template
import logging

from config import *

logger = logging.getLogger(__name__)

# Set logging format
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

app = Flask(__name__)

# Global settings dictionary
settings = {
    "auto_accept_enabled": True,
    "auto_lock_in_enabled": False,
    "auto_ban_enabled": False,
}

# Auto lock-in list of champions
auto_lock_in_champions = []

# Auto ban list of champions
auto_ban_list_champions = []

@app.route('/')
def serve_settings():
    # Serve the settings page HTML
    return render_template('settings.html', settings=settings)

@app.route('/update', methods=['POST'])
def update_settings():
    global settings
    global auto_lock_in_champions, auto_ban_list_champions

    data = request.get_json()

    setting = data['setting']
    value = data['value']

    if setting == 'auto_lock_in_champions':
        # Setting lock-in champions list
        auto_lock_in_champions = value
    elif setting == 'auto_ban_list_champions':
        # Setting ban champions list
        auto_ban_list_champions = value
    else:
        # Setting global settings
        settings[setting] = value

    # Log the new updated settings
    logger.info(f"{setting} updated to {value}")

    return jsonify({"message": f"{setting} updated to {value}", "settings": settings})

# Start Flask server
def start_flask_server():
    app.run(port=PORT)
