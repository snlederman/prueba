import sys
import os

# Insert the parent directory (which contains app.py) into sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))