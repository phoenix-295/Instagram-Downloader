from tkinter import Tk, Entry, Button, Label, Text
import re
from datetime import datetime
from tqdm import tqdm
import requests
import os
master = Tk()


def fun1():
    file_path = os.path.expanduser('~\Downloads')
    os.chdir(file_path)
    data1 = img_vid_url.get()
    x = re.match(r'^(https:)[/][/]www.([^/]+[.])*instagram.com', data1)
    try:
        if x:
            request_image = requests.get(data1)
            src = request_image.content.decode('utf-8')
            check_type = re.search(
                r'<meta name="medium" content=[\'"]?([^\'" >]+)', src)
            check_type_f = check_type.group()
            final = re.sub('<meta name="medium" content="', '', check_type_f)

            if final == "image":
                extract_image_link = re.search(
                    r'meta property="og:image" content=[\'"]?([^\'" >]+)', src)
                image_link = extract_image_link.group()
                final = re.sub(
                    'meta property="og:image" content="', '', image_link)
                _response = requests.get(final).content
                file_size_request = requests.get(final, stream=True)
                file_size = int(file_size_request.headers['Content-Length'])
                block_size = 1024
                filename = datetime.strftime(
                    datetime.now(), '%Y_%m_%d_%H_%M_%S')
                t = tqdm(total=file_size, unit='B',
                         unit_scale=True, desc=filename, ascii=True)
                with open(filename + '.jpg', 'wb') as f:
                    for data in file_size_request.iter_content(block_size):
                        t.update(len(data))
                        f.write(data)
                t.close()

            if final == "video":
                extract_video_link = re.search(
                    r'meta property="og:video" content=[\'"]?([^\'" >]+)', src)
                video_link = extract_video_link.group()
                final = re.sub(
                    'meta property="og:video" content="', '', video_link)
                _response = requests.get(final).content
                file_size_request = requests.get(final, stream=True)
                file_size = int(
                    file_size_request.headers['Content-Length'])
                block_size = 1024
                filename = datetime.strftime(
                    datetime.now(), '%Y-%m-%d-%H-%M-%S')
                t = tqdm(total=file_size, unit='B',
                         unit_scale=True, desc=filename, ascii=True)
                with open(filename + '.mp4', 'wb') as f:
                    for data in file_size_request.iter_content(block_size):
                        t.update(len(data))
                        f.write(data)
                t.close()
        else:
            pass
    except AttributeError:
        pass


def fun2():
    file_path = os.path.expanduser('~\Downloads')
    os.chdir(file_path)
    data1 = profile_pic.get()
    x = re.match(r'^(https:)[/][/]www.([^/]+[.])*instagram.com', data1)

    if x:
        check_url1 = re.match(
            r'^(https:)[/][/]www.([^/]+[.])*instagram.com[/].*\?hl=[a-z-]{2,5}', data1)
        check_url2 = re.match(
            r'^(https:)[/][/]www.([^/]+[.])*instagram.com$|^(https:)[/][/]www.([^/]+[.])*instagram.com/$', data1)
        check_url3 = re.match(
            r'^(https:)[/][/]www.([^/]+[.])*instagram.com[/][a-zA-Z0-9_]{1,}$', data1)
        check_url4 = re.match(
            r'^(https:)[/][/]www.([^/]+[.])*instagram.com[/][a-zA-Z0-9_]{1,}[/]$', data1)

        if check_url3:
            final_url = data1 + '/?__a=1'

        if check_url4:
            final_url = data1 + '?__a=1'

        if check_url2:
            final_url = print("Please enter an URL related to a profile")
            exit()

        if check_url1:
            alpha = check_url1.group()
            final_url = re.sub('\\?hl=[a-z-]{2,5}', '?__a=1', alpha)

    try:
        if check_url3 or check_url4 or check_url2 or check_url1:
            req = requests.get(final_url)
            get_status = requests.get(final_url).status_code
            get_content = req.content.decode('utf-8')

            if get_status == 200:
                find_pp = re.search(
                    r'profile_pic_url_hd\":\"([^\'\" >]+)', get_content)
                pp_link = find_pp.group()
                pp_final = re.sub('profile_pic_url_hd":"', '', pp_link)
                file_size_request = requests.get(pp_final, stream=True)
                file_size = int(file_size_request.headers['Content-Length'])
                block_size = 1024
                filename = datetime.strftime(
                    datetime.now(), '%Y_%m_%d_%H_%M_%S')
                t = tqdm(total=file_size, unit='B',
                         unit_scale=True, desc=filename, ascii=True)
                with open(filename + '.jpg', 'wb') as f:
                    for data in file_size_request.iter_content(block_size):
                        t.update(len(data))
                        f.write(data)
                t.close()

    except Exception:
        pass


img_vid_url = Entry(master, width=50)
profile_pic = Entry(master, width=50)
button1 = Button(master, text="Download Image/Video", width=25, command=fun1)
button2 = Button(master, text="Download Profile Pic", width=25, command=fun2)


img_vid_url.grid(row=0, column=0, padx=5, pady=10, ipady=3)
button1.grid(row=0, column=1)

profile_pic.grid(row=1, column=0, padx=5, pady=10, ipady=3)
button2.grid(row=1, column=1)
master.mainloop()
