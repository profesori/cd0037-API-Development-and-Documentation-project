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
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['categories']))

    def test_get_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']), 10)
        self.assertTrue(len(data['categories']))

    def test_get_questions_beyod_offset(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['questions'], [])

    def test_delete_question(self):
        res = self.client().delete('/questions/2')
        self.assertEqual(res.status_code, 204)

    def test_delete_uknown_question(self):
        res = self.client().delete('/questions/1')
        self.assertEqual(res.status_code, 422)

    def test_add_question(self):
        new_question = {
            'question': 'How are you?',
            'answer': 'answer',
            'difficulty': 1,
            'category': 1
        }

        res = self.client().post('/questions', json=new_question)

        self.assertEqual(res.status_code, 204)

    def test_add_question_with_missing_data(self):
        new_question = {
            'answer': 'answer',
            'difficulty': 1,
            'category': 1
        }

        res = self.client().post('/questions', json=new_question)

        self.assertEqual(res.status_code, 422)

    def test_search_question(self):
        search_term = {
            'searchTerm': 'beetle'
        }

        res = self.client().post('/questions/search', json=search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['questions']), 1)

    def test_search_question_with_missing_data(self):
        search_term = {
            'kr': 'beetle'
        }

        res = self.client().post('/questions/search', json=search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)

    def test_get_questions_by_category(self):

        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['questions']), 4)

    def test_get_questions_by_uknown_category(self):

        res = self.client().get('/categories/150/questions')

        self.assertEqual(res.status_code, 400)

    def test_quiz(self):
        quiz_data = {
            'quiz_category': {
                'id': 2,
                'type': 'History'
            },
            'previous_questions': [16]
        }

        res = self.client().post('/quizzes', json=quiz_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(data['question']['id'], 16)

    def test_quiz_with_missing_data(self):
        quiz_data = {
            'previous_question': 16
        }

        res = self.client().post('/quizzes', json=quiz_data)

        self.assertEqual(res.status_code, 422)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
