#!/usr/bin/bash

wget -c -O tur_repo_tur_aarch64.deps https://tur.kcubeterm.com/dists/tur-packages/tur/binary-aarch64/Packages

#wget -c -O tur_repo_tur_on_device_aarch64.deps https://tur.kcubeterm.com/dists/tur-packages/tur-on-device/binary-aarch64/Packages

#wget -c -O tur_repo_tur_continuous_aarch64.deps https://tur.kcubeterm.com/dists/tur-packages/tur-continuous/binary-aarch64/Packages

wget -i tur_repo_aarch64.txt -P tur_repo_aarch64 -c --no-check-certificate

