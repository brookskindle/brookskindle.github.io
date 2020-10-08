Title: Reducing zsh startup time by 400%
Date: 2020-10-08
Category: Programming
Tags: zsh, performance

As part of the nature of my work, I have to interact with a lot of systems and
tools. My `.zshrc` file has slowly grown in order to support this multi-project
workflow. So, too, has the startup time for my shell.

Want to know how long it takes right now? Over a second.

```
$ time zsh -i -c exit
zsh -i -c exit  1.24s user 0.84s system 85% cpu 2.423 total
```

That's insane! I use tmux, so I have to pay this price every time a new window
or pane is opened and it's frustrating to say the least.

It's best to measure first before cutting. I followed Steven Van Bael's post on
[profiling zsh startup time](https://stevenvanbael.com/profiling-zsh-startup)
and added `zmodload zsh/zprof` as the first line and `zprof` as the last in
`~/.zshrc`.

```
num  calls                time                       self            name
-----------------------------------------------------------------------------------
 1)    1         203.32   203.32   24.07%    203.22   203.22   24.05%  nvm_die_on_prefix
 2)    1         182.80   182.80   21.64%    182.80   182.80   21.64%  virtualenvwrapper_run_hook
 3)    2         432.98   216.49   51.25%    147.32    73.66   17.44%  nvm
 4)    1          85.92    85.92   10.17%     85.77    85.77   10.15%  __kubectl_bash_source
 5)    1          82.22    82.22    9.73%     72.98    72.98    8.64%  nvm_ensure_version_installed
 6)    1         472.63   472.63   55.94%     39.65    39.65    4.69%  nvm_auto
 7)    1          30.29    30.29    3.59%     30.29    30.29    3.59%  handle_completion_insecurities
 8)    1         200.14   200.14   23.69%     16.70    16.70    1.98%  virtualenvwrapper_initialize
 9)    1          15.86    15.86    1.88%     15.86    15.86    1.88%  compinit
10)    1          10.79    10.79    1.28%     10.68    10.68    1.26%  _zsh_highlight_load_highlighters
11)    1           9.24     9.24    1.09%      9.24     9.24    1.09%  nvm_is_version_installed
12)    2           5.88     2.94    0.70%      5.88     2.94    0.70%  grep-flag-available
13)    1           5.47     5.47    0.65%      5.47     5.47    0.65%  _zsh_highlight_bind_widgets
14)    1           4.12     4.12    0.49%      4.12     4.12    0.49%  nvm_supports_source_options
15)    1           3.22     3.22    0.38%      3.20     3.20    0.38%  powerlevel9k_vcs_init
16)    1           2.17     2.17    0.26%      2.17     2.17    0.26%  termColors
17)    2           1.84     0.92    0.22%      1.84     0.92    0.22%  env_default
18)    2           1.53     0.76    0.18%      1.53     0.76    0.18%  colors
19)    1           7.69     7.69    0.91%      1.31     1.31    0.16%  prompt_powerlevel9k_setup
20)   36           1.14     0.03    0.14%      0.96     0.03    0.11%  set_default
21)    5           0.78     0.16    0.09%      0.78     0.16    0.09%  add-zsh-hook
22)    1           0.59     0.59    0.07%      0.59     0.59    0.07%  virtualenvwrapper_setup_tab_completion
23)    2           0.47     0.23    0.06%      0.47     0.23    0.06%  is-at-least
24)    2           0.45     0.22    0.05%      0.45     0.22    0.05%  bashcompinit
25)    4           0.34     0.09    0.04%      0.34     0.09    0.04%  compdef
26)    2           0.32     0.16    0.04%      0.32     0.16    0.04%  (anon)
27)    3           0.50     0.17    0.06%      0.24     0.08    0.03%  complete
28)    2           0.22     0.11    0.03%      0.22     0.11    0.03%  nvm_has
29)   41           0.22     0.01    0.03%      0.22     0.01    0.03%  defined
30)    1         476.81   476.81   56.44%      0.06     0.06    0.01%  nvm_process_parameters
31)    1           0.08     0.08    0.01%      0.05     0.05    0.01%  print_deprecation_warning
32)    1           0.05     0.05    0.01%      0.05     0.05    0.01%  virtualenvwrapper_verify_workon_home
33)    2           0.05     0.02    0.01%      0.05     0.02    0.01%  segment_in_use
34)    1           0.02     0.02    0.00%      0.02     0.02    0.00%  nvm_is_zsh
...
```

The biggest culprit is `nvm`, the node version manager, followed by `kubectl`,
the CLI tool for kubernetes. I need both, but I don't need them all the time. I
can move their initializations to a function or alias and call them on an
as-needed basis.

```zsh
# Allow kubectl tab-completion
alias k='kubectl'
source <(kubectl completion zsh)
complete -F __start_kubectl k

export NVM_DIR=~/.nvm
source $(brew --prefix nvm)/nvm.sh
```

becomes

```zsh
function init_kubectl() {
    # Allow kubectl tab-completion
    alias k='kubectl'
    source <(kubectl completion zsh)
    complete -F __start_kubectl k
}

function init_nvm() {
    export NVM_DIR=~/.nvm
    # source $(brew --prefix nvm)/nvm.sh
    source /usr/local/opt/nvm/nvm.sh
}
```

```
$ time zsh -i -c exit
zsh -i -c exit  0.29s user 0.15s system 83% cpu 0.524 total
```

This comes out to a 427% performance improvement, but in practical terms it
means that the startup time is much less of a PITA. Not bad for 5 minutes of
effort; this is truly the [Pareto
principle](https://en.wikipedia.org/wiki/Pareto_principle) at work.

If you are interested in a more in-depth analysis of zsh performance, htr3n's
post on a [faster zsh](https://htr3n.github.io/2018/07/faster-zsh/) goes much
further than I did.
