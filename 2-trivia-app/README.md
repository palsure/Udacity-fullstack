# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

> View the [Frontend README](./frontend/README.md) for more details.

## API Reference
### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:

The API will return below error types when requests fail:
- 400: Bad Request
    ```
    {
        "success": False, 
        "error": 400,
        "message": "bad request"
    }
    ```
- 404: Resource Not Found
    ```
    {
        "success": False, 
        "error": 404,
        "message": "resource not found"
    }
    ```
- 405: Method Not Allowed
    ```
    {
        "success": False, 
        "error": 405,
        "message": "methgod not allowed"
    }
    ```
- 422: Not Processable 
    ```
    {
        "success": False, 
        "error": 422,
        "message": "unable to process the request"
    }
    ```
- 500: Internal Server Error 
    ```
    {
        "success": False, 
        "error": 500,
        "message": "internal server error"
    }
    ```

### Endpoints 
#### GET /categories
- General:
    - Returns available categories list and total categories.
- Request Sample: 
    `curl http://127.0.0.1:5000/categories`
- Response JSON:
    ```
    {
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true,
    "totalCategories": 6
    }
    ```
#### GET /questions
- General:
    - Returns categories and questions list, total questions.
    - Results are paginated in groups of 10.
- Request Sample: 
    `curl http://127.0.0.1:5000/questions` or `curl http://127.0.0.1:5000/questions?page=1`
- Resoponse JSON:
    ```
    {
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
        "answer": "Maya Angelou",
        "category": 4,
        "difficulty": 2,
        "id": 5,
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
        "answer": "Muhammad Ali",
        "category": 4,
        "difficulty": 1,
        "id": 9,
        "question": "What boxer's original name is Cassius Clay?"
        },
        {
        "answer": "Apollo 13",
        "category": 5,
        "difficulty": 4,
        "id": 2,
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
        "answer": "Tom Cruise",
        "category": 5,
        "difficulty": 4,
        "id": 4,
        "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
        "answer": "Edward Scissorhands",
        "category": 5,
        "difficulty": 3,
        "id": 6,
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
        "answer": "Brazil",
        "category": 6,
        "difficulty": 3,
        "id": 10,
        "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
        "answer": "Uruguay",
        "category": 6,
        "difficulty": 4,
        "id": 11,
        "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
        "answer": "George Washington Carver",
        "category": 4,
        "difficulty": 2,
        "id": 12,
        "question": "Who invented Peanut Butter?"
        },
        {
        "answer": "Lake Victoria",
        "category": 3,
        "difficulty": 2,
        "id": 13,
        "question": "What is the largest lake in Africa?"
        },
        {
        "answer": "The Palace of Versailles",
        "category": 3,
        "difficulty": 3,
        "id": 14,
        "question": "In which royal palace would you find the Hall of Mirrors?"
        }
    ],
    "success": true,
    "total_questions": 19
    }
    ```
#### DELETE /questions/{question_id}
- General:
    - Deletes the Question of the given ID if it exists. Returns the id of the deleted Question, success value.
- Request Sample: 
    `curl -X DELETE http://127.0.0.1:5000/questions/1`
- Resoponse JSON:
    ```
    {
        "success": true,
        "deleted": 1
    }
    ```
