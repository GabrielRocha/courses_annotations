from settings import COURSE_PATH, CREATE_ANNOTATION
from collections import defaultdict
from itertools import groupby
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
            for level, under_level in enumerate(root_without_path, start=1):
                file_path = "/".join(root_without_path[:level])
                if under_level in index:
                    index = index[under_level]['folders']
                else:
                    files = group_by_type(file_path, [file for file in files
                                                      if not re.search("^\.", file)])
                    index[under_level] = defaultdict(dict)
                    index[under_level]['folders'] = defaultdict(dict)
                    index[under_level]['files'] = files
    return directories


def find_directory(chapter_name, couse_structure):
    ''' Find folder on dict using indexes split by / '''
    if chapter_name[-1] != "/":
        chapter_name += "/"
    directory = couse_structure
    for name in chapter_name.split("/")[:-1]:
        files = directory[name]['files']
        directory = directory[name]['folders']
    return directory, files


def group_by_type(chapter_name, files):
    valid_files = [file for file in files if file.endswith(("mp4", "txt"))]
    valid_files.sort()
    group_files = groupby(valid_files, lambda x: x.split(".")[0])
    video_and_annotation_files = defaultdict(dict)
    for x, iter in group_files:
        file = "|".join(iter)
        video = re.search("( |\w|-|[0-9])*\.mp4", file)
        annotation = re.search("( |\w|-|[0-9])*\.txt", file)
        if video:
            video_and_annotation_files[x]["video"] = video.group()
        if annotation:
            video_and_annotation_files[x]["annotation"] = annotation.group()
            continue
        elif CREATE_ANNOTATION:
            video_and_annotation_files[x]["annotation"] = create_annotation(chapter_name, file)
    return video_and_annotation_files


def create_annotation(chapter_name, file):
    _file = file.split("|")[0]
    _file = f'{"".join(_file.split(".")[:-1])}.txt'
    if os.system(f"echo 'Annotation' > '{COURSE_PATH}{chapter_name}/{_file}'") == 0:
        return _file
