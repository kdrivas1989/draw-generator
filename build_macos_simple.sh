#!/bin/bash
# Simple macOS app builder for Draw Generator
# Creates a standalone .app bundle that runs the Flask server in a web view

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_NAME="Draw Generator"
APP_DIR="$SCRIPT_DIR/dist/${APP_NAME}.app"
CONTENTS_DIR="$APP_DIR/Contents"
MACOS_DIR="$CONTENTS_DIR/MacOS"
RESOURCES_DIR="$CONTENTS_DIR/Resources"

echo "Creating macOS app bundle..."

# Clean and create directories
rm -rf "$APP_DIR"
mkdir -p "$MACOS_DIR"
mkdir -p "$RESOURCES_DIR"
mkdir -p "$RESOURCES_DIR/templates"
mkdir -p "$RESOURCES_DIR/static"

# Copy resources
cp -r "$SCRIPT_DIR/templates/"* "$RESOURCES_DIR/templates/"
cp -r "$SCRIPT_DIR/static/"* "$RESOURCES_DIR/static/"

# Copy icon
if [ -f "$SCRIPT_DIR/DrawGenerator.icns" ]; then
    cp "$SCRIPT_DIR/DrawGenerator.icns" "$RESOURCES_DIR/AppIcon.icns"
fi

# Create Info.plist
cat > "$CONTENTS_DIR/Info.plist" << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>en</string>
    <key>CFBundleExecutable</key>
    <string>DrawGenerator</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon</string>
    <key>CFBundleIdentifier</key>
    <string>com.drawgenerator.app</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>Draw Generator</string>
    <key>CFBundleDisplayName</key>
    <string>Draw Generator</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSSupportsAutomaticGraphicsSwitching</key>
    <true/>
</dict>
</plist>
PLIST

# Create launcher script
cat > "$MACOS_DIR/DrawGenerator" << 'LAUNCHER'
#!/bin/bash

# Get the directory where the app bundle is located
APP_DIR="$(cd "$(dirname "$0")/../.."; pwd)"
RESOURCES_DIR="$APP_DIR/Contents/Resources"

# Change to resources directory so Flask can find templates/static
cd "$RESOURCES_DIR"

# Find Python 3
PYTHON=""
if command -v python3 &> /dev/null; then
    PYTHON="python3"
elif command -v python &> /dev/null; then
    PYTHON="python"
fi

if [ -z "$PYTHON" ]; then
    osascript -e 'display alert "Python Required" message "Python 3 is required to run Draw Generator. Please install Python from python.org."'
    exit 1
fi

# Check for required packages
$PYTHON -c "import flask, webview" 2>/dev/null
if [ $? -ne 0 ]; then
    osascript -e 'display alert "Missing Dependencies" message "Required Python packages are missing. Please run: pip3 install flask pywebview"'
    exit 1
fi

# Run the app
$PYTHON << 'PYTHONCODE'
import os
import sys
import threading
import webview
from flask import Flask, render_template, send_from_directory

# Set up paths
RESOURCES_DIR = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))) + '/Resources'
os.chdir(RESOURCES_DIR)

app = Flask(__name__,
            template_folder=os.path.join(RESOURCES_DIR, 'templates'),
            static_folder=os.path.join(RESOURCES_DIR, 'static'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

def start_flask():
    app.run(host='127.0.0.1', port=5002, debug=False, use_reloader=False)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()

    import time
    time.sleep(0.5)

    window = webview.create_window(
        title='Draw Generator',
        url='http://127.0.0.1:5002',
        width=1200,
        height=900,
        background_color='#111827'
    )
    webview.start()
PYTHONCODE
LAUNCHER

chmod +x "$MACOS_DIR/DrawGenerator"

echo ""
echo "================================================"
echo "  macOS App Created Successfully!"
echo "================================================"
echo ""
echo "App location: $APP_DIR"
echo ""
echo "Requirements:"
echo "  - Python 3"
echo "  - pip3 install flask pywebview"
echo ""
echo "You can now double-click the app to run it!"
