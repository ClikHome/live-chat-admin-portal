#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import abspath, join, dirname, exists, split
from shutil import copyfile
import os
import re

BASE_DIR = abspath(dirname(__file__))
TEMPLATE_DIR = join(BASE_DIR, 'templates', 'portal')

FILE = join(TEMPLATE_DIR, 'index.html')

RAW_TEMPLATE_DIRECTORY = abspath(r'C:\Users\Eugene\Desktop\themeforest-11989202-remark-responsive-bootstrap-admin-template\material\topbar\html')


def join_path(path):
    path_to_file = RAW_TEMPLATE_DIRECTORY

    for path in path.split('/'):
        if path == '..':
            path_to_file = dirname(path_to_file)
        else:
            path_to_file = join(path_to_file, path)

    filename = os.path.split(path_to_file)[-1]
    return filename, path_to_file


def change_html_pathes_to_static():
    static = lambda x: join(BASE_DIR, 'static', x)

    file_exp = {
        '.css':  static('css'),
        '.js': static('js'),
        '.png': static('images')
    }

    for path in file_exp.values():
        if not exists(path):
            os.makedirs(path)

    data_to_change = {}

    with open(FILE, 'r') as f:
        for i, line in enumerate(f.readlines()):

            if '<link rel="stylesheet"' in line:
                href = re.search(r'href="(.+)"', line).group(1)
                file_type = '.css'

            elif '<script src=' in line:
                href = re.search(r'src="(.+)"', line).group(1)
                file_type = '.js'

            elif 'src="' and '<img' in line:
                href = re.search(r'src="(.+)"', line).group(1)
                file_type = '.png'
                print href
            else:
                continue

            filename, path_to_file = join_path(href)

            if 'team' in filename:
                print path_to_file
                print filename, exists(path_to_file)

            if exists(path_to_file):
                path_to_new_file = file_exp[file_type]


                static_path = split(path_to_new_file)[1] + '/' +  filename
                static_str = "{% static '" + static_path + "' %}"

                data_to_change[str(i)] = line.replace(href, static_str)
                copyfile(path_to_file, join(path_to_new_file, filename))

                # with open(path_to_file, 'r') as original_file:
                #     with open(join(path_to_new_file, filename), 'w') as f:
                #         f.writelines(original_file.readlines())

    with open(FILE, 'r') as f:
        with open(join(TEMPLATE_DIR, 'index2.html'), 'w') as new_file:
            for i, line in enumerate(f.readlines()):
                if str(i) in data_to_change.keys():
                    line = data_to_change[str(i)]
                new_file.write(line)

change_html_pathes_to_static()


