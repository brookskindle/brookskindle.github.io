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
THEME_STATIC_DIR = "theme"

SITEURL = "http://localhost:8000"
RELATIVE_URLS = True  # Use document-relative URLs when developing

PATH = "content"
STATIC_PATHS = [
    "styles",
    "images",
]
EXTRA_PATH_METADATA = {
    # The Flex theme doesn't let us customize where to load pygments styles
    # from, so make sure our theme is placed where Flex can find it.
    "styles/pygments/dracula.css": {
        "path": f"{THEME_STATIC_DIR}/pygments/dracula.min.css"
    },
    "images/favicon.ico": {"path": "favicon.ico"},
}

CUSTOM_CSS = "styles/styles.css"

MARKUP = ["md", "ipynb"]
PLUGIN_PATHS = ["./plugins"]
PLUGINS = ["ipynb.markup"]
IPYNB_IGNORE_CSS = True  # Let ipynb posts use site CSS settings

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
SITESUBTITLE = "software engineer"
SITELOGO = "/images/profile.jpg"

LINKS = (
    ("blog home", "/"),
    ("tags", "/tags"),
)

SOCIAL = (
    ("github", "https://github.com/brookskindle"),
    ("linkedin", "https://www.linkedin.com/in/brookskindle/"),
)

# Use dracula colors: https://github.com/dracula/dracula-theme/
PYGMENTS_STYLE = "dracula"
BROWSER_COLOR = "#282a36"
