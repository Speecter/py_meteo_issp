import sys
import os
import flet as ft

# Ensure src is in the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ui.app import main

if __name__ == "__main__":
    ft.app(target=main)
