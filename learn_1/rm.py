# -*- coding: utf-8 -*-

import os


def file_name(file_dir):
    file_list = []
    # 三元tupple(dirpath, dirnames, filenames)
    '''
    dirpath：string，代表目录的路径；
    dirnames：list，包含了当前dirpath路径下所有的子目录名字（不包含目录路径）；
    filenames：list，包含了当前dirpath路径下所有的非目录子文件的名字（不包含目录路径）。
    '''
    for root, dirs, files in os.walk(file_dir):
        print(root)
        print(dirs)
        print("----")
        print(files)
        for file in files:
            print(os.path.splitext(file))
            if os.path.splitext(file)[1] == '.md':
                file_list.append(os.path.join(root, file))
    return file_list

def md_Link(file_list):
    for file in file_list:
        with open(file, 'r+', encoding='utf-8') as f:
            d = f.read()
            t = d.replace('http://xxxx.xx.clouddn.com', 'https://raw.xx.com/xxx-xxx/xx/xxx')
            f.seek(0, 0)
            f.write(t)

file_list = file_name('_posts')
# md_Link(file_list)
print(file_list)