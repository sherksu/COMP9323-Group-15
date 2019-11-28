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
    dic = function.get_user_info(current_user.username)
    img = dic['avatar']
    return render_template("/profile/detail.html",
                           **dic, get_course_name=function.get_course_name, get_course_code=function.get_course_code,
                           img=img, get_chapter_name=function.get_chapter_name)


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
    dic = function.get_user_info(current_user.username)
    return render_template("/profile/question_set.html", **dic, get_question_content=function.get_question_content,
                           get_chapter_name=function.get_chapter_name, get_course_name=function.get_course_name,
                           get_course_code=function.get_course_code, get_question_course=function.get_question_course,
                           get_question_chapter=function.get_question_chapter,correct_answer = function.correct_answer,
                           get_question_option=function.get_question_option,get_question_correct_answer=function.get_question_correct_answer,
                           chr=chr,int=int,str=str,get_question_knowledge_node = function.get_question_knowledge_node,get_node_name = function.get_node_name)

@profile.route('/data_project/')
def data_project():
    return render_template(
        "/profile/data_project.html",
        user_name=current_user.username,
        project_list = ['Speed_dating', 'Olympic_medals']
    )
    

