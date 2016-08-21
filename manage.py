#!/usr/bin/env python
"""Python script for my personal website."""

from flask.ext.script import Manager, Command

from app import create_app

app = create_app("config.py")
manager = Manager(app)


@manager.command
def freeze():
    """Freeze the website into a static version."""
    from flask_frozen import Freezer
    print("freezing...", end="")
    freezer = Freezer(app)
    freezer.freeze()
    print("done!")


if __name__ == "__main__":
    manager.run()
