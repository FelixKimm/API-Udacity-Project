import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        # setup_db(self.app, self.database_path)

        self.new_question = {"question": "who is the goat", "answer": "messi", "category": "6", "difficulty": "1" }

        # # binds the app to the current context
        # with self.app.app_context():
        #     self.db = SQLAlchemy()
        #     self.db.init_app(self.app)
        #     # create all tables
        #     # self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_paginate_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_404_paginate_questions_error(self):
        res = self.client().get('/questions?page=1234')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_404_get_categories(self):
        res = self.client().get('/categories?page=1234')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_question(self):
        res = self.client().delete('/questions/26')
        data =json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_422_delete_not_existing_question(self):
        res = self.client().delete('/questions/1234')
        data =json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)

    def test_create_questions(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_405_create_questions(self):
        res = self.client().post('/questions/1234', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)

    def test_search_question(self):
        res = self.client().post('/questions/search', json={
             'searchTerm': 'Testing'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_404_search_question(self):
        res = self.client().post('/questions/search', json={
            'searchTerm': 'notinthedatabase'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False) 

    def test_get_cat_question(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_404_get_cat_question(self):
        res = self.client().get('/categories/1234/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_play_quiz(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [],
            'quiz_category': {'id': 6, 'type': 'Sports'}
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_play_quiz(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [],
            'quiz_category': None
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)

    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()