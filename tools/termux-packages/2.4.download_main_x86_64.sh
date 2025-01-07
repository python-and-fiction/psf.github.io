#!/usr/bin/bash

wget -c -O main_x86_64.deps https://packages.termux.dev/apt/termux-main/dists/stable/main/binary-x86_64/Packages

wget -i main_x86_64.txt -P main_x86_64 -c

