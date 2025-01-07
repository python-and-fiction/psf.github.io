#!/usr/bin/bash

wget -c -O main_aarch64.deps https://packages.termux.dev/apt/termux-main/dists/stable/main/binary-aarch64/Packages

wget -i main_aarch64.txt -P main_aarch64 -c

