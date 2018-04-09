from settings import COURSE_PATH
from collections import defaultdict
import re
import os


def get_files(path=COURSE_PATH):
    ''' Find sub folders and files on the path'''
    if path[-1] != "/":
        path += "/"
    directories = defaultdict(dict)
    for root, folder, files, _ in os.fwalk(path):
        root_without_path = root.replace(path, "").split("/")
        if root_without_path[0]:
            index = directories
            for under_level in root_without_path:
                if under_level in index:
                    index = index[under_level]['folders']
                else:
                    index[under_level] = defaultdict(dict)
                    index[under_level]['folders'] = defaultdict(dict)
                    index[under_level]['files'] = [file for file in files
                                                   if not re.search("^\.", file)]
    return directories


def find_directory(chapter_name, couse_structure):
    ''' Find folder on dict using indexes split by / '''
    if chapter_name[-1] != "/":
        chapter_name += "/"
    directory = couse_structure
    for name in chapter_name.split("/")[:-1]:
        print(directory[name])
        files = directory[name]['files']
        directory = directory[name]['folders']
    return directory, files
