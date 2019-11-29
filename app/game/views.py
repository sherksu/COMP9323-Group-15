from . import game
from flask import render_template, abort, request,send_from_directory,current_app,Response
from app.MongoFunction import *
from flask_login import current_user, login_required
import re
from datetime import datetime
from bson import ObjectId
from pprint import pprint
from time import time
import pandas as pd
import os.path
import json
from app import answer_buffer,QUESTION_NUM,MCQ_QUESTION_NUM
from flask_socketio import emit,leave_room, rooms
from .. import socketio
from collections import defaultdict
# TODO 1. 排版 2. 游戏规则

id_regex = re.compile("^[0-9a-fA-F]{24}$")


def is_obid(ids):
    return id_regex.match(ids)

@login_required
@game.route('/download_csv', methods=['GET'], strict_slashes=False)
def download_csv():
    print("\ndownload_csv")
    print(request.files)
    print(current_app.static_folder,"\n")
    #send_from_directory handle the file not found exception with proper information
    return send_from_directory(current_app.static_folder,"game/csv/"+request.args["file"])

def add_pvplevel(room, username):
    cur = db.rooms.find_one({"_id": ObjectId(room)})
    if cur:
        roomdata = dict(cur)
        # print(roomdata)
        result = get_list_of_pvplevels(username, roomdata["course"])
        print("result",result)
        if not result or "pvplevels" not in result[0] or  result[0]["pvplevels"] is None:
            db.users.update({"username":username},{"$push":{"pvplevels":{"course":roomdata["course"],"wins":1}}})
            wins=0
        else:
            db.users.update({"username": username}, {"$pull": {"pvplevels": {"course": roomdata['course']}}})
            print({
                "course":roomdata["course"],
                "wins":result[0]["pvplevels"][0]["wins"]+1
            })
            wins=result[0]["pvplevels"][0]["wins"]
            db.users.update({"username": username}, {"$push": {"pvplevels": {
                "course":roomdata["course"],
                "wins":result[0]["pvplevels"][0]['wins']+1
            }}})
    return wins

def win_game(room,name=""):
    print("\nwin_game")

    if room in answer_buffer and len(answer_buffer[room]) == QUESTION_NUM:
        count = defaultdict(int)
        for k, v in answer_buffer[room['room']].items():
            count[v] += 1
        max = 0
        winner = ""
        for v in count.values():
            if v > max:
                max = v
                winner = k
        print("winner",winner,room)
        wins = add_pvplevel(room,winner)
        socketio.emit("win", {"winner": winner,
                              "answer": answer_buffer[room],
                              "wins":wins
                              },
                      room=room,
                      namespace='/pvp',
                      broadcast=1)
    else:
        cur = db.rooms.find_one({"_id": ObjectId(room)})
        if cur:
            roomdata = dict(cur)
        print("surviver",roomdata["player"],room )
        if len(roomdata['player']) == 1:
            wins = add_pvplevel(room, roomdata['player'][0])
        socketio.emit("win",{"winner":name,
        "answer":answer_buffer[room] if room in answer_buffer else {},
                             "wins": wins
                             },
                          room=room,
                          namespace='/pvp',
                          broadcast=1)
    print("\n")
    db.rooms.delete_one({"_id": ObjectId(room)})

def finish_game(room,sid):
    print("\nfinishing ","\n")
    cur = db.rooms.find_one({"_id": ObjectId(request.form['room'])})
    data = dict(cur)
    if len(data["player"]) > 1:
        db.rooms.update_one({"_id":ObjectId(room)},{"$pull":{"player":current_user.get_id()}})
        print(rooms(sid = sid,namespace='/pvp'))
        socketio.emit('loss',
                      {
                          "answer": answer_buffer[room] if room in answer_buffer else {},
                          room: json.dumps(data,default=str)
                      },
                      room=sid,
                      namespace='/pvp',
                      sid = sid)
        leave_room(room,sid = sid,namespace='/pvp')
        print(rooms(sid = sid,namespace='/pvp'))
    else:
        win_game(room,data["player"][0])
@login_required
@game.route('/upload_answer', methods=['post'], strict_slashes=False)
def on_upload_answer():
    print("\nupload_answer")
    print(request.form)
    cur = db.question_set.find_one({"_id":ObjectId(request.form['name'])})
    data = dict(cur)
    print(int(data["correct_answer"]),int(request.form["value"]))
    if int(data["correct_answer"]) == int(request.form["value"]):
        if request.form['room'] not in answer_buffer:
            answer_buffer[request.form['room']]={}
        if request.form['name'] not in answer_buffer[request.form['room']]:
            answer_buffer[request.form['room']][request.form['name']] = request.form['username']
        if len(answer_buffer[request.form['room']]) == QUESTION_NUM:
            win_game(request.form['room'])
    else:
        finish_game(request.form['room'],request.form['sid'])

    print("\n")
    return Response(json.dumps(answer_buffer, default=str), mimetype='application/json')

