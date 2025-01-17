import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# paginating the questions
def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * 10
    end = start + 10

    if start < 0 or start >= len(selection):
        abort(404)

    questions = [question.format() for question in selection]
    current_question = questions[start:end]

    return current_question

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization, true"
        )
        response.headers.add(
            "Access-Control-Allow-Headers", "GET, POST, PATCH, DELETE, OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route('/categories')

    def get_categories():

        categories = Category.query.order_by(Category.id).all()
        category_list = {item.id: item.type for item in categories}

        if len(categories) == 0:
            abort(404)

        return jsonify ({
            'success': True,
            'categories': category_list
        })

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
        questions = Question.query.order_by(Question.category).all()
        categories = Category.query.order_by(Category.id).all()
        cur_questions = paginate_questions(request, questions)

        if len(questions) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "questions": cur_questions,
            "total_questions": len(questions),
            "categories": {item.id: item.type for item in categories}
        })
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<int:question_id>', methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                "success": True,
                "question_deleted": question_id,
                "total_questions": len(Question.query.all())
            })
        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/questions', methods=["POST"])
    def create_question():
        body = request.get_json()


        new_question = body.get('question')
        new_answer = body.get('answer')
        new_category = body.get('category')
        new_difficulty = body.get('difficulty')

        if not ('question' in body and 'answer' in body and
                'difficulty' in body and 'category' in body):
            abort(422)

        try:
            question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)

            question.insert()

            selection = Question.query.order_by(Question.id).all()
            cur_question = paginate_questions(request, selection)

            return jsonify({
                "success": True,
                "created": question.id,
                "new_question": question.question,
                "questions": cur_question,
                "total_questions": len(Question.query.all())
                
            })
        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/questions/search', methods=["POST"])
    def search_questions():
        body = request.get_json()
        
        search = body.get("searchTerm", None)

        if search is None:
            abort(404)

        try:
            if search:
                selection = Question.query.filter(Question.question.ilike(f"%{search}%")).all()

                current = paginate_questions(request, selection)

                return jsonify({
                    "success": True,
                    "questions": current,
                    "total_question": len(selection) 
                })
        except:
            abort(404)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    
    @app.route('/categories/<int:id>/questions', methods=["GET"])
    def get_categories_questions(id):
        try:
            category = Category.query.get(id)

            if category is None:
                abort(404)

            selection = Question.query.filter_by(category=category.id).all()
            pagination = paginate_questions(request, selection)

            return jsonify({
                "success": True,
                "questions": pagination,
                "total_question": len(Question.query.all()),
                "current_category": category.type
            })
        except:
            abort(404)


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

    @app.route('/quizzes', methods=["POST"])
    def play_quiz():
        try:
            body = request.get_json()
            previous_questions = body.get('previous_questions', [])
            quiz_category = body.get('quiz_category', None)

            if quiz_category:
                get_category = quiz_category['id']
                if get_category == 0:
                    show_questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
                else:
                    show_questions = Question.query.filter(Question.category == get_category, Question.id.notin_(previous_questions)).all()
            
            if show_questions:
                randomized = random.choice(show_questions).format()
            else:
                randomized = None

            return jsonify({
                "success": True,
                "question": randomized
            })

        except:
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "error": 404, "message": "resource not found"}), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({"success": False, "error": 405, "message": "method not allowed"}), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({"success": False, "error": 422, "message": "unprocessable"}), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({"success": False, "error": 500, "message": "server error"}), 500

    return app

