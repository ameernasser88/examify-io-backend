 # College Graduation project , REST API backend



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
# Endpoints
## General
#### POST /dj-rest-auth/registration/
* General:
    - Returns Token and user type.
* Request Sample: ``` curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/dj-rest-auth/registration/ -X POST -H "Content-Type: application/json" -d
            '{
                "username": "name",
                "password1":"Aa123456789",
                "password2":"Aa123456789",
                "email":"name@gmail.com",
                "user_type":"1"
                }' 
            ```
* Response Sample:
```sh
{
    "key": "52862e084f56792e2644b1801952a728a75fd8e5",
    "user_type": 1
}
```
#### POST /dj-rest-auth/login/
* General:
    - Returns Token and user type.
* Request Sample: ``` curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/dj-rest-auth/login/ -X POST -H "Content-Type: application/json" -d
            '{
            "username": "name",
            "password":"Aa123456789"
            }' 
            ```
* Response Sample:
```sh
{
    "key": "bd5188970056063a94afcf859820713f8cab743e",
    "user_type": 2
}
```
## For Examiner:
#### GET /most-recent-exam/
* General:
    - Returns the most recent exam id for the logged in examiner.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/most-recent-exam/ -H "Content-Type: application/json" "Authorization: Token <ACCESS_TOKEN>"
        ```
* Response Sample:
```sh
{
    "id": 157
}
```
#### POST /exam/
* General:
    - Returns exam data.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/ -X POST -H "Content-Type: application/json"  "Authorization: Token <ACCESS_TOKEN>" -d
            '{
            "exam_name":"Exam 1",
            "exam_startdate":"2021-05-27 02:25:33+02:00",
            "exam_duration": 3.0
            }' 
            ```
* Response Sample:
```sh
{
    "id": 1,
    "exam_name": "Exam 1",
    "exam_startdate": "2021-05-27 02:25:33+02:00",
    "exam_duration": 3.0,
    "examiner": 2
}
```
#### GET /exam/
* General:
    - Returns exam list for the logged in examiner.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/ -H "Content-Type: application/json"  "Authorization: Token <ACCESS_TOKEN>"```
* Response Sample:
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
#### GET /exam/{exam_id}/
* General:
    - Returns a whole exam.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/{exam_id}/ -H "Content-Type: application/json"  "Authorization: Token <ACCESS_TOKEN>"```
* Response Sample:
```sh
{
    "id": 13,
    "exam": "Movies",
    "startdate": "2021-05-25T14:52:37Z",
    "duration": 3.0,
    "questions": [
        {
            "id": 18,
            "text": "what was tom hank's name in you've got mail ?",
            "mark": 10.0,
            "answers": {
                "12": {
                    "text": "Joe Fox",
                    "is_correct": true
                },
                "13": {
                    "text": "Joe Tom",
                    "is_correct": false
                },
                "14": {
                    "text": "Jack Tom",
                    "is_correct": false
                },
                "15": {
                    "text": "Jack Daniels",
                    "is_correct": false
                }
            }
        },
        {
            "id": 19,
            "text": "what was Sophie Turner's name in game of thrones ?",
            "mark": 10.0,
            "answers": {
                "16": {
                    "text": "Sansa Snow",
                    "is_correct": false
                },
                "17": {
                    "text": "Sansa Stark",
                    "is_correct": true
                },
                "18": {
                    "text": "Sansa Greyhound",
                    "is_correct": false
                },
                "19": {
                    "text": "Sansa Sand",
                    "is_correct": false
                }
            }
        },
        {
            "id": 20,
            "text": "what was Tom Hank's name in cast away ?",
            "mark": 10.0,
            "answers": {
                "20": {
                    "text": "Chuck Noland",
                    "is_correct": true
                },
                "21": {
                    "text": "Chuck Neil",
                    "is_correct": false
                },
                "22": {
                    "text": "Charles Neil",
                    "is_correct": false
                },
                "23": {
                    "text": "Charl Neil",
                    "is_correct": false
                }
            }
        }
    ]
}
```
#### PATCH /exam/{exam_id}/
* General:
    - Returns 200 ok.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/{exam_id}/ -X PATCH -H "Content-Type: application/json"  "Authorization: Token <ACCESS_TOKEN>"
