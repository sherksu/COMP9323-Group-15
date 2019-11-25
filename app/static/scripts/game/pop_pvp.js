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

$(document).ready(function(){
    let Room = function (course,type){
        this.id = 0
        this.course = course
        this.type = type
        this.player = []
        this.game_start = false
    }

    Room.from = function (obj) {
        let r = new Room()
        r .id = obj._id
        r .course = obj.course
        r .type = obj.type
        r .player = obj.player
        r .game_start = typeof obj.game_start !== "undefined"
        return r
    }

    Room.prototype.init = function (username="",join_handler) {
        let tpl, time, tid, outterID
        time = new Date().getTime()
        tid = "#player-"+this.id
        outterID = "#room-" + this.id
        tpl = "<div class=\"panel-group\" id=\""+outterID.substring(1)+"\">\n" +
            "                    <div class=\"panel panel-primary default-room\">\n" +
            "                        <div class=\"panel-heading\">\n"+
            "                           <a class='redirect pull-right'> <button class='btn btn-warning  join-room' style='margin-top: -8px;'>Join this room</button></a>"
        tpl +="                          <h4 class=\"panel-title\">\n" +
            "                                <a class=\"room_header\" data-toggle=\"collapse\" data-parent=\""+outterID+"\" href=\""+tid+"\">\n" +
            "                                    " + this.course + " —— <span class=\"room-mode\">"+this.type+"</span></a>\n" +
            "                            </h4>\n" +
            "                        </div>\n" +
            "                        <div id=\""+tid.substring(1)+"\" class=\"panel-collapse collapse in\">\n" +
            "                            <div class=\"panel-body\">\n"
        tpl += this.players(username)
        tpl += "                                   </a>"+
            "                                </div>\n" +
            "                            </div>\n" +
            "                        </div>\n" +
            "                    </div>\n" +
            "                </div>"
        this.e = $(tpl)
        let cb_val = this.id
        this.e.on("click",".join-room", function (e) {
            join_handler(cb_val,e)
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
    Room.prototype.players = function (username) {
        let tpl = ""
        this.player.forEach(function (item) {
            if (item == username) {
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
        // if(!this.player.includes(username) && !this.e.find(".join-room").length)
        //     this.e.find(".panel-heading").prepend("<button class='btn btn-warning pull-right join-room' style='margin-top: -8px;'>Join this room</button>")
        // else if (this.player.includes(username) && this.e.find(".join-room").length)
        //     this.e.find(".join-room").remove()
        //TODO -- 暂时先存在这里
        let type_num = {
            "1 vs 1": 2,
            "2 vs 2": 4,
            "Battlegrounds": 3,
            "fake type":1000
        }
        if (this.game_start && this.player.includes(username)){
            this.e.find(".join-room").removeClass("btn-warning").addClass("btn-success")
            this.e.find(".join-room").prop("disabled", false).attr("disabled", false).text("Game Started")
            this.e.find(".redirect").prop("href", "/game/pvp/" + this.course)
        }else if(this.player.includes(username) && !this.game_start ){
            this.e.find(".join-room").removeClass("btn-warning").addClass("btn-success")
            this.e.find(".join-room").prop("disabled", "disabled").attr("disabled", "disabled").text("Current Room")
        } else if(this.player.length >= type_num[this.type] || this.game_start) {
            this.e.find(".join-room").removeClass("btn-success").addClass("btn-warning")
            this.e.find(".join-room").prop("disabled", "disabled").attr("disabled", "disabled").text("Full Room")
        }else {
            this.e.find(".join-room").removeClass("btn-success").addClass("btn-warning")
            this.e.find(".join-room").prop("disabled", false).attr("disabled", false).text("Join this room")
        }
    }
    Room.prototype.update = function (username) {
        this.e.find(".panel-collapse.collapse.in").html(this.players(username))
        this.join_btn()
    }


    Rooms = function (container, user, course,new_handler,join_handler,leave_handler) {
        this.user = user
        this.container = container
        this.course = course
        this.rooms = {}
        this.new_handler = new_handler
        this.join_handler = join_handler
        this.leave_handler = leave_handler
    };
    Rooms.prototype.new_room = function (...args) {
        let r = this.create_room(...args)
        r.player.push(this.user)
        this.new_handler(r.data())
    }
    Rooms.prototype.join_room = function (type) {

    }
    Rooms.prototype.create_room = function (type) {
        return new Room(this.course, type)
    }
    Rooms.prototype.push_room = function (room,focus) {
        if (!(room instanceof Room))
            room = Room.from(room).init(this.user,this.join_handler)
        this.rooms[room.id] = room
        this.container.prepend(room.e)
        if (focus)
            room.e[0].scrollIntoView( {behavior: "smooth" })
    }
    Rooms.prototype.update_from = function (data, is_player_callback = null) {
        let _difference = new Set(this.rooms ? Object.keys(this.rooms) : [])
        // console.log("_difference",_difference)
        let is_player = 0
        let game_start = 0
        rs = this
        data.forEach(function (item) {
            if (item && item.hasOwnProperty("_id")) {
                if (rs.rooms.hasOwnProperty(item._id)) {
                    if (!equal(item.player, rs.rooms[item._id].player)) {
                        // console.log("\n",this.rooms[item._id].player)
                        // console.log(item.player,"\n")
                        rs.rooms[item._id].player = item.player
                        rs.rooms[item._id].update(rs.user)
                    }else if(rs.rooms[item._id].game_start != (typeof item.game_start !== "undefined")){
                        rs.rooms[item._id].game_start = true
                        rs.rooms[item._id].update(rs.user)
                    }
                } else {
                    let r = Room.from(item).init(rs.user,rs.join_handler)
                    rs.push_room(r)
                }
                if (!is_player) {
                    is_player = item.player.includes(rs.user)
                }
                if (!game_start) {
                    game_start = item.player.includes(rs.user)&&typeof item.game_start !== "undefined"
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
        if(game_start){
            rs.container.find(".join-room:contains('Join this room')").prop("disabled","disabled").attr("disabled","disabled")
        }
        // else{
        //     this.container.find(".join-room").prop("disabled",false)
        // }
        if (is_player_callback)
            is_player_callback(is_player,game_start)
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
    Rooms.prototype.leave_room = function(){
        this.leave_handler()
    }
    Rooms.prototype.updatebtn = function(){
        this.leave_handler()
    }


    $.fn.Rooms = function (...args) {
        return new Rooms($(this),...args);
    }
})

////////////////////////////////////////////////

let socket
let rooms
$(document).ready(function () {
    rooms = $("#pvp_Modal .modal-body").Rooms(username, c_code,new_socket,join_socket,leave_socket)
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
        rooms.leave_room()
        socket.disconnect()
    })

    $("#pvp_Modal .btn-group a").on("click", function (e) {
        $("#room_span").text(e.target.innerText)
    })
    //for development
    // $("nav").hide()
});

function new_room(e){
    in_room(1)
    rooms.new_room($("#room_span").text())
}

function in_room(is,game_start=0) {
    if(!game_start){
        $(".create_room").prop("disabled",false)
        $(".room_type").prop("disabled",false)
        $(".leave_room").addClass("btn-danger").removeClass("btn-default").prop("disabled",false)
    }
    if(is){
        $(".create_room").prop("disabled","disabled")
        $(".room_type").prop("disabled","disabled")
        $(".leave_room").addClass("btn-danger").removeClass("btn-default").prop("disabled",false)
    }else{
        $(".create_room").prop("disabled",false)
        $(".room_type").prop("disabled",false)
        $(".leave_room").addClass("btn-default").removeClass("btn-danger").prop("disabled","disabled")
    }
    // console.log("in_room",game_start)
    if(game_start){
        $(".create_room").prop("disabled","disabled")
        $(".room_type").prop("disabled","disabled")
        $(".leave_room").addClass("btn-default").removeClass("btn-danger").prop("disabled","disabled")
    }
}

function join_socket(id,e){
    socket.emit("change_room",id)
}
function leave_socket(){
    socket.emit("leave_room")
}
function new_socket(data){
    socket.emit("new_room", data, function (data) {
        console.log("new_room callback", data)
    })
}

let showed = false
let updateroomlog =0
let gaminglog = 0
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
        if(updateroomlog){
            console.debug("on update_room", JSON.parse(data))
        }
        rooms.update_from(JSON.parse(data), in_room)
    });

    socket.on('gaming', function (data) {
        data = JSON.parse(data)
        if(gaminglog){
            console.log("gaming",JSON.parse((data)))
        }
        let modal = "<div class=\"modal fade message-pop\" tabindex=\"-1\" role=\"dialog\">\n" +
            "  <div class=\"modal-dialog\" role=\"document\">\n" +
            "    <div class=\"modal-content\">\n" +
            "      <div class=\"modal-header\">\n" +
            "        <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button>\n" +
            "        <h4 class=\"modal-title\">Message</h4>\n" +
            "      </div>\n" +
            "      <div class=\"modal-body\">\n" +
            "        <p>&hellip;</p>\n" +
            "      </div>\n" +
            "      <div class=\"modal-footer\">\n" +
            "        <button type=\"button\" class=\"btn btn-default pull-left\" data-dismiss=\"modal\"> No </button>\n" +
            "        <a type=\"button\" class=\"btn btn-success pull-right yes-btn\" href=''> Yes </a>\n" +
            "      </div>\n" +
            "    </div><!-- /.modal-content -->\n" +
            "  </div><!-- /.modal-dialog -->\n" +
            "</div><!-- /.modal -->"
        if (!$(".message-pop").length)
            $("body").append(modal)
        if ($("#pvp_Modal:visible").length && !showed) {
            console.log("in")
            $(".message-pop").modal()
            $(".message-pop").find(".modal-body").html("<h2>Redirect you to the game page</h2>")
            tmp = data
            $(".message-pop").find("a.yes-btn").prop("href", "/game/pvp/" + data["data"]["course"])
            $("message-pop").show()
            $("#pvp_Modal .join-room:contains('Game Started')").parent(".redirect").prop("href", "/game/pvp/" + data["data"]["course"])
            showed = true
        }
    })
    socket.on('start_game', function (data) {
        console.debug("on start_game", data)

    });
}
