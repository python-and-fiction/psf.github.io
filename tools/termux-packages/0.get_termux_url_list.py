#!/usr/bin/env python3

import requests,json,os
from urllib.parse import unquote

current_dir = os.path.dirname(os.path.abspath(__file__))

git = dict(
    tur_wheels_aarch64 = r'https://api.github.com/repos/termux-user-repository/pypi-wheel-builder/releases/latest',
    tur_wheels_x86_64 = r'https://api.github.com/repos/termux-user-repository/pypi-wheel-builder/releases/latest',
)

git_tur = dict(
    tur_repo_aarch64 = r'https://api.github.com/repos/termux-user-repository/dists/releases/latest',
    tur_repo_x86_64 = r'https://api.github.com/repos/termux-user-repository/dists/releases/latest',
)

apt = dict(
    glibc_aarch64 = r'https://packages.termux.dev/apt/termux-glibc/dists/glibc/stable/binary-aarch64/Packages',
    glibc_x86_64 = r'https://packages.termux.dev/apt/termux-glibc/dists/glibc/stable/binary-x86_64/Packages',
    main_aarch64 = r'https://packages.termux.dev/apt/termux-main/dists/stable/main/binary-aarch64/Packages', 
    main_x86_64 = r'https://packages.termux.dev/apt/termux-main/dists/stable/main/binary-x86_64/Packages', 
)

apt_tur = dict(
    tur_repo_aarch64 = r'https://tur.kcubeterm.com/dists/tur-packages/tur/binary-aarch64/Packages',
    tur_repo_x86_64 = r'https://tur.kcubeterm.com/dists/tur-packages/tur/binary-x86_64/Packages',
)

def get_namelist_tur(url):
    response = requests.get(url)
    content = response.text
    file_urls = []
    for i in content.split():
        if i.startswith('pool/tur/'):
            i = i.split('/')[-1]
            if i not in file_urls:
                file_urls.append(i)
    return file_urls

def get_download_url_git(url,key:str):
    response = requests.get(url)
    content = response.text
    json_obj = json.loads(content)
    file_urls = []
    allowed_suffixs_aarch64 = [
        'aarch64.deb',
        'all.deb',
        'aarch64.whl',
        ]
    allowed_suffixs_x86_64 = [
        'x86_64.deb',
        'all.deb',
        'x86_64.whl',
        ]
    for i in json_obj["assets"]:
        browser_download_url = i["browser_download_url"]
        if any(browser_download_url.endswith(suffix) for suffix in (allowed_suffixs_aarch64 if key.endswith('aarch64') else allowed_suffixs_x86_64)):
            if browser_download_url not in file_urls:
                file_urls.append(unquote(browser_download_url))
    alt_url = r'https://ghgo.xyz/'
    return [ alt_url+i for i in file_urls ]

for k in git.keys():
    with open(f'{current_dir}/{k}.txt','w') as f:
        for i in get_download_url_git(git[k],k):
            f.write(i+'\n')
            
for k in git_tur.keys():
    name_list = get_namelist_tur(apt_tur[k])
    with open(f'{current_dir}/{k}.txt','w') as f:
        for i in get_download_url_git(git_tur[k],k):
            for n in name_list:
                if n in i:f.write(i+'\n')

def get_download_url_apt(url):
    response = requests.get(url)
    content = response.text
    file_urls = []
    for i in content.split():
        if i.startswith('pool/'):
            if i not in file_urls:
                file_urls.append(i)
    prefix_url = r'https://packages.termux.dev/apt/termux-glibc/' if url.startswith(r'https://packages.termux.dev/apt/termux-glibc/') else r'https://packages.termux.dev/apt/termux-main/'
    return [ prefix_url+i for i in file_urls]
    
for k in apt.keys():
    with open(f'{current_dir}/{k}.txt','w') as f:
        for i in get_download_url_apt(apt[k]):
            f.write(i+'\n')