'{
    "id": 13,
    "exam": "Movies",
    "startdate": "2021-05-25T14:52:37Z",
    "duration": 3.0
}'```
* Response Sample:
```sh
HTTP 200 OK
```
#### Delete /exam/{exam_id}/
* General:
    - Returns 200 ok.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/{exam_id}/ -X Delete -H "Content-Type: application/json"  "Authorization: Token <ACCESS_TOKEN>"```
* Response Sample:
```sh
HTTP 200 OK
```
#### POST /exam/{exam_id}/question/
* General:
    - Returns the question that has been added.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/{exam_id}/question/ -X POST -H "Content-Type: application/json"  "Authorization: Token <ACCESS_TOKEN>" -d
            '{
            "text": "how old are you now wrong ?",
            "mark": 100
            }' 
        ```
* Response Sample:
```sh
{
    "id": 6,
    "text": "how old are you now?",
    "mark": 100.0,
    "exam": 1,
    "previous_question": null
}
```
#### PATCH /exam/{exam_id}/question/{question_id}/
* General:
    - Returns 200 ok.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/{exam_id}/question/{question_id}/ -X PATCH -H "Content-Type: application/json"  "Authorization: Token <ACCESS_TOKEN>" -d
            '{
    "id": 157,
    "text": "what was Sophie Turner's name in game of thrones ? edited question",
    "mark": 11.0
}' 
        ```
* Response Sample:
```sh
200 OK
```
#### DELETE /exam/{exam_id}/question/{question_id}/
* General:
    - Returns 200 ok.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/{exam_id}/question/{question_id}/ -X DELETE -H "Content-Type: application/json"  "Authorization: Token <ACCESS_TOKEN>" ```
* Response Sample:
```sh
200 OK
```
#### POST /exam/question/{question_id}/answer/
* General:
    - Returns the answer that has been added.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/question/{question_id}/answer/ -X POST -H "Content-Type: application/json" -H "Content-Type: application/json"  "Authorization: Token <ACCESS_TOKEN>" -d
            '{
            "text":"15",
            "is_correct":true
            }' 
        ```
* Response Sample:
```sh
{
    "id": 3,
    "text": "15",
    "is_correct": true,
    "question": 6
}
```
#### PATCH /exam/question/{question_id}/answer/{answer_id}/
* General:
    - Returns 200 OK.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/question/{question_id}/answer/{answer_id}/ -X PATCH -H "Content-Type: application/json" -H "Content-Type: application/json"  "Authorization: Token <ACCESS_TOKEN>" -d
            '{
    "text": "Sansa Snow new",
    "is_correct": false
}' 
        ```
* Response Sample:
```sh
200 OK
```
#### DELETE /exam/question/{question_id}/answer/{answer_id}/
* General:
    - Returns 200 OK.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/question/{question_id}/answer/{answer_id}/ -X DELETE -H "Content-Type: application/json" -H "Content-Type: application/json"  "Authorization: Token <ACCESS_TOKEN>" -d ```
* Response Sample:
```sh
200 OK
```
#### POST exam/{exam_id}/allowed-students/
* General:
    - Returns list of students that has been added.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/{exam_id}/allowed-students/ -X POST -H "Content-Type: application/json" "Authorization: Token <ACCESS_TOKEN>" -d
            '{
                "students":["student1","student2"]
            }' 
        ```
* Response Sample:
```sh
{
    "id": 2,
    "student": [
        10,
        6
    ],
    "exam": 1
}
```
#### GET exam/{exam_id}/allowed-students/
* General:
    - Returns list of students allowed to enter the exam.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/{exam_id}/allowed-students/ -H "Content-Type: application/json" "Authorization: Token <ACCESS_TOKEN>"
        ```
* Response Sample:
```sh
    {
    "exam": 165,
    "student": [
        {
            "student_id": 28,
            "student_name": "stu1"
        },
        {
            "student_id": 19,
            "student_name": "stu2"
        },
        {
            "student_id": 18,
            "student_name": "stu3"
        },
        {
            "student_id": 1,
            "student_name": "stu4"
        },
        {
            "student_id": 6,
            "student_name": "stu5"
        }
    ]
}
```
#### DELETE exam/{exam_id}/allowed-students/{student_id}/
* General:
    - Delete allowed student to enter the exam.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/{exam_id}/allowed-students/{student_id}/ -x DELETE -H "Content-Type: application/json" "Authorization: Token <ACCESS_TOKEN>"
        ```
