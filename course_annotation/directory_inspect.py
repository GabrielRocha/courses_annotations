import os
import re
from collections import OrderedDict, defaultdict
from itertools import groupby

import settings

REGEX_VIDEO = re.compile(f'( |\w|-|[0-9])*\.{settings.VIDEO_EXTENSION}')
REGEX_ANNOTATION = re.compile(f'( |\w|-|[0-9])*\.{settings.ANNOTATION_EXTENSION}')


def get_files(path=settings.COURSE_PATH):
    """ Find sub folders and files on the path """
    if path[-1] != "/":
        path += "/"
    directories = defaultdict(dict)
    for root, folder, files, _ in os.fwalk(path):
        files = [file for file in files if not re.search("^\.", file)]
        root_without_path = root.replace(path, "").split("/")
        if root_without_path[0]:
            index = directories
            for level, under_level in enumerate(root_without_path, start=1):
                if under_level in index:
                    index = index[under_level]['folders']
                else:
                    get_folder_file(files, under_level, index)
        elif files:
            folder = root.split("/")[-2]
            get_folder_file(files, folder, directories)
    return directories


def get_folder_file(files, root, directories):
    files = group_by_type(files)
    directories[root] = defaultdict(dict)
    directories[root]['folders'] = defaultdict(dict)
    directories[root]['files'] = OrderedDict(sorted(files.items(), key=lambda x: x[0][1]))
    return directories


def find_directory(chapter_name, couse_structure):
    """ Find folder on dict using indexes split by / """
    if chapter_name[-1] != "/":
        chapter_name += "/"
    directory = couse_structure
    for name in chapter_name.split("/")[:-1]:
        files = directory[name].get('files', {})
        directory = directory[name].get('folders', {})
    return directory, files


def group_by_type(files):
    valid_files = [file for file in files]
    valid_files.sort()
    group_files = groupby(valid_files, lambda x: x.split(".")[0])
    video_and_annotation_files = defaultdict(dict)
    for _file, _iter in group_files:
        file = "|".join(_iter)
        video = REGEX_VIDEO.search(file)
        annotation = REGEX_ANNOTATION.search(file)
        if video:
            video_and_annotation_files[_file]["video"] = video.group()
        if annotation:
            video_and_annotation_files[_file]["annotation"] = annotation.group()
            continue
    return video_and_annotation_files


def statistics(folders, parents=""):
    """
    Return total of folders, videos and annotations in the course
    and three folders that contains videos
    """
    folder_videos = []
    folder = len(folders)
    videos = len(folders.get('files', []))
    annotations = 0
    for item, values in folders.items():
        parent = f'{parents}/{item}'
        statistics_folder = statistics(values.get('folders', {}), parent)
        folder += statistics_folder['count_folder']
        videos += len(values['files']) + statistics_folder['count_videos']
        if len(folder_videos) < 3 and values['files']:
            folder_videos.append((parent, item, values))
        for _, video in values['files'].items():
            if 'annotation' in video:
                annotations += 1
        annotations += statistics_folder['count_annotations']
    return {
        'count_folder': folder,
        'count_videos': videos,
        'count_annotations': annotations,
        'folder_videos': folder_videos
    }
