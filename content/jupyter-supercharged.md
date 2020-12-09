Title: Supercharge your jupyter startup with bash and tmux
Date: 2018-06-08
Category: programming
Tags: python, shell

If you're like me, you dislike doing repetitive tasks when a script could have
just as easily done the work for you. For example, starting a jupyter server on
my local machine requires me to do the following:

1. open a terminal
1. source the virtual environment I use for jupyter work
1. `cd` to the directory I want to start jupyter in
1. run `jupyter-notebook`
1. open up my browser and point it to `http://localhost:8888`
1. If I want to close the terminal now, I have to had already
    * either started jupyter within tmux
    * or started jupyter as a background process (`jupyter-notebook &`)

That's repetitive work, especially for someone that uses jupyter on a daily or
semi-daily basis. It's not hard, but the menial task gets old really quckly.

All of this could be placed in a bash script and then called every time you
want to start or open up a jupyter session.
```bash
#!/bin/bash

# A simple script that starts up a jupyter server if not running, or opens the
# browser if one is already running

tmux has-session -t jupyter 1>/dev/null 2>&1
returncode=$?

if [ $returncode -ne 0 ]; then
    echo jupyter is not running
    tmux new-session -d -s "jupyter" -c ~/code
    # Want jupyter to open in a new window?
    # Open the jupyter config in
    #   ~/.jupyter/jupyter_notebook_config.py
    # or generate the config with
    #   jupyter-notebook --generate-config
    # and edit the c.NotebookApp.browser and c.NotebookApp.webbrowser_open_new
    # values to your liking.
    tmux send-keys 'workon jupyter && jupyter-notebook' 'C-m'
    tmux rename-window "jupyter"
else
    echo jupyter is already running, starting web browser
    chromium http://localhost:8888 --new-window
fi
```

If the script is in your PATH and is executable
```
-rwxr-xr-x 1 brooks brooks 816 May 27 12:40 jupyter
```

then it could be called from an application launcher of your choice, without
ever opening a terminal.

![]({filename}/images/start-jupyter.gif)
*launching jupyter with [rofi](https://github.com/DaveDavenport/rofi)*
