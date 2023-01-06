import os
import subprocess
from pytube import YouTube
import random
import requests
import re
import string



def foldertitle(url):
    try:
        res = requests.get(url)
    except:
        print('no internet')
        return False
    plain_text = res.text
    if 'list=' in url:
        eq = url.rfind('=') + 1
        cPL = url[eq:]
    else:
        print('Incorrect attempt.')
        return False
    return cPL


def link_snatcher(url):
    our_links = []
    try:
        res = requests.get(url)
    except:
        print('no internet')
        return False
    plain_text = res.text
    if 'list=' in url:
        eq = url.rfind('=') + 1
        cPL = url[eq:]
    else:
        print('Incorrect Playlist.')
        return False
    tmp_mat = re.compile(r'watch\?v=\S+?list=' + cPL)
    mat = re.findall(tmp_mat, plain_text)
    for m in mat:
        new_m = m.replace('&amp;', '&')
        work_m = 'https://youtube.com/' + new_m
        # print(work_m)
        if work_m not in our_links:
            our_links.append(work_m)
    return our_links

if os.name == 'nt':
  os.system('cls')
else:
  os.system('clear')

BASE_DIR = os.getcwd()

print('WELCOME TO PLAYLIST DOWNLOADER DEVELOPED BY - www.github.com/shashwot')

url = str(input("\nSpecify your Playlist URL: "))

options = ['1080p','720p', '360p', 'mp3']

user_input = ''

input_message = "\nPick an option: \n"

for index, item in enumerate(options):
    input_message += f'{index+1}) {item}\n'

input_message += '\nYour choice: '

while user_input.lower() not in options:
    user_input = input(input_message)

user_res = user_input.lower()

our_links = link_snatcher(url)

os.chdir(BASE_DIR)

new_folder_name = foldertitle(url)
print(new_folder_name[:7])

try:
    os.mkdir(new_folder_name[:7])
except:
    print('folder already exists')

os.chdir(new_folder_name[:7])
SAVEPATH = os.getcwd()
print(f'\n files will be saved to {SAVEPATH}')

x=[]
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        pathh = os.path.join(root, name)
        if os.path.getsize(pathh) < 1:
            os.remove(pathh)
        else:
            x.append(str(name))


print('\nconnecting . . .\n')


print()

for link in our_links:
    try:
        yt = YouTube(link)
        main_title = yt.title
        main_title = main_title + '.mp4'
        main_title = main_title.replace('|', '')
        
    except:
        print('connection problem..unable to fetch video info')
        break

    
    if main_title not in x:

        
        if user_res == '360p' or user_res == '720p' or user_res == '1080p':
            vid = yt.streams.filter(progressive=True, file_extension='mp4', res=user_res).first()
            print('Downloading. . . ' + vid.default_filename + ' and its file size -> ' + str(round(vid.filesize / (1024 * 1024), 2)) + ' MB.')
            vid.download(SAVEPATH)
            print('Video Downloaded')
        elif user_res == 'mp3':
            vid = yt.streams.filter(only_audio=True).first()
            filename = vid.default_filename
            new_filename = filename[:-4] + '.mp3'
            print('Downloading. . . ' + new_filename + ' and its file size -> ' + str(round(vid.filesize / (1024 * 1024), 2)) + ' MB.')
            vid.download(SAVEPATH, filename=new_filename)
            print('Audio Downloaded')
        else:
            print('something is wrong.. please rerun the script')


    else:
        print(f'\n skipping "{main_title}" video \n')


print('\n Downloading Finished \n')
print(f'\n All your Videos/Audios are saved at --> {SAVEPATH}')
