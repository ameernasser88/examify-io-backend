 # College Graduation project , REST API backed



## Getting Started
### Installing Dependencies
#### Python
Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment
I recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies
Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies
- [Django](https://www.djangoproject.com/)  is a backend framework. Django is required to handle requests and responses.

- [Django-rest-framework](https://www.django-rest-framework.org/) Django REST framework is a powerful and flexible toolkit for building Web APIs.


## Running the server
From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:
#### Mac , Linux

```bash

python3 manage.py runserver
```

To run the server, execute:
#### Windows

```bash
python manage.py runserver
```
## Endpoints
# POST /dj-rest-auth/registration/
* General:
    - Returns Token and user type.
* Sample: ``` curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/dj-rest-auth/registration/ -X POST -H "Content-Type: application/json" -d
            '{
                "username": "omar",
                "password1":"Aa123456789",
                "password2":"Aa123456789",
                "email":"omar@omar.com",
                "user_type":"1"
                }' 
            ```
```sh
{
    "key": "52862e084f56792e2644b1801952a728a75fd8e5",
    "user": 9
}
```
# POST /dj-rest-auth/login/
* General:
- Returns Token and user type.
* Sample: ``` curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/dj-rest-auth/login/ -X POST -H "Content-Type: application/json" -d
            '{
            "username": "omar",
            "password":"Aa123456789"
            }' 
            ```
```sh
{
    "key": "bd5188970056063a94afcf859820713f8cab743e",
    "user": 2
}
```
# GET /exam/
* General:
- Returns exam list for the logged in examiner.
* Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/ -H "Content-Type: application/json"  "Authorization: Token <ACCESS_TOKEN>"```
```sh
{
    {
        "id": 1,
        "exam_name": "Exam 1",
        "exam_startdate": "2021-05-25T14:52:37Z",
        "exam_duration": 3.0,
        "examiner": 2
    }
}
```
# POST /exam/
* General:
- Returns exam list for the logged in examiner.
* Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/ -X POST -H "Content-Type: application/json"  "Authorization: Token <ACCESS_TOKEN>" -d
            '{
            "exam_name":"Exam 1",
            "exam_startdate":"2021-05-27 02:25:33+02:00",
            "exam_duration": 3.0
            }' 
            ```
```sh
{
    "id": 1,
    "exam_name": "Exam 1",
    "exam_startdate": "2021-05-27 02:25:33+02:00",
    "exam_duration": 3.0,
    "examiner": 2
}
```

# POST /exam/{exam_id}/question/
* General:
- Returns exam list for the logged in examiner.
* Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/{exam_id}/question/ -X POST -H "Content-Type: application/json" -H "Content-Type: application/json"  "Authorization: Token <ACCESS_TOKEN>" -d
            '{
            "text": "how old are you now wrong ?",
            "mark": 100
            }' 
        ```
```sh
{
    "id": 6,
    "text": "how old are you now?",
    "mark": 100.0,
    "exam": 1,
    "previous_question": null
}
```
# POST /exam/question/{question_id}/answer/
* General:
- Returns exam list for the logged in examiner.
* Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/question/{question_id}/answer/ -X POST -H "Content-Type: application/json" -H "Content-Type: application/json"  "Authorization: Token <ACCESS_TOKEN>" -d
            '{
            "text":"15",
            "is_correct":true
            }' 
        ```
```sh
{
    "id": 3,
    "text": "15",
    "is_correct": true,
    "question": 6
}
```
# POST /exam/question/{question_id}/answer/
* General:
- Returns exam list for the logged in examiner.
* Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/1/start/ -X POST -H "Content-Type: application/json" -H "Content-Type: application/json"  "Authorization: Token <ACCESS_TOKEN>" -d ```
```sh
{
    "exam_name": "Exam 1",
    "exam_starttime": "2021-05-25T23:25:33Z",
    "exam_duration": 3.0,
    "questions": {
        "how old are you ?": {
            "mark": 4.5,
            "previous_question": null,
            "answers": {
                "0": "6",
                "1": "23"
            }
        },
        "test?": {
            "mark": 50.0,
            "previous_question": null,
            "answers": {
                "0": "15"
            }
        },
        "how old are you now wrong new?": {
            "mark": 100.0,
            "previous_question": null,
            "answers": {}
        },
        "how old are you now wrong test new?": {
            "mark": 100.0,
            "previous_question": null,
            "answers": {}
        }
    }
}
```