* Response Sample:
```sh
  200 OK
```
#### GET exam/{exam_id}/supervisors/
* General:
    - Retruns list of supervisors for the exam.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/{exam_id}/supervisors/ -X GET -H "Content-Type: application/json" "Authorization: Token <ACCESS_TOKEN>" -d```
* Response Sample:
```sh
[
    {
        "supervisor_id": 45,
        "supervisor_name": "super1",
        "students": [
            "stu1",
            "stu2",
            "stu3"
        ]
    },
    {
        "supervisor_id": 46,
        "supervisor_name": "super2",
        "students": [
            "stu4",
            "stu5"
        ]
    }
]
```
#### GET exam/{exam_id}/statistics/
* General:
    - Retruns statistics for a single exam and its questions.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/{exam_id}/statistics/ -X GET -H "Content-Type: application/json" "Authorization: Token <ACCESS_TOKEN>" -d```
* Response Sample:
```sh
[
    {
        "id": 163,
        "total_mark": 20.0,
        "name": "Movies",
        "exam_statistics": {
            "avg": 29.5,
            "max": 63.0,
            "min": 10.0,
            "num_of_students_submited_the_exam": 4,
            "standard_deviation": 20.081085628023203
        }
    },
    {
        "0": {
            "id": 269,
            "text": "what was Sophie Turner's name in game of thrones ?",
            "correct_answer": "Sansa",
            "mark": 10.0,
            "correct_count": 1,
            "wrong_count": 1
        },
        "1": {
            "id": 270,
            "text": "what was Christian Bale's name in The Dark Knight  ?",
            "correct_answer": "Bruce Wayne",
            "mark": 10.0,
            "correct_count": 2,
            "wrong_count": 0
        }
    }
]
```
#### POST exam/{exam_id}/supervisors/
* General:
    - adds supervisors to exam.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/{exam_id}/supervisors/ -X POST -H "Content-Type: application/json" "Authorization: Token <ACCESS_TOKEN>" -d
        '{
                "supervisor": [
                    "super1",
                    "super2",
                    "super3"
                ]
        }' 
        ```
* Response Sample:
```sh
201 Created 
```
#### DELETE exam/{exam_id}/supervisor/{supervisor_id}/
* General:
    - delete assigned supervisor to exam.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/{exam_id}/supervisor/{supervisor_id}/ -X DELETE -H "Content-Type: application/json" "Authorization: Token <ACCESS_TOKEN>" 
        ```
* Response Sample:
```sh
200 OK 
```
#### GET /exam/{exam_id}/attendance/
* General:
    - Returns list of students allowed to enter the exam.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/{exam_id}/attendance/ -H "Content-Type: application/json" "Authorization: Token <ACCESS_TOKEN>"
        ```
* Response Sample:
```sh
[
    {
        "student_name": "student1",
        "supervisor_name": "supervisor1",
        "enter_time": "2021-05-18T18:34:37Z",
        "submit_time": "2021-05-18T18:34:39Z"
    },
    {
        "student_name": "student2",
        "supervisor_name": "supervisor2"git ,
        "enter_time": "2021-05-18T18:32:12Z",
        "submit_time": "2021-05-18T18:32:14Z"
    },
    {
        "student_name": "student3",
        "supervisor_name": "supervisor3",
        "enter_time": "2021-05-18T18:32:47Z",
        "submit_time": "2021-05-18T18:33:02Z"
    }
]
```
#### GET /exam/{exam_id}/marks/
* General:
    - Returns list of students marks in exam.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/{exam_id}/marks/ -H "Content-Type: application/json" "Authorization: Token <ACCESS_TOKEN>"
        ```
