from . import knowledge_structure
from flask import render_template
from .. import db
from bson import ObjectId


@knowledge_structure.route('/<course>')
@knowledge_structure.route('/<course>/<chapter>/<node>')
def specific_page(course, chapter='', node=''):
    try:
        courses = db.courses.find_one({"code": course})
        chapters = db.chapters.find({"course": courses['_id']})
    except TypeError:
        courses = db.courses.find_one({"_id": ObjectId(course)})
        chapters = db.chapters.find({"course": courses['_id']})
    if chapter and node:
        chapter = db.chapters.find_one({"name": chapter})
        node = db.knowledge_nodes.find_one({"name": node})
    return render_template('/knowledge_structure/nodes.html',
                           course=courses, chapters=chapters, db=db, chapter=chapter, node=node)
