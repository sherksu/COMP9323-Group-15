from . import game
from flask import render_template, abort, request
from app.MongoFunction import *
from flask_login import current_user, login_required
import re
from datetime import datetime
from bson import ObjectId
from pprint import pprint

# TODO 1. 排版 2. 游戏规则

id_regex = re.compile("^[0-9a-fA-F]{24}$")


def is_obid(ids):
    return id_regex.match(ids)

# pvp game - main process
@game.route('/pvp/<room>', methods=['GET'], strict_slashes=False)
# @login_required
def pvp_game(room):
    print("\n\n\n\npvp_game")
    # print(request.args)
    print("\n\n\n\n")
    return render_template('/game/pvp_game.html')

# development
@game.route('/boostrap_example', methods=['GET'], strict_slashes=False)
# @login_required
def boostrap_example():
    print("\n\n\n\nboostrap_example")
    # print(request.args)
    print("\n\n\n\n")
    return render_template('/game/boostrap_example.html')
    # return "<h1>HI</h1>"

# pve game - main process
@game.route('/<model>/<node>', methods=['GET'], strict_slashes=False)
@login_required
def game_start(model, node):
    print("\n",request.path,request.method)
    node = node.lower()
    num = 10
    if not (node and num and is_obid(node)):
        abort(404)
    if model == "beginner":
        print("beginner")
        data = db.question_set.find({"knowledge_node": ObjectId(node)}).limit(num)
        data = list(data)
        # print(f"query",{"knowledge_node": ObjectId(node)})
        # pprint(data)
        node_name = db.knowledge_nodes.find_one({"_id": ObjectId(node)})
    elif model == "random":
        data = db.question_set.aggregate([{"$match": {"chapter": ObjectId(node)}}, {"$sample": {"size": num}}])
        node_name = db.chapters.find_one({"_id": ObjectId(node)})
    else:
        abort(404)
    # print("if",data and node_name)
    if data and node_name:
        course_id = node_name['course']
        user_id = get_user_id(current_user.username)
        level_info = get_list_of_levels(user_id, course_id)['levels']
        print("\n")
        return render_template('/game/game.html',
                               data=data, node_name=node_name['name'], type=model.upper(),
                               chr=chr, level_info=level_info)
    else:
        abort(404)

# game_feedback save error set
@game.route('/error_save', methods=['POST'])
def save_error():
    data = eval(request.get_data().decode())
    for i in data:
        i["question"] = ObjectId(i["question"])
        i["date"] = datetime.now()
        db.users.update({"username": current_user.username}, {"$push": {"error_set": i}})
    return "Success!"


# game_feedback save level
@game.route('/level_save', methods=['POST'])
def save_level():
    data = eval(request.get_data().decode())
    data['course'] = ObjectId(data['course'])
    db.users.update({"username": current_user.username}, {"$pull": {"levels": {"course": data['course']}}})
    db.users.update({"username": current_user.username}, {"$push": {"levels": data}})
    return "Success!"