@game.route('/upload_csv', methods=['POST'], strict_slashes=False)
# @login_required
def upload_csv():
    print("\nupload_csv")
    print(request.form)
    cur = db.question_set.find_one({"_id":ObjectId(request.form['question'])})
    data = dict(cur)
    if data:
        # print(data['correct_answer'])
        answer = pd.read_csv(current_app.static_folder+"/game/csv/"+data['correct_answer'])
        # pprint(answer)
        submited = pd.read_csv(request.files['fileToUpload'])
        # pprint(submited)
        print(answer.equals(submited))
        if answer.equals(submited) and "room" in request.form:
            # db.rooms.update({"_id":ObjectId(request.form['room']),ObjectId(request.form['room']):{"$exists":0}},{"$set":{ObjectId(request.form['room']):1}})
            if request.form['room'] not in answer_buffer:
                answer_buffer[request.form['room']] = {}
            if request.form['question'] not in answer_buffer[request.form['room']]:
                answer_buffer[request.form['room']][request.form['question']] = request.form['username']
            if len(answer_buffer[request.form['room']]) == QUESTION_NUM:
                win_game(request.form['room'])

        if not answer.equals(submited) and "room" in request.form :
            finish_game(request.form['room'],request.form['sid'])

        print("\n")
        return data['correct_answer'] if answer.equals(submited) else "0"
    else:
        return "0"

# pvp game - main process
@login_required
@game.route('/pvp/<course>', methods=['GET'], strict_slashes=False)
# @login_required
def pvp_game(course):
    print("\npvp_game")
    #if player refresh
    cur = db.rooms.find_one({"player": {"$in": [current_user.get_id()]},"game_start":True},{"quiz":1,"_id":0})
    if cur:
        data = dict(cur)['quiz']
        # print("\n\ndata refresh",data[0],"\n\n")
        return render_template('/game/pvp_game.html', data=data, name=current_user.get_id(), alter=len(data))

    # print(course)
    cur = db.courses.find_one({"code":course},{"_id":1})
    # print({"code":course},{"_id":1})
    if cur:
        data = dict(cur)
        # print(data)
        cur = db.question_set.aggregate([
            {"$match":{"course":data['_id']}},
            {"$sample":{"size":QUESTION_NUM}}
        ])
        if(cur):
            data = list(cur)
            db.rooms.update_one({"player":{"$in":[current_user.get_id()]},"game_start":True},{"$set":{"quiz":data}})
            print("\n")
            return render_template('/game/pvp_game.html', data=data, name=current_user.get_id(),alter=len(data))
    else:
        return "course is missing",404

# development
# @game.route('/draft/<room>', methods=['GET'], strict_slashes=False)
# # @login_required
# def boostrap_example(room):
#     print("\nwin_game")
#     print(current_user.get_id())
#     cur = db.rooms.find_one({"_id": ObjectId(room)})
#     if cur:
#         roomdata = dict(cur)
#         # print(roomdata)
#         result = get_list_of_pvplevels(current_user.username, roomdata["course"])
#         print("result",result)
#         if len(result) and "pvplevels" in result[0] and  not len(result[0]["pvplevels"]):
#             db.users.update({"username":current_user.username},{"$push":{"pvplevels":{"course":roomdata["course"],"wins":1}}})
#         else:
#             db.users.update({"username": current_user.username}, {"$pull": {"pvplevels": {"course": roomdata['course']}}})
#             print({
#                 "course":roomdata["course"],
#                 "wins":result[0]["pvplevels"][0]["wins"]+1
#             })
#             db.users.update({"username": current_user.username}, {"$push": {"pvplevels": {
#                 "course":roomdata["course"],
#                 "wins":result[0]["pvplevels"][0]['wins']+1
#             }}})
#             return "Success!"
#
#     print("\n")
#
#     return "404"

# pve game - main process
@game.route('/<model>/<node>', methods=['GET'], strict_slashes=False)
@login_required
def game_start(model, node):
    print("\n",request.path,request.method)
    node = node.lower()
    num = MCQ_QUESTION_NUM
    if not (node and num and is_obid(node)):
        abort(404)
    if model == "beginner":
        print("beginner")
        data = db.question_set.find({"knowledge_node": ObjectId(node),"type":"mcq"}).limit(num)
        data = list(data)
        # print(f"query",{"knowledge_node": ObjectId(node)})
        # pprint(data)
        node_name = db.knowledge_nodes.find_one({"_id": ObjectId(node)})
    elif model == "expert":
        data = db.question_set.aggregate([{"$match": {"chapter": ObjectId(node),"type":"mcq"}}, {"$sample": {"size": num}}])
        data = list(data)
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
                               chr=chr, level_info=level_info, node_id=node_name['course'])
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



