from . import game
from flask_login import current_user, login_required
from flask import render_template, abort, request, Response, session
from bson import ObjectId
from app.MongoFunction import db
from .. import socketio
from flask_socketio import emit, join_room, leave_room, disconnect, Namespace
import json
from pprint import  pprint

#background green thread
def pvp_room_thread(evt):
    #每有新数据立即推送新数据，会导致多人操作时发送过于频繁，所以统一每秒更新数据
    while True:
        socketio.sleep(1)
        if evt.ready():
            evt.reset()

            socketio.emit('json_room',{'data': 'Server generated event'},namespace='/pvp', broadcast=1)

@socketio.on('connect', namespace='/pvp')
def on_connect():
    print("connect",request.namespace)
    print("pvp Client connected")

@socketio.on('disconnect', namespace='/pvp')
def on_disconnect():
    print("pvp Client disconnected")

@socketio.on('message', namespace='/pvp')
def text(message):
    print("\n\n\n\n","text",message,"\n\n\n\n")
    return "message was received by server"

@socketio.on('new_room', namespace='/pvp')
def new_room(data):
    print("\n\n\n\n","new_room",data,"\n\n\n\n")
    room = {
        "course":data['course'],
        "type":data['type'],
        "player":data["player"]
        }
    result = db.rooms.insert_one(room)
    room["_id"] = str(result.inserted_id)
    emit("new_room",room,namespace="/pvp",broadcast=1)
    return "new_room was received by server"

@game.route('/leave_room', methods=['POST'])
def leave_room():
    # affected = db.rooms.find({
    #     "player":request.form.getlist("user"),
    # })
    result = db.rooms.delete_many({
        "player":{ "$in" : request.form.getlist("user")},
    })
    if result.acknowledged:
        return Response(json.dumps({"status":result.acknowledged}, default=str), mimetype='application/json')
    else:
        return ""

@game.route('/get_rooms', methods=['GET'])
def get_rooms():
    cur = db.rooms.find({"course":request.args["course"]})
    return Response(json.dumps(list(cur), default=str), mimetype='application/json')