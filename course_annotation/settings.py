from prettyconf import config


COURSE_PATH = config('COURSE_PATH', default=".")

ANNOTATION_EXTENSION = config('ANNOTATION_EXTENSION', default="html")

VIDEO_EXTENSION = config('VIDEO_EXTENSION', default="mp4")
