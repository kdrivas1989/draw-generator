"""
py2app setup script for Draw Generator macOS app.

Build with:
    python setup.py py2app

For development testing:
    python setup.py py2app -A
"""

from setuptools import setup
import os

# Get the directory containing setup.py
HERE = os.path.dirname(os.path.abspath(__file__))

# App metadata
APP_NAME = 'Draw Generator'
APP_VERSION = '1.0.0'
APP_BUNDLE_ID = 'com.drawgenerator.app'

# Main app entry point
APP = ['macos_app.py']

# Data files to include
DATA_FILES = [
    ('templates', ['templates/index.html']),
]

# Include all static files
static_dir = os.path.join(HERE, 'static')
for root, dirs, files in os.walk(static_dir):
    if files:
        rel_path = os.path.relpath(root, HERE)
        file_paths = [os.path.join(root, f) for f in files if not f.startswith('.')]
        if file_paths:
            DATA_FILES.append((rel_path, file_paths))

# py2app options
OPTIONS = {
    'argv_emulation': False,
    'iconfile': None,  # Add path to .icns file if you have one
    'plist': {
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': APP_NAME,
        'CFBundleIdentifier': APP_BUNDLE_ID,
        'CFBundleVersion': APP_VERSION,
        'CFBundleShortVersionString': APP_VERSION,
        'LSMinimumSystemVersion': '10.13',
        'NSHighResolutionCapable': True,
        'NSRequiresAquaSystemAppearance': False,  # Support dark mode
        'CFBundleDevelopmentRegion': 'English',
    },
    'packages': [
        'flask',
        'webview',
        'jinja2',
        'werkzeug',
    ],
    'includes': [
        'webview.platforms.cocoa',
    ],
    'excludes': [
        'tkinter',
        'test',
        'unittest',
    ],
    'resources': [],
    'site_packages': True,
}

setup(
    name=APP_NAME,
    version=APP_VERSION,
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
