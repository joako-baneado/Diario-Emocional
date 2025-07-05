#!/usr/bin/env python3
# main.py - Entry point for the Emotional Diary GUI application
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.simple_gui import main

if __name__ == "__main__":
    main()