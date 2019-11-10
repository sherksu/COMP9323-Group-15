from . import profile
from app.MongoFunction import *
from flask import render_template
from . import ranking_function as function
from flask_login import current_user


@profile.route('/', methods=['GET', 'POST'])
def personal_profile():
    dic = {
        'user_name': current_user.username,
    }
    return render_template("/profile/personal_profile.html", **dic)


@profile.route('/detail/', methods=['GET', 'POST'])
def detail():
    dic = get_user_info(current_user.username)
    img = dic['avatar']
    return render_template("/profile/detail.html",
                           **dic, get_course_name=get_course_name, get_course_code=get_course_code,
                           img=img, get_chapter_name=get_chapter_name)


# so the ranking is url /ranking
@profile.route('/ranking')
def ranking():
    # then get the list of the course_id he is doing
    username = current_user.username
    course_id_list = function.get_user_course_list(username)

    # if the course list is not empty
    if course_id_list:
        # extract the ranking
        course_code_name_list = function.get_course_code_name_list(course_id_list)
        total_rank_list = []
        for each_course in course_id_list:
            total_rank_list.append(function.get_list_of_level_rank(each_course))

        # construct a list, indicating the user's rank above all other uses
        position_list = function.get_position_list(username, total_rank_list)

        # render the template
        return render_template('/profile/ranking.html',
                               username=username,
                               course_code_name_list=course_code_name_list,
                               total_rank_list=total_rank_list,
                               position_list=position_list,
                               enumerate=enumerate,
                               len=len
                               )

    # if this person does no course, render another template
    else:
        return render_template('/profile/no_ranking.html',
                               username=username
                               )


@profile.route('/question_set/')
def question_set():
    dic = get_user_info(current_user.username)
    return render_template("/profile/question_set.html", **dic, get_question_content=get_question_content,
                           get_chapter_name=get_chapter_name, get_course_name=get_course_name,
                           get_course_code=get_course_code, get_question_course=get_question_course,
                           get_question_chapter=get_question_chapter,correct_answer = correct_answer)

@profile.route('/question_set_solutions/<question_id>')
def question_set_solutions(question_id):
    question = get_question(question_id)
    q_id = question['_id']
    content = question['content']
    option = question['option']
    correct_answer = question['correct_answer']
    solution = question['solutions']
    dic = get_user_info(current_user.username)
    for i in dic['error_set']:
        if i['question'] == q_id:
            user_answer = int(i['answer'])
    print(user_answer)
    return render_template("/profile/question_set_solutions.html",content=content, option=option, correct_answer=correct_answer,
                           solutions=solution, chr=chr, id=q_id,user_answer = user_answer)

@profile.route('/study_career/')
def study_career():
    return render_template("/profile/study_career.html", user_name=current_user.username)


def get_user_info(user_name):
    result = db.users.find_one({"username": user_name})
    return result


def get_course_name(course_id):
    course = db.courses.find_one({"_id": course_id})
    if course:
        return course['name']


def get_course_code(course_id):
    course = db.courses.find_one({"_id": course_id})
    if course:
        return course['code']


def get_chapter_name(chapter_id):
    chapter = db.chapters.find_one({"_id": chapter_id})
    if chapter:
        return chapter['name']


def get_question_content(question_id):
    question = db.question_set.find_one({"_id": question_id})
    if question:
        return question['content']


def get_question_course(question_id):
    question = db.question_set.find_one({"_id": question_id})
    if question:
        return question['course']


def get_question_chapter(question_id):
    question = db.question_set.find_one({"_id": question_id})
    if question:
        return question['chapter']
    
def correct_answer(str):
    if str == '1':
        return 'A'
    elif str == '2':
        return 'B'
    elif str == '3':
        return 'C'
    elif str == '4':
        return 'D'
