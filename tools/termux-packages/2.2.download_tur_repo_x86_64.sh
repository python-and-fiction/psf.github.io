#!/usr/bin/bash

wget -c -O tur_repo_tur_x86_64.deps https://tur.kcubeterm.com/dists/tur-packages/tur/binary-x86_64/Packages

#wget -c -O tur_repo_tur_on_device_x86_64.deps https://tur.kcubeterm.com/dists/tur-packages/tur-on-device/binary-x86_64/Packages

#wget -c -O tur_repo_tur_continuous_x86_64.deps https://tur.kcubeterm.com/dists/tur-packages/tur-continuous/binary-x86_64/Packages

wget -i tur_repo_x86_64.txt -P tur_repo_x86_64 -c --no-check-certificate

