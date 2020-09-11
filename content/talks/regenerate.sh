#!/bin/bash
#
# Useful with:
#   echo cli-whirlwind-tour.md | entr ./regenerate.sh

cat remark-begin.html ./cli-whirlwind-tour.md ./remark-end.html > ./whirlwind.html
