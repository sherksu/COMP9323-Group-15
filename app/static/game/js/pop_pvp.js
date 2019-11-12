// var Rooms

function equal(setA, setB) {
    setA = new Set(setA);
    setB = new Set(setB);
    if (setA.size != setB.size)
        return 0
    for (var elem of setB) {
        setA.delete(elem);
    }
    return !setA.size ;
}

(function($){
    let Room = function (course,type){
        this.id = 0
        this.course = course
        this.type = type
        this.player = []
    }

    Room.from = function (obj) {
        let r = new Room()
        r .id = obj._id
        r .course = obj.course
        r .type = obj.type
        r .player = obj.player
        return r
    }

    Room.prototype.init = function (user_name="",join_handler) {
        let tpl, time, tid, outterID
        time = new Date().getTime()
        tid = "#player-"+this.id
        outterID = "#room-" + this.id
        tpl = "<div class=\"panel-group\" id=\""+outterID.substring(1)+"\">\n" +
            "                    <div class=\"panel panel-primary default-room\">\n" +
            "                        <div class=\"panel-heading\">\n"
        tpl +="                          <h4 class=\"panel-title\">\n" +
            "                                <a class=\"room_header\" data-toggle=\"collapse\" data-parent=\""+outterID+"\" href=\""+tid+"\">\n" +
            "                                    " + this.course + " —— <span class=\"room-mode\">"+this.type+"</span></a>\n" +
            "                            </h4>\n" +
            "                        </div>\n" +
            "                        <div id=\""+tid.substring(1)+"\" class=\"panel-collapse collapse in\">\n" +
            "                            <div class=\"panel-body\">\n"
        tpl += this.players(user_name)
        tpl += "                                   </a>"+
            "                                </div>\n" +
            "                            </div>\n" +
            "                        </div>\n" +
            "                    </div>\n" +
            "                </div>"
        this.e = $(tpl)
        let cb_val = this.id
        this.e.on("click",".join-room", function (e,) {
            join_handler(cb_val)
        })
        this.join_btn()
        return this
    }
    Room.prototype.data = function () {
        return {
            "outterID":this.id,
            "course":this.course,
            "type":this.type,
            "player":this.player
        }
    }
    Room.prototype.players = function (user_name) {
        let tpl = ""
        this.player.forEach(function (item) {
            if (item == user_name) {
                tpl += "<a href=\"#\" class=\"list-group-item list-group-item-action list-group-item-info\">" +
                    item +
                    "</a>"
            } else {
                tpl += "<a href=\"#\" class=\"list-group-item list-group-item-action\">" +
                    item +
                    "</a>"
            }
        })
        return tpl
    }
    Room.prototype.join_btn = function(){
        if(!this.player.includes(user_name) && !this.e.find(".join-room").length)
            this.e.find(".panel-heading").prepend("<button class='btn btn-warning pull-right join-room' style='margin-top: -8px;'>Join this room</button>")
        else if (this.player.includes(user_name) && this.e.find(".join-room").length)
            this.e.find(".join-room").remove()
        //TODO -- 暂时先存在这里
        let type_num = {
            "1 vs 1": 2,
            "2 vs 2": 4,
            "Battlegrounds": 10,
            "fake type":1000
        }
        if(this.player.length >= type_num[this.type]){
            this.e.find(".join-room").prop("disabled","disabled").text("Full Room")
        }else{
            this.e.find(".join-room").prop("disabled",false).text("Join this room")
        }
    }
    Room.prototype.update = function (user_name) {
        this.e.find(".panel-collapse.collapse.in").html(this.players(user_name))
        this.join_btn()
        this.full_check()
    }


    Rooms = function (container, user, course,join_cb) {
        this.user = user
        this.container = container
        this.course = course
        this.rooms = {}
        this.join_cb = join_cb
    };
    Rooms.prototype.new_room = function (...args) {
        let r = this.create_room(...args)
        r.player.push(this.user)
        socket.emit("new_room",r.data(),function (data) {
            console.log("new_room callback",data)
        })
    }
    Rooms.prototype.join_room = function (type) {
        //TODO -- join in database
    }
    Rooms.prototype.create_room = function (type) {
        return new Room(this.course, type)
    }
    Rooms.prototype.push_room = function (room,focus) {
        if (!(room instanceof Room))
            room = Room.from(room).init(this.user,join_cb)
        this.rooms[room.id] = room
        this.container.prepend(room.e)
        if (focus)
            room.e[0].scrollIntoView( {behavior: "smooth" })
    }
    Rooms.prototype.update_from = function (data, is_player_callback = null) {
        let _difference = new Set(this.rooms ? Object.keys(this.rooms) : [])
        // console.log("_difference",_difference)
        let is_player = 0
        rs = this
        data.forEach(function (item) {
            if (item && item.hasOwnProperty("_id")) {
                if (rs.rooms.hasOwnProperty(item._id)) {
                    if (!equal(item.player, rs.rooms[item._id].player)) {
                        // console.log("\n",this.rooms[item._id].player)
                        // console.log(item.player,"\n")
                        rs.rooms[item._id].player = item.player
                        rs.rooms[item._id].update(rs.user)
                    }
                } else {
                    let r = Room.from(item).init(rs.user,join_cb)
                    rs.push_room(r)
                }
                if (!is_player) {
                    is_player = item.player.includes(rs.user)
                }
                _difference.delete(item._id);
                // console.log("_difference",_difference)
            }
        })
        // console.log("final _difference",_difference)
        for (let i of _difference) {
            rs.pop_room(i)
        }
        // console.log("rooms update is player",is_player)
        // console.log("is_player_callback",is_player_callback)
        if (is_player_callback)
            is_player_callback(is_player)
    }
    Rooms.prototype.update = function (is_player_callback=null) {
        let rs = this
        $.ajax({
            url: window.location.origin + "/game/get_rooms",
            method: "GET",
            data:{"course":rs.course},
            datatype: "JSON",
            success: function (data) {
                console.log("success", data, typeof data)
                rs.update_from(data,is_player_callback)
            }
        })
    }
    Rooms.prototype.pop_room = function(id){
        if(this.rooms.hasOwnProperty(id)){
            tmp =this.rooms[id]
            this.rooms[id].e.remove()
            delete this.rooms[id]
        }
    }
    Rooms.prototype.leave_room = function(is_player_callback){
        rs = this
        $.ajax({
            url: window.location.origin + "/game/leave_room",
            method: "POST",
            datatype: "JSON",
            success: function (data) {
                console.log("success", data, typeof data)
                rs.update(is_player_callback)
            }
        })
    }

    $.fn.Rooms = function (user, course) {
        return new Rooms($(this), user, course);
    }
}(jQuery))

