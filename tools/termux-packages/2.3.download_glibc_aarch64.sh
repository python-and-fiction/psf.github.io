#!/usr/bin/bash

wget -c -O glibc_aarch64.deps https://packages.termux.dev/apt/termux-glibc/dists/glibc/stable/binary-aarch64/Packages

wget -i glibc_aarch64.txt -P glibc_aarch64 -c

