import os

#   __ _ _ __  _ __
#  / _` | '_ \| '_ \
# | (_| | |_) | |_) |
#  \__,_| .__/| .__/
#       |_|   |_|

def parent_dir(path):
    """Return the parent of a directory"""
    return os.path.abspath(os.path.join(path, os.pardir))

APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = parent_dir(APP_DIR)

# Normally this would be a security problem if I were to host a live version of
# thie site. However, since I'm using Frozen-Flask to turn this into a static
# site this doesn't matter.
DEBUG = True

#  _____                             _____ _           _
# |  ___| __ ___ _______ _ __       |  ___| | __ _ ___| | __
# | |_ | '__/ _ \_  / _ \ '_ \ _____| |_  | |/ _` / __| |/ /
# |  _|| | | (_) / /  __/ | | |_____|  _| | | (_| \__ \   <
# |_|  |_|  \___/___\___|_| |_|     |_|   |_|\__,_|___/_|\_\

# Freeze to the project root dir (where this file is located)
FREEZER_DESTINATION = PROJECT_ROOT

# TODO: Change this when ready to host on github. Should probably be
# http://brookskindle.github.io
FREEZER_BASE_URL = "http://localhost:5000"

# Prevent Frozen-Flask from removing non-frozen files when it is run. More
# information at http://pythonhosted.org/Frozen-Flask/#getting-started
FREEZER_REMOVE_EXTRA_FILES = False

#  _____ _           _         _____ _       _   ____
# |  ___| | __ _ ___| | __    |  ___| | __ _| |_|  _ \ __ _  __ _  ___  ___
# | |_  | |/ _` / __| |/ /____| |_  | |/ _` | __| |_) / _` |/ _` |/ _ \/ __|
# |  _| | | (_| \__ \   <_____|  _| | | (_| | |_|  __/ (_| | (_| |  __/\__ \
# |_|   |_|\__,_|___/_|\_\    |_|   |_|\__,_|\__|_|   \__,_|\__, |\___||___/
#                                                           |___/

# Tell FlatPages to search for *.md files within the app/pages/ directory
FLATPAGES_ROOT = os.path.join(APP_DIR, "pages")
FLATPAGES_EXTENSION = ".md"
