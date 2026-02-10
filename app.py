#!/usr/bin/env python3
"""Draw Generator - Standalone draw generation for skydiving competitions."""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    """Draw generator page for creating competition draws based on USPA or SVNH rules."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=5002, debug=True)
