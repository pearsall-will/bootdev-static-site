#!/bin/bash
python3 -m unittest discover -s src -vv #2>&1 | GREP_COLOR='01;32' egrep -i --color=always '^test.*OK$|' |  GREP_COLOR='01;31' egrep -i --color=always '.*FAIL.*$|'

