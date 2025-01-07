#!/usr/bin/bash

wget -c -O glibc_x86_64.deps https://packages.termux.dev/apt/termux-glibc/dists/glibc/stable/binary-x86_64/Packages

wget -i glibc_x86_64.txt -P glibc_x86_64 -c

