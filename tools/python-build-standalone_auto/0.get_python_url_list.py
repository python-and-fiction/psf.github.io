#!/usr/bin/env python3

import requests,json,os
from urllib.parse import unquote

current_dir = os.path.dirname(os.path.abspath(__file__))

python_url = r'https://api.github.com/repos/astral-sh/python-build-standalone/releases/latest'

def get_download_url_git(url):
    response = requests.get(url)
    content = response.text
    json_obj = json.loads(content)
    file_urls = []
    for i in json_obj["assets"]:
        browser_download_url = i["browser_download_url"]
        if any(browser_download_url.endswith(suffix) for suffix in ['.zst','.tar.gz']) \
        and any(target in browser_download_url for target in ['linux','windows'] ) \
            and any(arch in browser_download_url for arch in ['aarch64','x86_64'] ):
            if browser_download_url not in file_urls:
                file_urls.append(unquote(browser_download_url))
    alt_url = r'https://ghproxy.net/'
    return [ alt_url+i for i in file_urls ]

with open(f'{current_dir}/0.python_url.txt','w') as f:
    for i in get_download_url_git(python_url):
        f.write(i+'\n')