* Response Sample:
```sh
[
    {
        "id": 41,
        "student_name": "student 1",
        "mark": 40.0
    },
    {
        "id": 6,
        "student_name": "student 2",
        "mark": 39.5
    }
]
```
#### GET /exam/{exam_id}/violations/
* General:
    - Returns list of students marks in exam.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/{exam_id}/violations/ -H "Content-Type: application/json" "Authorization: Token <ACCESS_TOKEN>"
        ```
* Response Sample:
```sh
{
    "id": 165,
    "exam_name": "Performance",
    "violations": [
        {
            "id": 6,
            "student": "student1",
            "violation": "cheating from the mobile phone",
            "supervisor": "super2",
            "time": "2021-07-10 18:04:39.827472+00:00"
        },
        {
            "id": 18,
            "student": "student2",
            "violation": "cheating from the book",
            "supervisor": "super3",
            "time": "2021-07-11 01:37:53.449630+00:00"
        }
    ]
}
```
#### GET /exam/{exam_id}/student/{student_id}/
* General:
    - Returns the exam of the student.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/{exam_id}/student/{student_id}/  -H "Content-Type: application/json" "Authorization: Token <ACCESS_TOKEN>"
        ```
* Response Sample:
```sh
[
    {
        "student_name": "student 1",
        "student": 41,
        "exam": 13,
        "exam_name": "Movies",
        "question": 18,
        "question_text": "how old are you now wrong new?",
        "answer": 12,
        "answer_text": "Joe Fox",
        "is_correct": true
    },
    {
        "student_name": "student 1",
        "student": 41,
        "exam": 13,
        "exam_name": "Movies",
        "question": 19,
        "question_text": "how old are you now wrong new?",
        "answer": 17,
        "answer_text": "Sansa Stark",
        "is_correct": true
    },
    {
        "student_name": "student 1",
        "student": 41,
        "exam": 13,
        "exam_name": "Movies",
        "question": 20,
        "question_text": "how old are you now wrong new?",
        "answer": 20,
        "answer_text": "Chuck Noland",
        "is_correct": true
    }
]
```
#### GET /exam/{exam_id}/time-left/
* General:
    - Returns time left for the exam.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/{exam_id}/time-left/ -H "Content-Type: application/json" "Authorization: Token <ACCESS_TOKEN>"
        ```
* Response Sample:
```sh
{
    "time_left": "2:56:45.558412"
}
```

## For Examiner --- Programming Test
#### POST /programming-test/
* General:
    - Returns the data of the added programming test.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/programming-test/ -X POST -H "Content-Type: application/json"  "Authorization: Token <ACCESS_TOKEN>" -d
            '{
            "test_name":"programming test - python ",
            "test_startdate":"2021-09-27 02:25:33+02:00",
            "test_duration": 3.0
            }' 
            ```
* Response Sample:
```sh
{
    "id": 2,
    "test_name": "programming test - python",
    "test_startdate": "2021-09-27T00:25:33Z",
    "test_duration": 3.0,
    "examiner": 40
}
```


#### GET /programming-test/
* General:
    - Returns lists of programming tests for the logged in examiner.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/programming-test/ -H "Content-Type: application/json"  "Authorization: Token <ACCESS_TOKEN>"```
* Response Sample:
```sh
[
    {
        "id": 1,
        "test_name": "First programming test",
        "test_startdate": "2021-07-27T00:25:33Z",
        "test_duration": 3.0,
        "examiner": 40
    },
    {
        "id": 2,
        "test_name": "programming test - python",
        "test_startdate": "2021-09-27T00:25:33Z",
        "test_duration": 3.0,
        "examiner": 40
    }
]
```


#### GET /programming-test/{test_id}/
* General:
    - Returns a whole test.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/programming-test/{test_id}/ -H "Content-Type: application/json"  "Authorization: Token <ACCESS_TOKEN>"```
* Response Sample:
```sh
{
    "id": 1,
    "test": "First programming test",
    "startdate": "2021-07-27T00:25:33Z",
    "duration": 3.0,
    "questions": [
        {
            "id": 1,
            "text": "write a python fuction that takes an int list as an argument and returns the sum of it elements , list_sum(numbers)  , call it 2 time for (30 60 5 7 95 21) ( 4 51 -25 96 -74 60)"
        },
        {
            "id": 2,
            "text": "write a python fuction that takes an int list as an argument and returns the average of it elements , list_avg(numbers)  , call it 2 time for (30 60 5 7 95 21) ( 4 51 -25 96 -74 60)"
        }
    ]
}
```

