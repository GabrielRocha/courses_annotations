from flask import Flask, render_template
from directory_inspect import get_files, find_directory
from settings import COURSE_PATH

app = Flask(__name__, static_url_path="/static", static_folder=COURSE_PATH)


COUSE_STRUCTURE = get_files()


@app.route("/")
def index():
    context = {"folders": sorted(COUSE_STRUCTURE)}
    return render_template("index.html", **context)


@app.route("/chapter/<path:chapter_name>", methods=["GET"])
def chapter(chapter_name):
    directory, files = find_directory(chapter_name, COUSE_STRUCTURE)
    context = {"folders": sorted(directory),
               "files": sorted(files.items(), key=lambda x:x[0]),
               "chapter": chapter_name}
    return render_template("chapter.html", **context)


if __name__ == "__main__":
    app.run(debug=True)