////////////////////////////////////////////////

let socket
let rooms
$(document).ready(function () {
    rooms = $("#pvp_Modal .modal-body").Rooms(user_name, c_code,join_cb)
    socket = io.connect(window.location.origin+"/pvp?course="+(c_code?c_code:"''")).disconnect()
    bind_event()
    $("#pvp_Modal").on("show.bs.modal", function (e) {
        console.log("show.bs.modal")
        if (typeof socket !== "undefined") {
            if (!socket.connected)
                // socket.connect(window.location.origin+"/pvp?course="+(c_code?c_code:"''"))
                socket.connect()
        } else {
            socket = io.connect(window.location.origin+"/pvp?course="+(c_code?c_code:"''"))
            bind_event()
        }
        rooms.update(in_room)
    })

    $("#pvp_Modal").on("hide.bs.modal", function (e) {
        console.log("hide.bs.modal")
        socket.emit('disconnect');
        rooms.leave_room(in_room)
        socket.disconnect()
    })

    $("#pvp_Modal .btn-group a").on("click", function (e) {
        $("#room_span").text(e.target.innerText)
    })
});

function new_room(e){
    in_room(1)
    rooms.new_room($("#room_span").text())
}

function in_room(is) {
    if(is){
        $(".create_room").prop("disabled","disabled")
        $(".room_type").prop("disabled","disabled")
        $(".leave_room").addClass("btn-danger").removeClass("btn-default").prop("disabled",false)
    }else{
        $(".create_room").prop("disabled",false)
        $(".room_type").prop("disabled",false)
        $(".leave_room").addClass("btn-default").removeClass("btn-danger").prop("disabled","disabled")
    }

}

function join_cb(id){
    socket.emit("change_room",id)
}

function bind_event(){
    socket.on('connect', function () {
        console.log("connect\n\n\n\n")
        socket.emit("join",{"room":c_code},function (data) {
            console.log("join",data)
        })
    });
    socket.on('disconnect', function (data) {
        console.log("disconnect", data)
    });
    socket.on('message', function (data) {
        console.log("message", data)
    });
    socket.on('echo', function (data) {
        console.log("echo", data)
    });
    socket.on('new_room', function (data) {
        console.log("on new_room", data)
        // rooms.push_room(data, 1)
    });
    socket.on('update_room', function (data) {
        console.debug("on update_room", data)
        rooms.update_from(JSON.parse(data), in_room)
    });
}