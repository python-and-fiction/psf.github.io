#!/usr/bin/env python3

import os

current_dir = os.path.dirname(os.path.abspath(__file__))
url_list_file = ['tur_wheels_aarch64','tur_wheels_x86_64','tur_repo_aarch64','tur_repo_x86_64','glibc_aarch64','glibc_x86_64','main_aarch64','main_x86_64']
#url_list_file = ['tur_wheels_aarch64','tur_wheels_x86_64','main_aarch64','main_x86_64']
#url_list_file_aarch64 = url_list_file[0::2]
#url_list_file_x86_64 = url_list_file[1::2]
#url_list_file = url_list_file_aarch64

def check_file(file_name):
    file_list = []
    with open(f'{file_name}.txt','r') as f:
        for line in f:
            file_list.append(os.path.basename(line).strip())
    for root,dirs,files in os.walk(file_name):
        for file in files:
            if file not in file_list:
                if os.path.exists(f'{file_name}/{file}'):
                    print(f'{file_name}\'s {file} will be removed!')
                    os.remove(f'{file_name}/{file}')
                
for i in url_list_file:
    check_file(i)
    
