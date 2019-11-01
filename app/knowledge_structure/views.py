from . import knowledge_structure
from flask import render_template
from .. import db


@knowledge_structure.route('/<course>')
@knowledge_structure.route('/<course>/<chapter>/<node>')
def specific_page(course, chapter='', node=''):
    course = db.courses.find_one({"code": course})
    chapters = db.chapters.find({"course": course['_id']})
    if chapter and node:
        chapter = db.chapters.find_one({"name": chapter})
        node = db.knowledge_nodes.find_one({"name": node})
    return render_template('/knowledge_structure/nodes.html',
                           course=course, chapters=chapters, db=db, chapter=chapter, node=node)
