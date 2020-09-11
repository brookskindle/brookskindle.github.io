#!/bin/bash
#
# Useful with:
#   echo cli-whirlwind-tour.md | entr bash regenerate.sh

cat remark-begin.html ./cli-whirlwind-tour.md ./remark-end.html > ./whirlwind.html
