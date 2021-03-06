### Annotations Organizer

The goal is to create a management system for local videos annotations.
Using local files the user could update, read and send to cloud the annotations without the system.

## Example:
### Folder Tree
```bash
course
    ├── chapter_1
    │   ├── example.html
    │   └── example.mp4
    ├── chapter_2
    │   ├── example_2.mp4
    │   └── folder
    │       └── example_2_1.mp4
    └── chapter_3
        ├── example_3.mp4
        ├── image_example.png
        └── text_example.pdf
```

### Menu Tree
``` bash
course
  ├── chapter_1
  ├── chapter_2
  │   └── .
  │   └── folder   
  └── chapter_3
```

### Page Example

The user has to create the annotation for each video.

![no_annotation](doc/images/no_annotation.png)

![annotation](doc/images/annotation.png)

## Configuration
Copy `local.env` to `.env`
```bash
cp local.env .env
```

This file has 3 variables that you need configure

* COURSE_PATH
    * Course or Videos path
      * ex: /home/user/videos/
* ANNOTATION_EXTENSION
    * File extension that you want create
* VIDEO_EXTENSION
    * Video extension.


## Run Project

Both environments below use the port **8000** and host **localhost**

### Development
You need the python `virtualenv`. Below has two ways to create, choose one.
* [virtualenv](https://virtualenv.pypa.io/en/stable/) 
* [pipenv](https://docs.pipenv.org/)

**Install libs**
```bash
pip install -r requirements/development.pip
```

**Run the server**
```bash
cd course_annotation
python app.py
```

#### Tests
```bash
pytest .
```

### Production

Technologies
* [docker](https://www.docker.com/what-docker)
* [docker-compose](https://docs.docker.com/compose/overview/)
* [gunicorn](http://gunicorn.org/)

```bash
docker-compose up
```

## FYI

If you need reload the course path, just access:
```text
http://localhost:8000/reload/
```
