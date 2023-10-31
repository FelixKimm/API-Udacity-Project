# Udacity Full Stack Trivia API Project

This project allows you to play a trivia game with an API that was created from the ground up. This project allows you to:

1 - Display questions - both all questions and by category. Questions should show the question, category, and difficulty rating by default and can show/hide the answer.
2 - Delete questions.
3 - Add questions and require that they include the question and answer text.
4 - Search for questions based on a text query string.
5 - Play the quiz game, randomizing either all questions or within a specific category.

## Requirements

### Installing dependencies

### Frontend dependencies

1. **Installing Node and NPM**
   This project depends on Nodejs and Node Package Manager (NPM).

2. **Installing project dependencies**
   This project uses NPM to manage software dependencies.

```bash
npm install
```

### Backend dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

## Running your frontend

The frontend app was built using create-react-app. In order to run the app in development mode use `npm start`. You can change the script in the `package.json` file.

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.

```bash
npm start
```

## Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Documentation for Trivia API

### Reference

The Trivia API is a REST API, this particular doesn't need an authentication key, and is hosted locally at http://127.0.0.1:5000/ or http://localhost:5000/

### Endpoints

#### GET '/categories'

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key: value pairs.

```
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

#### GET '/questions'

- Fetches a dictionary of 10 questions per grouping, that includes the category, question, answer, difficulty and id
- Returns: An object with 10 questions:

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
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        },
        {
            "answer": "Answer is yes",
            "category": 1,
            "difficulty": 1,
            "id": 26,
            "question": "Testing the first post question2"
        },
        {
            "answer": "There are no answer",
            "category": 1,
            "difficulty": 1,
            "id": 24,
            "question": "Testing the first post question"
        },
        {
            "answer": "Yes",
            "category": 1,
            "difficulty": 1,
            "id": 37,
            "question": "Test on the front"
        },
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        }
    ],
    "success": true,
    "total_questions": 18
}
```

### DELETE '/questions/int:id'

- Deletes a specific question using the id of the question
- Returns: The id of the deleted question and the total remaining questions

```
{
    "question_deleted": 24,
    "success": true,
    "total_questions": 17
}
```

### POST '/questions'

- Create a new question
- Category from 1-6 and difficulty from 1-5
- Body:
```
{
    "question": "This is an example",
    "answer": "example",
    "category": "6",
    "difficulty": "1"
}
```

### POST '/questions/search'

- Searches a question using the input given
- Returns: the question searched and the total number of questions

```
```

### GET '/categories/int:id/questions'

- Fetches all questions from a specific category
- Returns: An object with the questions from the specified category

```
{
    "current_category": "Art",
    "questions": [
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        }
    ],
    "success": true,
    "total_question": 17
}
```

### POST '/quizzes'

- Allows the user to play the trivia game
- Request Body (JSON):

```
{
    "previous_question": 1
    "quiz_category": { id: 1}
}
```

## Errors

The errors that the API will return are:

- 400: bad request
- 404: resource not found
- 405: method not allowed
- 422: unprocessable
- 500: server error