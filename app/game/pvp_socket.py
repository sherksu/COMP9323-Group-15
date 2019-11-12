from . import game
from flask_login import current_user, login_required
from flask import render_template, abort, request, Response, session
from bson import ObjectId
from app.MongoFunction import db
from .. import socketio, bg_task,client
from flask_socketio import emit, join_room, leave_room, disconnect, Namespace, rooms
import json
from pprint import  pprint

#background green thread
def bg_update_room(course):
    #每有新数据立即推送新数据，会导致多人操作时发送过于频繁，所以统一每秒更新数据
    while True:
        socketio.sleep(1)
        cur = db.rooms.find({"course": course})
        data = json.dumps(list(cur), default=str)
        # print("bg_update_room",data)
        socketio.emit('update_room',
                      data,
                      namespace='/pvp',
                      broadcast = 1,
                      skip_sid=1)

@socketio.on('connect',namespace="/pvp")
def on_connect():
    try:
        print("\nconnect to:",request.namespace)
        print(request.args)
        if request.args["course"] in bg_task and bg_task[request.args["course"]] == 0:
            bg_task[request.args["course"]] = socketio.start_background_task(bg_update_room,request.args["course"])
            bg_task[request.args["course"]] = 1
        print("\n")
    except Exception as e:
        pprint(e)

@socketio.on('reconnect', namespace='/pvp')
def on_reconnect(data):
    print("\nreconnect to:")
    print(data)
    print(request)
    print("\n")

@socketio.on('join', namespace='/pvp')
def on_join(data):
    try:
        print("\njoin to:",request.namespace,data["room"])
        join_room(data["room"])
        return {"status":1,"join":data["room"],"rooms":rooms()}
    except KeyError as e:
        return ""

@socketio.on('disconnect', namespace='/pvp')
def on_disconnect():
    print("pvp Client disconnected")

@socketio.on('message', namespace='/pvp')
def on_message(message):
    print("\n\n\n\n","text",message,"\n\n\n\n")
    return "message was received by server"

@socketio.on('echo', namespace='/pvp')
def on_echo(message):
    print("\n\n\n\n","echo",message,"\n\n\n\n")
    if "room" in message:
        for r in message["room"]:
            emit("echo",{"data":message["s"],"room":r,"rooms":rooms()}, namespace='/pvp',room=r)
    else:
        emit("echo", {"data": message["s"], "rooms": rooms()}, namespace='/pvp')
    return ("echo was received by server",rooms())

@socketio.on('new_room', namespace='/pvp')
def on_new_room(data):
    try:
        print("\n\n\n\n","new_room",data,"\n\n\n\n")
        room = {
            "course": data['course'],
            "type": data['type'],
            "player": data["player"]
        }
        result = db.rooms.insert_one(room)
        return json.dumps({"status": result.acknowledged,
                           "new_room": result.inserted_id,
                           }, default=str)
    except KeyError as e:
        return json.dumps({"status": result.acknowledged,
                           "msg": "KeyError",
                           }, default=str)

@socketio.on('change_room', namespace='/pvp')
def on_change_room(data):
    try:
        print("\n\n\n\n","change_room",data,dir(current_user))
        print(current_user.get_id())
        # emit("echo",data)

        with client.start_session() as s:
            s.start_transaction()
            db.rooms.update({"player": {"$in": [current_user.get_id()]}},
                                     {"$pull": {"player": current_user.get_id()}})
            db.rooms.delete_many({"player": []})
            db.rooms.update({"_id": ObjectId(data)}, {"$push": {"player": current_user.get_id()}})
            s.commit_transaction()
        return json.dumps({"status": 1,
                           # "new_room": result.inserted_id,
                           }, default=str)
    except Exception as e:
        print(e)
        return json.dumps({"status": 0,
                           "msg": str(e),
                           }, default=str )

@game.route('/leave_room', methods=['POST'])
def leave_room():
    try:
        # affected = db.rooms.find({
        #     "player":request.form.getlist("user"),
        # }
        with client.start_session() as s:
            s.start_transaction()
            db.rooms.update({"player": {"$in": [current_user.get_id()]}},
                                     {"$pull": {"player": current_user.get_id()}})
            db.rooms.delete_many({"player": []})
            result = s.commit_transaction()
        print(result,dir(result),"\n\n\n")
        return Response(json.dumps({"status":1,
                                    }, default=str), mimetype='application/json')
    except KeyError as e:
        return Response(json.dumps({"status": 0,
                                    "msg": "KeyError",
                                    }, default=str), mimetype='application/json')

@game.route('/get_rooms', methods=['GET'])
def get_rooms():
    cur = db.rooms.find({"course":request.args["course"]})
    return Response(json.dumps(list(cur), default=str), mimetype='application/json')