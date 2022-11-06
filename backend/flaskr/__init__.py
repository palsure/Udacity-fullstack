import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import traceback
from werkzeug.exceptions import HTTPException

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.app_context().push()
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={'/': {'origins': '*'}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response): 
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # helper methods
    def get_paginated_questions(request, questions): 
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        current_questions = questions[start:end]
        return current_questions

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        try:
            if request.method != 'GET':
                abort(405)

            categories = Category.query.all()
            categories_data = {}

            for category in categories:
                categories_data[category.id] = category.type
  
            if (len(categories_data) == 0):
                abort(404)

            return jsonify({
                'success': True,
                'categories': categories_data,
                'totalCategories': len(categories_data)
            })

        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                traceback.print_exc()
                abort(422)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        try:
            if request.method != 'GET':
                abort(405)

            questions = Question.query.all()
            questions = [question.format() for question in questions]
            total_questions = len(questions)
            current_questions = get_paginated_questions(request, questions)

            categories = Category.query.all()
            categories_data = {}

            for category in categories:
                categories_data[category.id] = category.type

            if (len(current_questions) == 0):
                abort(404)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': total_questions,
                'categories': categories_data
            })

        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                traceback.print_exc()
                abort(422)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            if request.method != 'DELETE':
                abort(405)

            question = Question.query.filter_by(id = question_id).one_or_none()
            
            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id
            })

        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                traceback.print_exc()
                abort(422)
        
        finally:
            db.session.close()

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions', methods=['POST'])
    def add_or_search_questions():
        try:
            if request.method != 'POST':
                abort(405)

            request_json = request.get_json()

            # If search term is present, return questions for the search term
            search_term = request_json.get('searchTerm', None)
            if (search_term is not None):
                if (len(search_term) < 3):
                    abort(400)

                search_results = Question.query.order_by(Question.id).filter(
                    Question.question.ilike("%{}%".format(search_term))).all()
                questions = [question.format() for question in search_results]
                
                if (len(questions) == 0):
                    abort(404)

                paginated_questions = get_paginated_questions(request, questions)
                
                return jsonify({
                    'success': True,
                    'questions': paginated_questions,
                    'total_questions': len(paginated_questions),
                    'search_term': search_term
                })

            # create new question
            else:
                question = request_json.get('question')
                answer = request_json.get('answer')
                difficulty = request_json.get('difficulty')
                category = request_json.get('category')

                if ((question is None) or (answer is None)
                        or (difficulty is None) or (category is None)):
                    abort(400)

                new_question = Question(question = question, 
                                        answer = answer, 
                                        difficulty = difficulty, 
                                        category = category)
                new_question.insert()

                questions = Question.query.order_by(Question.id).all()
                questions = [question.format() for question in questions]
                paginated_questions = get_paginated_questions(request, questions)

                return jsonify({
                    'success': True,
                    'created': new_question.id,
                    'question_created': new_question.question,
                    'questions': paginated_questions,
                    'total_questions': len(questions)
                }), 201

        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                traceback.print_exc()
                db.session.rollback()
                abort(422)
        
        finally:
            db.session.close()

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        try:
            if request.method != 'GET':
                abort(405)

            category = Category.query.filter_by(id = category_id).one_or_none()
            
            if (category is None):
                abort(404)

            category_questions = Question.query.filter_by(category = category_id).all()
            
            if (category_questions is None):
                abort(404)

            questions = [question.format() for question in category_questions]
            paginated_questions = get_paginated_questions(request, questions)

            return jsonify({
                'success': True,
                'questions': paginated_questions,
                'total_questions': len(questions),
                'current_category': category.type
            })
        
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                traceback.print_exc()
                abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route("/quizzes",methods=['POST'])
    def retrieve_quizzes_by_category():
        try:
            if request.method != 'POST':
                abort(405)
                
            request_json = request.get_json()
            quiz_category = request_json.get("quiz_category")
            previous_questions = request_json.get("previous_questions")

            if (quiz_category is None):
                abort(400) 
            elif (quiz_category['id'] == 0):
                category_questions = Question.query.all()
            elif (Category.query.filter_by(id = quiz_category['id']).one_or_none() is None):
               abort(400)
            else:
                category_questions = Question.query.filter(Question.category == quiz_category['id']).all()
            
            if (len(category_questions) == 0):
                abort(404)

            questions = [question.format() for question in category_questions]

            random.shuffle(questions)
            filtered_questions = []

            if previous_questions is None:
                filtered_questions = questions
            else:
                for question in questions:
                    if question['id'] not in previous_questions:
                        filtered_questions.append(question)

            if (len(filtered_questions) > 0):
                quiz_question = random.choice(filtered_questions)
            else:
                abort(404)
                    
            return jsonify({
                'success': True,
                'question': quiz_question,
                'previous_questions': previous_questions
            })  

        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                traceback.print_exc()
                abort(422)
        finally:
            db.session.close()

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False, 
            "error": 405, 
            "message": "method not allowed"
            }), 405

    @app.errorhandler(422)
    def unable_to_process(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unable to process the request"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app

