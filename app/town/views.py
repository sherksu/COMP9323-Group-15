
from flask import render_template,request
from flask_login import login_required, current_user
from app.MongoFunction import *
from app import db
from . import town


@town.route('/<course>')
@login_required
def entry_town(course):
    user_id = db.users.find_one({'username': current_user.username})['_id']
    course = db.courses.find_one({'code': course})
    code = course['code']
    name = course['name']
    course_id = course['_id']
    chapters = db.chapters.find({'course': course_id})
    get_node = db.knowledge_nodes.find

    # level = get_list_of_levels(user_id, course_id)['levels'][0]
    level = 1
    return render_template('/town/my_town.html',  username=current_user.username, level=level, course=course,
                           is_town=True, code=code, _id=course_id, name=name, chapters=list(chapters),
                           get_node=get_node)
