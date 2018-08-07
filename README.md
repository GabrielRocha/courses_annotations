### Course Organizer Template


#### Example:
##### Folder Tree
```bash
course
  ├── chapter_1
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

#### Menu Tree
``` bash
course
  ├── chapter_1
  ├── chapter_2
  │   └── folder   
  └── chapter_3
```

#### Page Example



#### Build and Run Project

##### Configuration
Copy `local.env` to `.env`
```bash
cp local.env .env
```

This file has 3 variables that you need configure

* COURSE_PATH
    * Course or Videos path
* ANNOTATION_EXTENSION
    * File extension that you want create
* VIDEO_EXTENSION
    * Video extension.

##### Development
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

##### Tests
```bash
pytest .
```

##### Production

Technologies
* [docker](https://www.docker.com/what-docker)
* [docker-compose](https://docs.docker.com/compose/overview/)
* [gunicorn](http://gunicorn.org/)

```bash
docker-compose up
```