from flask import Flask, render_template, send_from_directory, request
from directory_inspect import get_files, find_directory
from settings import COURSE_PATH, EXTENSION_ANNOTATION
import os

app = Flask(__name__, static_url_path="/static")


COUSE_STRUCTURE = get_files()


def reload_structure():
    global COUSE_STRUCTURE
    COUSE_STRUCTURE = get_files()


@app.route("/")
def index():
    context = {"folders": sorted(COUSE_STRUCTURE)}
    return render_template("index.html", **context)


@app.route("/chapter/<path:chapter_name>", methods=["GET"])
def chapter(chapter_name):
    directory, files = find_directory(chapter_name, COUSE_STRUCTURE)
    context = {
        "folders": sorted(directory),
        "files": sorted(files.items(), key=lambda x: x[0][1]),
        "chapter": chapter_name}
    return render_template("chapter.html", **context)


@app.route("/file/<path:filename>")
def send_files(filename):
    return send_from_directory(COURSE_PATH, filename)


@app.route("/save", methods=["POST"])
def save_files():
    data = request.form
    file_path = f'{COURSE_PATH}{data["file_name"]}'
    if os.path.isfile(file_path):
        with open(file_path, "w") as annotation:
            annotation.write(data["text"])
        return "Success Upload!"
    return file_path


@app.route("/create", methods=["POST"])
def create_file():
    data = request.form
    file_path = f'{COURSE_PATH}{data["file_name"]}.{EXTENSION_ANNOTATION}'
    if not os.path.isfile(file_path):
        open(file_path, "w").close()
        reload_structure()
        return "Annotation created!"
    return "Fail to create the annotation!!!"


if __name__ == "__main__":
    app.run(debug=True)
