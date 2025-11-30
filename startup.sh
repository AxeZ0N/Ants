#!/bin/bash

path=$(dirname "$(realpath $0)")
echo $path
cd $path

cmd="$path/venv/bin/python3 -m solara run model.py"

gnome-terminal -- bash -c "$cmd" &

vim -S session.vim
