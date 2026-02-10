#!/bin/bash
# Script to create iOS/iPadOS app for Draw Generator
# This prepares the web content and creates the Xcode project structure

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
IOS_DIR="$SCRIPT_DIR"

echo "================================================"
echo "  Draw Generator - iOS/iPadOS App Setup"
echo "================================================"
echo ""

# Create web directory and copy web content
echo "Step 1: Preparing web content..."
mkdir -p "$IOS_DIR/DrawGenerator/DrawGenerator/web/static/css"
mkdir -p "$IOS_DIR/DrawGenerator/DrawGenerator/web/static/formations"

# Copy the HTML template (modify paths for local file access)
sed 's|/static/|static/|g' "$PROJECT_ROOT/templates/index.html" > "$IOS_DIR/DrawGenerator/DrawGenerator/web/index.html"

# Copy static assets
cp "$PROJECT_ROOT/static/css/tailwind.css" "$IOS_DIR/DrawGenerator/DrawGenerator/web/static/css/"
cp "$PROJECT_ROOT/static/formations/"*.png "$IOS_DIR/DrawGenerator/DrawGenerator/web/static/formations/"

echo "Step 2: Creating Assets catalog..."
mkdir -p "$IOS_DIR/DrawGenerator/DrawGenerator/Assets.xcassets/AppIcon.appiconset"
mkdir -p "$IOS_DIR/DrawGenerator/DrawGenerator/Assets.xcassets/LaunchBackground.colorset"

# Copy app icons
cp "$PROJECT_ROOT/DrawGenerator.iconset/icon_1024x1024.png" "$IOS_DIR/DrawGenerator/DrawGenerator/Assets.xcassets/AppIcon.appiconset/"

# Create AppIcon Contents.json
cat > "$IOS_DIR/DrawGenerator/DrawGenerator/Assets.xcassets/AppIcon.appiconset/Contents.json" << 'ICONJSON'
{
  "images" : [
    {
      "filename" : "icon_1024x1024.png",
      "idiom" : "universal",
      "platform" : "ios",
      "size" : "1024x1024"
    }
  ],
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}
ICONJSON

# Create LaunchBackground color
cat > "$IOS_DIR/DrawGenerator/DrawGenerator/Assets.xcassets/LaunchBackground.colorset/Contents.json" << 'COLORJSON'
{
  "colors" : [
    {
      "color" : {
        "color-space" : "srgb",
        "components" : {
          "alpha" : "1.000",
          "blue" : "0.153",
          "green" : "0.094",
          "red" : "0.067"
        }
      },
      "idiom" : "universal"
    }
  ],
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}
COLORJSON

# Create Assets.xcassets Contents.json
cat > "$IOS_DIR/DrawGenerator/DrawGenerator/Assets.xcassets/Contents.json" << 'ASSETSJSON'
{
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}
ASSETSJSON

echo ""
echo "================================================"
echo "  Setup Complete!"
echo "================================================"
echo ""
echo "Web content prepared at:"
echo "  $IOS_DIR/DrawGenerator/DrawGenerator/web/"
echo ""
echo "To create the Xcode project:"
echo "1. Open Xcode"
echo "2. Create a new iOS App project named 'DrawGenerator'"
echo "3. Choose SwiftUI as the interface"
echo "4. Save it to: $IOS_DIR/DrawGenerator/"
echo "5. Replace the generated files with the ones in DrawGenerator/"
echo "6. Add the 'web' folder to the project (Create folder references)"
echo "7. Build and run!"
echo ""
echo "Files count:"
ls -la "$IOS_DIR/DrawGenerator/DrawGenerator/web/static/formations/" | wc -l
echo "formation images copied"
