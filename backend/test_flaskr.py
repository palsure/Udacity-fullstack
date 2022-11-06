import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://postgres:abc@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
        # new question data
        self.new_question = {
            'question': 'What is your favorite sports?',
            'answer': 'VolleyBall',
            'difficulty': 1,
            'category': 6
        }

        # quiz data
        self.quiz = {
            'previous_questions': [1, 2],
            'quiz_category': {
                'type': 'Art', 
                'id': 2
            }
        }

        # quiz data
        self.quiz_all = {
            'previous_questions': [],
            'quiz_category': {
                'type': 'All', 
                'id': 0
            }
        }

        # quiz invalid data
        self.quiz_invalid = {
            'previous_questions': [10, 20],
            'quiz_category': {
                'type': 'Invalid', 
                'id': '100'
            }
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        response = self.client().get('/categories')
        response_data = json.loads(response.data)
        categories = Category.query.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(len(response_data['categories']) > 0)
        self.assertEqual(response_data['totalCategories'], len(categories))
    
    def test_get_categories_inavlid_405(self):
        response = self.client().post('/categories')
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'method not allowed')

    def test_get_questions(self):
        response = self.client().get('/questions')
        response_data = json.loads(response.data)
        questions = Question.query.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertEqual(response_data['total_questions'], len(questions))
        self.assertTrue(len(response_data['questions']))

    def test_get_questions_by_page(self):
        response = self.client().get('/questions?page=1')
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['total_questions'])
        self.assertTrue(len(response_data['questions']) <= QUESTIONS_PER_PAGE)

    def test_get_questions_invalid_404(self):
        response = self.client().get('/questions?page=1000')
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'resource not found')

    def test_delete_question(self):
        # add a new question
        question = Question(question = self.new_question['question'], 
                            answer = self.new_question['answer'],
                            category = self.new_question['category'], 
                            difficulty = self.new_question['difficulty'])
        question.insert()
        # delet the question added
        response = self.client().delete('/questions/{}'.format(question.id))
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertEqual(response_data['deleted'], question.id)
        question = Question.query.filter(Question.id == question.id).one_or_none()
        self.assertEqual(question, None)

    def test_delete_question_invalid_404(self):
        response = self.client().delete('/questions/-1')
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['success'], False)

    def test_create_question(self):
        request_data = self.new_question
        response = self.client().post('/questions', json = request_data)
        response_data = json.loads(response.data)
        total_questions = len(Question.query.all())
        question = Question.query.filter_by(id = response_data['created']).one_or_none()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data['success'], True)
        self.assertEqual(response_data['question_created'], request_data['question'])
        self.assertTrue(response_data['questions'])
        self.assertEqual(response_data['total_questions'], total_questions)
        self.assertIsNotNone(question)
        self.assertEqual(question.answer, request_data['answer'])
        self.assertEqual(question.category, request_data['category'])
        self.assertEqual(question.difficulty, request_data['difficulty'])

    def test_create_question_invalid_400(self):
        response = self.client().post('/questions', json = {})
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'bad request')

    def test_search_questions(self):
        search_term = 'first'
        response = self.client().post('/questions', json = {'searchTerm': search_term})
        response_data = json.loads(response.data)
        toatal_questions = len(Question.query.order_by(Question.id).filter(
                    Question.question.ilike("%{}%".format(search_term))).all())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertEqual(len(response_data['questions']), toatal_questions)
        self.assertTrue(response_data['questions'])
        self.assertEqual(response_data['search_term'], search_term)

    def test_search_questions_invalid_404(self):
        response = self.client().post('/questions', json = {'searchTerm': 'iiiiiiiiiiiii'})
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'resource not found')

    def test_get_questions_by_category(self):
        category_id = 3
        response = self.client().get('/categories/{}/questions'.format(category_id))
        response_data = json.loads(response.data)
        category_questions = Question.query.filter_by(category = category_id).all()
        category = Category.query.filter_by(id = category_id).one_or_none()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertEqual(len(response_data['questions']), len(category_questions))
        self.assertEqual(response_data['current_category'], category.type)

    def test_questions_by_category_invalid_404(self):
        response = self.client().get('/categories/1000/questions')
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'resource not found')

    def test_retrieve_quizzes_by_category(self):
        request_json = self.quiz
        response = self.client().post('/quizzes', json = request_json)
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['question'])
        self.assertEqual(response_data['question']['category'], 2)
        self.assertNotEqual(response_data['question']['id'], 1)
        self.assertNotEqual(response_data['question']['id'], 2)

    def test_retrieve_quizzes_all_category(self):
        response = self.client().post('/quizzes', json = self.quiz_all)
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['question'])
    
    def test_retrieve_quizzes_invalid_category_404(self):
        response = self.client().post('/quizzes', json = self.quiz_invalid)
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'resource not found')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()