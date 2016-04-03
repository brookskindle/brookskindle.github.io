#!/usr/bin/env python
"""Python script for my personal website."""

from app import create_app

app = create_app("config.py")

if __name__ == "__main__":
    app.run()
