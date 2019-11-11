from flask import render_template,request
from flask_login import login_required,current_user
from app import db
from . import town


@town.route('/<course>')
@login_required
def entry_town(course):
    course = db.courses.find_one({'code': course})
    code = course['code']
    name = course['name']
    course_id = course['_id']
    chapters = db.chapters.find({'course': course_id})
    get_node = db.knowledge_nodes.find
    return render_template('/town/my_town.html',  course=course, is_town=True,
                           code=code, _id=course_id, name=name, chapters=list(chapters), get_node=get_node,
                           user_name=current_user.get_id())
