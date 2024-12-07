from flask import Flask, request, jsonify, render_template, url_for
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
}

@app.route('/')
def home():
    # Serve the settings page HTML
    return render_template('settings.html', settings=settings)

@app.route('/update', methods=['POST'])
def update_settings():
    global settings
    data = request.get_json()
    setting = data['setting']
    value = data['value']
    settings[setting] = value

    # Log the new updated settings
    logger.info(f"{setting} updated to {value}")

    return jsonify({"message": f"{setting} updated to {value}", "settings": settings})

# Start Flask server
def start_flask_server():
    app.run(port=PORT)
