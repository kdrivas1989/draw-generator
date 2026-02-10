#!/bin/bash
# Build script for Draw Generator macOS app

set -e

echo "================================================"
echo "  Draw Generator - macOS App Build Script"
echo "================================================"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

echo "Step 1: Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

echo "Step 2: Activating virtual environment..."
source venv/bin/activate

echo "Step 3: Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Step 4: Cleaning previous builds..."
rm -rf build dist

echo "Step 5: Building macOS app..."
python setup.py py2app

echo ""
echo "================================================"
echo "  Build Complete!"
echo "================================================"
echo ""
echo "The app has been created at:"
echo "  $SCRIPT_DIR/dist/Draw Generator.app"
echo ""
echo "To run the app:"
echo "  open \"dist/Draw Generator.app\""
echo ""
echo "To install to Applications:"
echo "  cp -R \"dist/Draw Generator.app\" /Applications/"
echo ""
