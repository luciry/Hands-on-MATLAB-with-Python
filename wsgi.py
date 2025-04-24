"""
WSGI config for MATLAB with Python Integration project.
This module contains the WSGI application used by production servers.
"""

import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the Flask app
from webapp.app import app

# For running directly
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)