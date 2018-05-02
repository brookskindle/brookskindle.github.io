#!/usr/bin/env python
import pathlib

#  ____      _ _                                     __
# |  _ \ ___| (_) ___ __ _ _ __      ___ ___  _ __  / _|
# | |_) / _ \ | |/ __/ _` | '_ \    / __/ _ \| '_ \| |_
# |  __/  __/ | | (_| (_| | | | |  | (_| (_) | | | |  _|
# |_|   \___|_|_|\___\__,_|_| |_|   \___\___/|_| |_|_|

AUTHOR = "Brooks Kindle"
SITEDESCRIPTION = None
SITENAME = AUTHOR

THEME = str(pathlib.Path.cwd() / "theme")

SITEURL = "https://brookskindle.github.io"
RELATIVE_URLS = True  # Use document-relative URLs when developing

PATH = "content"
STATIC_PATHS = [
    "styles",
]
EXTRA_PATH_METADATA = {
    "styles/dracula.css": {"path": "static/custom.css"},
}

DEFAULT_PAGINATION = 10

TIMEZONE = "America/Los_Angeles"
DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

#  _____ _                                             __
# |_   _| |__   ___ _ __ ___   ___     ___ ___  _ __  / _|
#   | | | '_ \ / _ \ '_ ` _ \ / _ \   / __/ _ \| '_ \| |_
#   | | | | | |  __/ | | | | |  __/  | (_| (_) | | | |  _|
#   |_| |_| |_|\___|_| |_| |_|\___|   \___\___/|_| |_|_|

# https://github.com/alexandrevicenzi/Flex/wiki/Custom-Settings

SITETITLE = AUTHOR
SITESUBTITLE = "software engineer | pythonista"
SITELOGO = "images/profile.jpg"

LINKS = (
    ("blog home", "/"),
    ("tags", "/tags"),
)

SOCIAL = (
    ("github", "https://github.com/brookskindle"),
)

# Use dracula colors: https://github.com/dracula/dracula-theme/
PYGMENTS_STYLE = "dracula"
BROWSER_COLOR = "#282a36"
CUSTOM_CSS = "static/custom.css"
