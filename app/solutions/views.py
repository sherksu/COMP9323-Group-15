from . import solutionss
from flask import render_template, request
from flask_login import login_required
from app.MongoFunction import *
from datetime import datetime


@solutionss.route('/<question_id>')
@login_required
def solutions(question_id):
    question = get_question(question_id)
    q_id = question['_id']
    content = question['content']
    option = question['option']
    correct_answer = question['correct_answer']
    solution = question['solutions']
    return render_template('/solutions/solutions.html',
                           content=content, option=option, correct_answer=correct_answer,
                           solutions=solution, chr=chr, id=q_id)


@solutionss.route('/solution_save', methods=['POST'])
@login_required
def solution_save():
    data = eval(request.get_data().decode())
    q_id = data['id']
    del data['id']
    data['time'] = datetime.now()
    db.question_set.update({"_id": ObjectId(q_id)}, {"$push": {"solutions": data}})
    return 'Success!'
