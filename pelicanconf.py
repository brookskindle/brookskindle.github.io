#!/usr/bin/env python
import pathlib

AUTHOR = "Brooks Kindle"
SITENAME = AUTHOR
SITEURL = ""

SITETITLE = AUTHOR
SITESUBTITLE = "software engineer | pythonista"

PATH = "content"

TIMEZONE = "America/Los_Angeles"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("blog home", "/"),
    ("tags", "/tags"),
)

# Social widget
SOCIAL = (
    ("github", "https://github.com/brookskindle"),
)

DEFAULT_PAGINATION = 10

THEME = str(pathlib.Path.cwd() / "theme")

PYGMENTS_STYLE = "default"

SITELOGO = f"{SITEURL}/images/profile.jpg"

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
