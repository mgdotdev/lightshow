#!/bin/bash

rm nohup.out
kill $(pgrep lightshow)
nohup lightshow "$@" &
