# API Guide

* `POST /api/create_load/` main app endpoint, creates load with provided data. `Hint: you may not to update or delete loads, just create the new one`.

     Example data to send:
     ```
  {
        "teacher": {
            "name": "Юрий",
            "surname": "Полозков",
            "patronymic": "Владимирович"
            },
        "discipline": {
            "name": "test",
            "semester": 2
            },
        "jobs": [
            {
                "id": 1,
                "input_value": 40
            },
            {
                "id": 2,
                "input_value": 46
            },
            {
                "id": 5,
                "input_value": 107
            },
            {
                "id": 6,
                "input_value": 41
            }
        ]
    }
  ```
    If teacher does not exists, it will be created automatically.
    If discipline does not exists it will be created automatically.
    Talking about discipline's semester, semester with id=0 is semester that has started from 01-01-2019, 1 is 01-09-2019 and so on.
    Jobs format have to include `id` is id of job instance, that used in system and input value.
    
    The return value is like:
    ```
    {
        "1": 40.0,
        "2": 46.0,
        "5": 32.1,
        "6": 16.400000000000002
    }
    ```
  There are jobs ids correlates with calculated value for each job.
  
  Make sure that you providing API token as `Authorization  Token xxxxxxxxxxxxxxxxxx`. (Then looks like 'You have to be authorized')
  
* `POST /api/login/` API endpoint, that returns token for existing user. Because current app is fully closed, you have to ask administrator for credentials.
    Request data have to be provided in this format:
    ```
        {
            "username": "admin",
            "password": "admin"
        }
    ```
    Endpoint should returns such data as:
    ```
        {
            "token": "c7119a79ebd9541fa5cb60b51f600b51327b6861"
        }
    ```

* `GET /api/jobs/` API endpoint to receive all existing jobs. You have to be authorized.
    Return value:
    ```
        [
            {
                "id": 1,
                "section": "student",
                "lesson_type": "lecture",
                "common_id": "1.1",
                "description": "Чтение лекций",
                "dimension": "Академических часов",
                "factor": 1.0,
                "additional_load_method": null,
                "additional_method_value": null,
                "validator_methods": [],
                "validator_values": []
            },
            ...]
    ```
 
 * `POST /api/jobs/` API endpoint to create job. You have to be authorized.
    Expected data example:
    ```
        {
            "section": "student",
            "lesson_type": "lecture",
            "common_id": "1.1",
            "description": "Чтение лекций",
            "dimension": "Академических часов",
            "factor": 1.0,
            "additional_load_method": null,
            "additional_method_value": null,
            "validator_methods": [],
            "validator_values": []
        }
    ```