#### POST /programming-test/{test_id}/question/
* General:
    - Returns the question that has been added.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/programming-test/{tes_id}/question/ -X POST -H "Content-Type: application/json"  "Authorization: Token <ACCESS_TOKEN>" -d
            '{ "text" : "write a python fuction that takes an int list as an argument and returns the sum of it elements , list_sum(numbers)  , call it 2 time for (30 60 5 7 95 21) ( 4 51 -25 96 -74 60) " }' 
        ```
* Response Sample:
```sh
{
    "id": 1,
    "text": "write a python fuction that takes an int list as an argument and returns the sum of it elements , list_sum(numbers)  , call it 2 time for (30 60 5 7 95 21) ( 4 51 -25 96 -74 60)",
    "test": 1
}
```


#### POST /programming-test/{test_id}/allowed-students/
* General:
    - Returns 201 or 400
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/programming-test/{test_id}/allowed-students/ -X POST -H "Content-Type: application/json" "Authorization: Token <ACCESS_TOKEN>" -d
            '{
                "students":["student1","student2"]
            }' 
        ```
* Response Sample:
```sh
{
    "id": 2,
    "student": [
        10,
        6
    ],
    "test" 1
}
```
#### GET programming-test/{test_id}/allowed-students/
* General:
    - Returns list of students allowed to enter the exam.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/programming-test/{test_id}/allowed-students/ -H "Content-Type: application/json" "Authorization: Token <ACCESS_TOKEN>"
        ```
* Response Sample:
```sh
    {
    "test": 1,
    "student": [
        "student1",
        "student2"
    ]
}
```


#### GET /programming-test/{test_id}/student/{student_id}/
* General:
    - Returns the test answers of the student.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/programming-test/{test_id}/student/{student_id}/  -H "Content-Type: application/json" "Authorization: Token <ACCESS_TOKEN>"
        ```
* Response Sample:
```sh
[
    {
        "student_name": "ameerstudent",
        "student": 28,
        "test": 3,
        "test_name": "programming test - ruby",
        "question": 3,
        "question_text": "write a ruby fuction that takes an int list as an argument and returns the sum of it elements",
        "answer": "x=2 \ny=5\nprint(x+y)",
        "programming_language": "python3",
        "output": "{\"output\":\"7\\n\",\"statusCode\":200,\"memory\":\"7348\",\"cpuTime\":\"0.02\"}"
    },
    {
        "student_name": "ameerstudent",
        "student": 28,
        "test": 3,
        "test_name": "programming test - ruby",
        "question": 4,
        "question_text": "write a ruby fuction that takes an int list as an argument and returns the avg of it elements",
        "answer": "x=2 \ny=5\nprint(x+y)",
        "programming_language": "python3",
        "output": "{\"output\":\"7\\n\",\"statusCode\":200,\"memory\":\"7432\",\"cpuTime\":\"0.01\"}"
    }
]
```
## For Student:
#### GET student/dashboard/
* General:
    - Returns all exams for the logged in student.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/student/dashboard/ -H "Authorization: Token <ACCESS_TOKEN>" ```
* Response Sample:
```sh
[
    {
        "exam_id": 140,
        "exam_name": "Movies",
        "student_id": 6,
        "student_name": "stu1",
        "full_mark": 20.0,
        "student_mark": 10.0,
        "is_started": "The Exam is Closed"
    },
    {
        "exam_id": 163,
        "exam_name": "Physics",
        "student_id": 6,
        "student_name": "stu1",
        "full_mark": 4.0,
        "student_mark": 0,
        "is_started": "The Exam is Open"
    },
    {
        "exam_id": 147,
        "exam_name": "Maths",
        "student_id": 6,
        "student_name": "stu1",
        "full_mark": 100.0,
        "student_mark": 0,
        "is_started": "The Exam is Closed"
    }
]
```


#### GET /exam/{exam_id}/start/
* General:
    - Returns the whole exam for the student.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/{exam_id}/start/ -H "Authorization: Token <ACCESS_TOKEN>" ```
