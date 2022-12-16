import os
import sys
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
# db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
        where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks")
def get_drinks():
    try:
        # Allows only GET request
        if request.method != 'GET':
            abort(405)
        # Gets all drinks
        drinks = Drink.query.order_by(Drink.id).all()
        # Returns error 404 if no drinks available
        if len(drinks) == 0:
            abort(404)
        # created dictionary of all drinks with short
        drinks_data = [drink.short() for drink in drinks]
        # returns json response with 200 status
        return jsonify(
            {
                "success": True,
                "drinks": drinks_data
            }
        ), 200
    except Exception as e:
        if isinstance(e, HTTPException):
            abort(e.code)
        else:
            print(sys.exc_info())
            # Returns error 422 unprocessable
            abort(422)


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
        where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks-detail")
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    try:
        # Allows only GET request
        if request.method != 'GET':
            abort(405)
        # Gets all drinks
        drinks = Drink.query.order_by(Drink.id).all()
        # Returns error 404 if no drinks available
        if len(drinks) == 0:
            abort(404)
        # created dictionary of all drinks with long
        drinks_data = [drink.long() for drink in drinks]
        # returns json response with 200 status
        return jsonify(
            {
                "success": True,
                "drinks": drinks_data
            }
        ), 200
    except Exception as e:
        if isinstance(e, HTTPException):
            abort(e.code)
        else:
            print(sys.exc_info())
            # Returns error 422 unprocessable
            abort(422)


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
        where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks", methods=['POST'])
@requires_auth('post:drinks')
def create_drink(jwt):
    try:
        # Allows only POST request
        if request.method != 'POST':
            abort(405)
        # gets drink details from request
        request_json = request.get_json()
        drink_title = request_json.get('title', None)
        drink_recipe = request_json.get('recipe', None)
        # Returns error 400 if drink title or recipe is missing in request
        if ((drink_title is None) or (drink_recipe is None)):
            abort(400)
        # create new drink bject
        drink = Drink(
            title=drink_title,
            recipe=json.dumps(drink_recipe)
        )
        # save new drink bject
        drink.insert()
        # returns json response with 200 status
        return jsonify(
            {
                "success": True,
                "drinks": [drink.long()]
            }
        ), 200
    except Exception as e:
        if isinstance(e, HTTPException):
            abort(e.code)
        else:
            print(sys.exc_info())
            # Returns error 422 unprocessable
            abort(422)


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
        where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(jwt, drink_id):
    print(drink_id)
    try:
        # Allows only PATCH request
        if request.method != 'PATCH':
            abort(405)
        # gets drink details from request
        request_json = request.get_json()
        drink_title = request_json.get('title', None)
        drink_recipe = request_json.get('recipe', None)
        # Returns error 400 if drink title or recipe is missing in request
        if ((drink_title is None) and (drink_recipe is None)):
            abort(400)
        # gets drink details from db for drink_id
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        # returns 404 error if no drink found for drink_id
        if (drink is None):
            abort(404)
        # update details for drink
        if drink_title:
            drink.title = drink_title
        if drink_recipe:
            drink.recipe = drink_recipe
        drink.update()
        # returns json response with 200 status
        return jsonify(
            {
                "success": True,
                "drinks": [drink.long()]
            }
        ), 200
    except Exception as e:
        if isinstance(e, HTTPException):
            abort(e.code)
        else:
            print(sys.exc_info())
            # Returns error 422 unprocessable
            abort(422)


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id}
        where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, drink_id):
    try:
        # Allows only DELETE request
        if request.method != 'DELETE':
            abort(405)
        # gets frink details from db for drink_id
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        # returns 404 error if no drink found for drink_id
        if (drink is None):
            abort(404)
        # deletes drink from db
        drink.delete()
        # returns json response with 200 status
        return jsonify(
            {
                "success": True,
                "delete": drink_id
            }
        ), 200
    except Exception as e:
        if isinstance(e, HTTPException):
            abort(e.code)
        else:
            print(sys.exc_info())
            # Returns error 422 unprocessable
            abort(422)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


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


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
    }), 500


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": 'Unathorized'
    }), 401
