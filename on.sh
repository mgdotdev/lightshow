#!/bin/sh

rm nohup.out
kill $(pgrep lightshow)
nohup lightshow "$@" &
