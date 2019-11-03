from . import profile
from flask import render_template
from flask_login import current_user
from app.MongoFunction import *


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


@profile.route('/ranking/')
def ranking():
    # use three functions, all from the MongoFunction.py
    # first extract the username
    username = current_user.username
    # then get the list of the course_id he is doing
    user = db.users.find_one({"username": username})
    user_id = user['_id']
    course_id_list = get_user_course_list(user_id)

    if course_id_list:      # if the course list is not empty
        # extract the ranking
        course_code_name_list = get_course_code_name_list(course_id_list)
        total_rank_list = []
        for each_course in course_id_list:
            total_rank_list.append(get_list_of_level_rank(each_course))

        # render the template
        return render_template('/profile/ranking.html',
                               username=username,
                               noCourse=False,
                               course_code_name_list=course_code_name_list,
                               total_rank_list=total_rank_list,
                               enumerate=enumerate)

    else:
        return render_template('/profile/ranking.html',
                               username=username,
                               noCourse=True)


@profile.route('/question_set/')
def question_set():
    dic = get_user_info(current_user.username)
    print(dic)
    return render_template("/profile/question_set.html", **dic, get_question_content=get_question_content,
                           get_chapter_name=get_chapter_name, get_course_name=get_course_name,
                           get_course_code=get_course_code, get_question_course=get_question_course,
                           get_question_chapter=get_question_chapter,correct_answer = correct_answer)


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
