import os

from flask import (
    Flask,
    redirect,
    render_template,
    request,
    send_from_directory,
)

from directory_inspect import find_directory, get_files, statistics
from settings import ANNOTATION_EXTENSION, COURSE_PATH, VIDEO_EXTENSION

app = Flask(__name__, static_url_path='/static')


COURSE_STRUCTURE = get_files()


def _reload_structure():
    global COURSE_STRUCTURE
    COURSE_STRUCTURE = get_files()


@app.route('/reload')
def reload():
    _reload_structure()
    return redirect('/')


@app.route('/')
def index():
    context = {
        'folders': COURSE_STRUCTURE,
        'video_extension': VIDEO_EXTENSION,
        'statistics': statistics(COURSE_STRUCTURE)
    }
    return render_template('index.html', **context)


@app.route('/chapter/<path:chapter_name>/', methods=['GET'])
def chapter(chapter_name):
    directory, files = find_directory(chapter_name, COURSE_STRUCTURE)
    context = {
        'folders_directory': sorted(directory),
        'folders': COURSE_STRUCTURE,
        'files': sorted(files.items(), key=lambda x: x[0][1]),
        'chapter': chapter_name}
    return render_template('chapter.html', **context)


@app.route('/file/<path:filename>/')
def send_files(filename):
    return send_from_directory(COURSE_PATH, filename)


@app.route('/save', methods=['POST'])
def save_files():
    data = request.form
    file_path = f'{COURSE_PATH}/{data["file_name"]}'
    if os.path.isfile(file_path):
        try:
            with open(file_path, 'w') as annotation:
                annotation.write(data['text'])
            return 'Success!'
        except Exception:
            return 'Fail!'
    return file_path


@app.route('/create', methods=['POST'])
def create_file():
    data = request.form
    file_path = f'{COURSE_PATH}/{data["file_name"]}.{ANNOTATION_EXTENSION}'
    if not os.path.isfile(file_path):
        open(file_path, 'w').close()
        _reload_structure()
        return 'Annotation created!'
    return 'Fail to create the annotation!!!'


if __name__ == '__main__':
    app.run(debug=True, port=8000)
