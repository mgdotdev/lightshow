#!/bin/bash

kill $(pgrep python)
nohup lightshow "$@" &
