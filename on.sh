#!/bin/bash

kill $(pgrep python)
nohup python /root/code/script.py "$@" &
