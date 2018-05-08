# This repository
is the source for my blog, built with python 3.6 and
[Pelican](https://blog.getpelican.com/).

## Installation
is simple, just `pip install -r requirements.txt`

> this project has submodules, make sure that those are checked out as well, or
> you will run into problems! The easiest way is to say `--recursive` when
> cloning.
>
> `git clone git@github.com:brookskindle/brookskindle.github.io.git --recursive`

## Running a local site
is done by running `./develop_server.sh start` and pointing your browser to
`http://localhost:8000`

## Publishing to Github
happens by running `make github`
