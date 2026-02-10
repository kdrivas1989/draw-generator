#!/usr/bin/env python3
"""
Draw Generator - macOS Native App
Wraps the Flask web application in a native macOS window using pywebview.
"""

import os
import sys
import threading
import webview
from flask import Flask, render_template, send_from_directory

# Determine if we're running as a bundled app or from source
if getattr(sys, 'frozen', False):
    # Running as a bundled app
    bundle_dir = os.path.dirname(sys.executable)
    # For py2app, resources are in ../Resources relative to MacOS
    if sys.platform == 'darwin':
        bundle_dir = os.path.join(os.path.dirname(bundle_dir), 'Resources')
    template_folder = os.path.join(bundle_dir, 'templates')
    static_folder = os.path.join(bundle_dir, 'static')
else:
    # Running from source
    bundle_dir = os.path.dirname(os.path.abspath(__file__))
    template_folder = os.path.join(bundle_dir, 'templates')
    static_folder = os.path.join(bundle_dir, 'static')

# Create Flask app with correct paths
app = Flask(__name__,
            template_folder=template_folder,
            static_folder=static_folder)

# Disable Flask's reloader to prevent issues with pywebview
app.config['DEBUG'] = False


@app.route('/')
def index():
    """Draw generator page for creating competition draws based on USPA or SVNH rules."""
    return render_template('index.html')


@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files."""
    return send_from_directory(static_folder, filename)


def start_flask():
    """Start the Flask server in a separate thread."""
    app.run(host='127.0.0.1', port=5002, threaded=True, use_reloader=False)


def main():
    """Main entry point for the macOS app."""
    # Start Flask in a background thread
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()

    # Give Flask a moment to start
    import time
    time.sleep(0.5)

    # Create the native window
    window = webview.create_window(
        title='Draw Generator',
        url='http://127.0.0.1:5002',
        width=1200,
        height=900,
        min_size=(800, 600),
        resizable=True,
        background_color='#111827',  # Match the app's dark theme
        text_select=True,
    )

    # Start the webview (this blocks until the window is closed)
    webview.start()


if __name__ == '__main__':
    main()
