# This repository
is the source for my blog, built with python and
[Pelican](https://blog.getpelican.com/).

## Installation
is simple, just `pip install -r requirements.txt`

> this project has submodules, make sure that those are checked out as well, or
> you will run into problems! The easiest way is to say `--recursive` when
> cloning.
>
> `git clone git@github.com:brookskindle/brookskindle.github.io.git --recursive`

## Running a local site
is done by running `make devserver` and pointing your browser to
`http://localhost:8000`

## Publishing to Github
happens by running `make github`