* Response Sample:
```sh
{
    "exam_name": "Exam test",
    "exam_starttime": "2021-05-09T20:47:36Z",
    "exam_duration": 4.0,
    "questions": {
        "how old are you now wrong ?": {
            "mark": 1.0,
            "previous_question": null,
            "answers": {}
        },
        "how old are you now wrong 2?": {
            "mark": 1.0,
            "previous_question": null,
            "answers": {
                "10": "answer 1",
                "11": "answer 2"
            }
        }
    }
}
```
#### POST /exam/{exam_id}/submit/
* General:
    - Submits all exam answers for the student.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/{exam_id}/submit/ -X POST -H "Content-Type: application/json" "Authorization: Token <ACCESS_TOKEN>" -d
            '{
    "student_answers":
    {
        "18" : 12, 
        "19":17,
        "20" : 20, 
        "21":24,
        "22":29
    }
}'```
    -  where question id and 12 is chosen answer id
* Response Sample:
```sh
HTTP 200 OK
```

## For Student --  Programming


#### GET student/dashboard/programming-tests/
* General:
    - Returns all programming tests for the logged in student.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/student/dashboard/programming-tests/ -H "Authorization: Token <ACCESS_TOKEN>" ```
* Response Sample:
```sh
[
{"test_id":1,"test_name":"First programming test",
"test_startdate":"2021-07-27T00:25:33Z",
"test_duration":3.0,"student_id":28,
"student_name":"ameerstudent"
} ,

{"test_id":2,"test_name":"programming test - python",
"test_startdate":"2021-07-29T00:25:33Z",
"test_duration":3.0,"student_id":28,
"student_name":"ameerstudent"
}

]
```

#### GET /programming-test/{test_id}/start/
* General:
    - Returns the whole exam for the student.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/programming-test/{test_id}/start/ -H "Authorization: Token <ACCESS_TOKEN>" ```
* Response Sample:
```sh
{
"test_name":"programming test - ruby",
"test_starttime":"2021-07-10T22:00:00Z",
"test_duration":24.0,
"questions":
{"3":"write a ruby fuction that takes an int list as an argument and returns the sum of it elements",
"4":"write a ruby fuction that takes an int list as an argument and returns the avg of it elements"}}
```

#### POST /programming-test/{test_id}/submit/
* General:
    - Submits all exam answers for the student.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/programming-test/{test_id}/submit/ -X POST -H "Content-Type: application/json" "Authorization: Token <ACCESS_TOKEN>" -d
            '{
    {
    "student_answers"
    : 
    {
    "3" : ["python3" , "x=2 \ny=5\nprint(x+y)"],
    
    "4" : ["python3" , "x=2 \ny=5\nprint(x+y)"] 
    }
    }
}'```
    -  where question id   is 3   and python3  is chosen programming language , "x=2 \ny=5\nprint(x+y)" is the code snippet and it should be an escaped string
* Response Sample:
```sh
HTTP 200 OK
```


## For Supervisor:
#### GET supervisor/dashboard/
* General:
    - Returns list of exams for the logged in supervisor.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/supervisor/dashboard/ -H "Content-Type: application/json" "Authorization: Token <ACCESS_TOKEN>"
        ```
* Response Sample:
```sh
[
    {
        "exam_id": 165,
        "exam_name": "Performance",
        "exam_startdate": "2021-06-27T23:37:05Z",
        "exam_duration": 2.0,
        "is_started": "The Exam is Open"
    }
]
```
#### GET exam/{exam_id}/supervise/
* General:
    - Returns some exam details and assigned students to supervise.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/{exam_id}/supervise/ -H "Content-Type: application/json" "Authorization: Token <ACCESS_TOKEN>"
        ```
* Response Sample:
```sh
{
    "exam_id": 165,
    "exam_name": "Performance",
    "exam_startdate": "2021-06-27T23:37:05Z",
    "exam_duration": 3.0,
    "students": [
        {
            "student_id": 6,
            "student_name": "stu1"
        },
        {
            "student_id": 19,
            "student_name": "stu2"
        },
        {
            "student_id": 1,
            "student_name": "stu3"
        }
    ]
}
```
#### POST exam/{exam_id}/supervise/student/{student_id}/
* General:
    -Assigned supervisor can reports a violation.
* Request Sample: ```curl http://ec2-18-191-113-113.us-east-2.compute.amazonaws.com:8000/exam/{exam_id}/supervise/student/{student_id}/ -H "Authorization: Token <ACCESS_TOKEN>" ```
* Response Sample:
```sh
{
    "violation": "cheating from the mobile phone"
}
```
* Response Sample:
```sh
200 OK
```
