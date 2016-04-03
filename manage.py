#!/usr/bin/env python
"""Python script for my personal website."""

from flask.ext.script import Manager, Command

from app import create_app


class Freeze(Command):
    """Freezes the website into a static version."""

    def run(self):
        from flask_frozen import Freezer
        freezer = Freezer(app)
        freezer.freeze()

app = create_app("config.py")
manager = Manager(app)
manager.add_command("freeze", Freeze())

if __name__ == "__main__":
    manager.run()
