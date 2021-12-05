#!/bin/bash

kill $(pgrep lightshow)
nohup lightshow "$@" &