#### POST /questions
This endpoint support both new question creation and searching question using a search term.
1. Create New Question:
    - General:
        - Created new Question using question, answer, difficulty and category. Returns the id of the created Question, success value, question name, paginated questions and total questions.
    - Request Sample: 
        `curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"question": "What is your favorite sports?", "answer": "VolleyBall", "difficulty": 1, "category": 6}'`
    - Resoponse JSON:
        ```
        {
            'created': 83, 
            'question_created': 'What is your favorite sports?', 
            'questions': [
                {
                    'answer': 'Apollo 13', 
                    'category': 5, 
                    'difficulty': 4, 
                    'id': 2, 
                    'question': 'What movie earned Tom Hanks his third straight Oscar nomination, in 1996?'
                }, 
                {
                    'answer': 'Tom Cruise', 
                    'category': 5, 
                    'difficulty': 4, 
                    'id': 4, 
                    'question': 'What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?'
                }, 
                {
                    'answer': 'Maya Angelou', 
                    'category': 4, 
                    'difficulty': 2, 
                    'id': 5, 
                    'question': "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
                }, 
                {
                    'answer': 'Edward Scissorhands', 
                    'category': 5, 
                    'difficulty': 3, 
                    'id': 6, 
                    'question': 'What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?'
                }, 
                {
                    'answer': 'Muhammad Ali', 
                    'category': 4, 
                    'difficulty': 1, 
                    'id': 9, 'question': 
                    "What boxer's original name is Cassius Clay?"
                }, 
                {
                    'answer': 'Brazil', 
                    'category': 6, 
                    'difficulty': 3, 
                    'id': 10, 
                    'question': 'Which is the only team to play in every soccer World Cup tournament?'
                }, 
                {
                    'answer': 'Uruguay', 
                    'category': 6, 
                    'difficulty': 4, 
                    'id': 11, 
                    'question': 'Which country won the first ever soccer World Cup in 1930?'
                }, {
                    'answer': 'George Washington Carver', 
                    'category': 4, 
                    'difficulty': 2, 
                    'id': 12, 
                    'question': 'Who invented Peanut Butter?'
                }, {
                    'answer': 'Lake Victoria', 
                    'category': 3, 
                    'difficulty': 2, 
                    'id': 13, 
                    'question': 'What is the largest lake in Africa?'
                }, {
                    'answer': 'The Palace of Versailles', 
                    'category': 3, 
                    'difficulty': 3, 
                    'id': 14, 
                    'question': 'In which royal palace would you find the Hall of Mirrors?'
                }
            ], 
            'success': True, 
            'total_questions': 57
        }
        ```
2. Search Question's:
    - General:
        - Search questions using a search term. Returns the questions based on the serch term, success value, search term, and total questions.
    - Request Sample: 
        `curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"searchTerm": "first"}'`
    - Resoponse JSON:
        ```
        {
            'questions': [
                {
                    'answer': 'Tom Cruise', 
                    'category': 5, 
                    'difficulty': 4, 
                    'id': 4, 
                    'question': 'What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?'
                }, 
                {
                    'answer': 'Uruguay', 
                    'category': 6, 
                    'difficulty': 4, 
                    'id': 11, 
                    'question': 'Which country won the first ever soccer World Cup in 1930?'
                }
            ], 
            'search_term': 'first', 
            'success': True, 
            'total_questions': 2
        }
        ```
#### GET /categories/{category_id}/questions
- General:
    - Returns the list of Questions for the category id provided. Returns category name, list of Questions, success value and total questions.
- Request Sample: 
    `curl -X GET http://127.0.0.1:5000/categories/3/questions`
- Resoponse JSON:
    ```
    {
        'current_category': 'Geography', 
        'questions': [
            {
                'answer': 'Lake Victoria', 
                'category': 3, 
                'difficulty': 2, 
                'id': 13, 
                'question': 'What is the largest lake in Africa?'
            }, 
            {
                'answer': 'The Palace of Versailles', 
                'category': 3, 
                'difficulty': 3, 
                'id': 14, 
                'question': 'In which royal palace would you find the Hall of Mirrors?'
            }, 
            {
                'answer': 'Agra', 
                'category': 3, 
                'difficulty': 2, 
                'id': 15, 
                'question': 'The Taj Mahal is located in which Indian city?'
            }
        ], 
        'success': True, 
        'total_questions': 3
    }
    ```
#### POST /quizzes
- General:
    - Returns a random question as a quiz based on the requested category and previous questions or from the list of questions.
- Request Sample: 
    `curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"previous_questions": [1, 2], "quiz_category": {"type": "Art", "id": "2"}}'`
    or
    `curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{}'`
- Resoponse JSON:
    ```
    {
        'previous_questions': [1, 2], 
        'question': {
            'answer': 'One', 
            'category': 2, 
            'difficulty': 4, 
            'id': 18, 
            'question': 'How many paintings did Van Gogh sell in his lifetime?'
        }, 
        'success': True
    }
    ```
## Deployment N/A

## Authors
Yours truly, Suresh Palus

