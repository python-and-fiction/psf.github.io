import webbrowser
import time
import requests
import re
import sys

repo_url = 'https://api.github.com/repos/microsoft/vscode/releases/latest'

version = requests.get(repo_url).json()['tag_name']
answer = input(f'Latest Version is {version}，Upgrade(y or n)?')
if answer == 'n':
	sys.exit()

release_url = requests.get(repo_url).json()['html_url']
commit_id = (re.search('href=\"/microsoft/vscode/commit/(.+?)\"',requests.get('https://mirror.ghproxy.com/'+release_url).text).group(1))

server_urls = [
	(f'https://update.code.visualstudio.com/commit:{commit_id}/server-linux-x64/stable',6),
	(f'https://update.code.visualstudio.com/commit:{commit_id}/server-win32-x64/stable',6),
	(f'https://update.code.visualstudio.com/commit:{commit_id}/server-alpine-arm64/stable',6),
	(f'https://update.code.visualstudio.com/commit:{commit_id}/server-linux-arm64/stable',6)
]
server_web_urls = [
	(f'https://update.code.visualstudio.com/commit:{commit_id}/server-linux-x64-web/stable',6),
	(f'https://update.code.visualstudio.com/commit:{commit_id}/server-win32-x64-web/stable',6),
	(f'https://update.code.visualstudio.com/commit:{commit_id}/server-alpine-arm64-web/stable',6),
	(f'https://update.code.visualstudio.com/commit:{commit_id}/server-linux-arm64-web/stable',6)
]
bin_urls = [
	(f'https://update.code.visualstudio.com/commit:{commit_id}/cli-win32-x64/stable',2),
	(f'https://update.code.visualstudio.com/commit:{commit_id}/cli-win32-arm64/stable',2),
	(f'https://update.code.visualstudio.com/commit:{commit_id}/cli-alpine-x64/stable',2),
	(f'https://update.code.visualstudio.com/commit:{commit_id}/cli-alpine-arm64/stable',2),
	(f'https://update.code.visualstudio.com/commit:{commit_id}/win32-x64-user/stable',10),
	(f'https://update.code.visualstudio.com/commit:{commit_id}/win32-arm64-user/stable',10),
	(f'https://update.code.visualstudio.com/commit:{commit_id}/win32-x64/stable',10),
	(f'https://update.code.visualstudio.com/commit:{commit_id}/win32-arm64/stable',10),
	(f'https://update.code.visualstudio.com/commit:{commit_id}/win32-x64-archive/stable',14),
	(f'https://update.code.visualstudio.com/commit:{commit_id}/win32-arm64-archive/stable',14),
	(f'https://update.code.visualstudio.com/commit:{commit_id}/linux-deb-x64/stable',10),
	(f'https://update.code.visualstudio.com/commit:{commit_id}/linux-deb-arm64/stable',10),
	(f'https://update.code.visualstudio.com/commit:{commit_id}/linux-rpm-x64/stable',14),
	(f'https://update.code.visualstudio.com/commit:{commit_id}/linux-rpm-arm64/stable',14),
	(f'https://update.code.visualstudio.com/commit:{commit_id}/linux-x64/stable',14),
	(f'https://update.code.visualstudio.com/commit:{commit_id}/linux-arm64/stable',14)
	]

answer2 = input(f'Download(y or n)?choose n to print urls and write them into urls.txt:')
if answer2 == 'n':
	str1 = '\n'.join([ i[0] for i in server_urls])
	str2 = '\n'.join([ i[0] for i in server_web_urls])
	str3 = '\n'.join([ i[0] for i in bin_urls])
	output = f'''vscode server's urls are:
{str1}
vscode server web's urls are:
{str2}
vscode bin's urls are：
{str3}'''
	with open(r'./urls.txt','w') as f:
		f.write(output)
	print(output)
	sys.exit()

for url,wait_time in bin_urls:
    webbrowser.open_new_tab(url)
    time.sleep(wait_time)
    
for url,wait_time in server_urls:
    webbrowser.open_new_tab(url)
    time.sleep(wait_time)
    
for url,wait_time  in server_web_urls:
    webbrowser.open_new_tab(url)
    time.sleep(wait_time)