(function ($) {
    let Colors = ["darkkhaki", "darkmagenta", "darkolivegreen", "darkorange", "darkorchid", "darkred", "darksalmon", "darkviolet",
        "fuchsia", "gold", "green", "indigo", "khaki", "lightblue", "lightcyan", "lightgreen", "lightgrey", "lightpink",
        "lightyellow", "lime", "magenta", "maroon", "navy", "olive", "orange", "pink", "purple", "violet", "red",
        "silver", "white", "yellow"]
    let ScrollNav = function (contents, target = $("body")) {
        this.contents = contents
        this.target = target
        this.init()
        this.player_added = 0
        let sn=this
        $(window).scroll(function (e) {
            sn.scrollHandler(sn)
        })
    }

    ScrollNav.prototype = {
        init: function () {
            let tpl = "    <nav class=\"navbar navbar-expand-sm navbar-light \" id='ScrollNav'>\n" +
                "                <a class=\"navbar-brand\" href=\""+window.location.origin+"/\" target='_self'><i class=\"fas fa-home\"></i>Home</a>\n" +
                "                <button class=\"navbar-toggler\" type=\"button\" data-toggle=\"collapse\" data-target=\"#navbarNavAltMarkup\"\n" +
                "                        aria-controls=\"navbarNavAltMarkup\" aria-expanded=\"false\" aria-label=\"Toggle navigation\">\n" +
                "                    <span class=\"navbar-toggler-icon\"></span>\n" +
                "                </button>\n" +
                "                <div class=\"collapse navbar-collapse\" id=\"navbarNavAltMarkup\">\n" +
                "                    <div class=\"navbar-nav\">\n"
            this.contents.each(function (k,item) {
                // console.log("item",typeof item)
                // tmp = item
                tpl +="                  <a class=\"nav-item nav-link\" href='#"+item.getAttribute("id")+
                    "' >"+item.getAttribute("data-label")+" </a>\n"
            })
            tpl += "                 </div>\n" +
                "                </div>\n" +
                "            </nav>"
            this.e = $(tpl)
            this.target.append(this.e)
        },
        scrollHandler:function(sn){
            console.log("scroll")
            let inViewPort = 0
            sn.e.find(".nav-link").removeClass("active")
            sn.contents.each(function (k, item) {

                let domRect = item.getBoundingClientRect()
                if ((domRect.top < 0 && domRect.bottom >= 50)
                    || (domRect.top >= 0 && domRect.top < (window.innerHeight - 50))) {
                    item = $(item)
                    let ele = sn.e.find(".nav-link[href='#" + item.prop("id") + "']")
                    // tmp = ".nav-link[href='#" + item.prop("id") + "']"
                    if (!inViewPort)
                        inViewPort = ele
                    ele.addClass("active")
                    // console.log("in",ele,item,".nav-link[href='#" + item.prop("id") + "']")
                    return true
                } else {
                    if (inViewPort.length) {
                        if (window.innerWidth > 768) {
                            $(window).off("scroll")
                            inViewPort[0].scrollIntoView({behavior: "auto", block: "center"})
                            $(window).scroll(function (e) {
                                sn.scrollHandler(sn)
                            })
                        }else{
                            $(window).off("scroll")
                            inViewPort[0].scrollIntoView({behavior: "auto",inline:"center"})
                            $(window).scroll(function (e) {
                                sn.scrollHandler(sn)
                            })
                        }
                        return false;
                    } else {
                        return true;
                    }
                }
            })
        },
        addPlayer:function(players){
            sp = ""
            for(let n=0; n <players.length;n++){
                if(players[n]==username)
                    continue
                sp +="<span class='invisible play-span "+players[n]+"' style='border: 5px solid "+Colors[n]+"'></span>"
            }
            sp = $(sp)
            this.e.find(".nav-item.nav-link").each(function (index,element) {
                aSP = sp.clone()
                aSP.addClass("question"+(index+1))
                $(element).prepend(aSP)
            })
            this.player_added = 1
        },
        showPlayers:function (players,data) {
            if(!this.player_added){
                return 0
            }
            players.forEach(function (player) {
                if((player!=username)&&data.hasOwnProperty(player)){
                    $("."+player).addClass("invisible")
                    data[player].forEach(function (focus_q) {
                        $("."+focus_q.trim()+"."+player).removeClass("invisible")
                    })
                }

            })
        },
        showPlayer:function (player) {
            if ((player["user"] != username) && player.hasOwnProperty("focus")) {
                $("." + player["user"].trim()).addClass("invisible")
                player["focus"].forEach(function (focus_q) {
                    $("." + focus_q.trim() + "." + player["user"].trim()).removeClass("invisible")
                })
            }
        }
    }

    $.fn.ScrollNav = function (...args) {
        return new ScrollNav($(this), ...args)
    }
}(jQuery))
/////////////////////////////////////////
let tmp
let pvpNavBar
let socket
let update_interval_id
let sid
$(document).ready(function () {
    socket = io.connect(window.location.origin+"/pvp")
    bind_event()
    pvpNavBar = $(".question-block").ScrollNav($(".side-wrapper"))
    // console.log("pvp_game.js", pvpNavBar)

    $(".question-block .download-btn").click(function (e) {
        console.log(this)
        window.open(this.getAttribute("data-file"))
        return false
    })
    $(window).trigger("scroll")

    $(".submit-answer").click(function () {
        let answer_array = $(this).closest('.question').find("input").serializeArray()
        if (answer_array.length) {
            answer_array[0]["username"] = username
            answer_array[0]["room"] = room_id['_id']
            answer_array[0]["sid"] = sid
            tmp = answer_array
            disable_question(answer_array[0]["name"],"",1)
            $.ajax({
                url: window.location.origin + "/game/upload_answer",
                method: "POST",
                data: answer_array[0],
                success: function (data) {
                    console.log("submit-answer callback", data)
                }
            })
        } else {
            alert("Please choose an answer before commit")
        }

    })

})

function file_change(e){
    console.log('onchange');
    $(e).parent('form').find(".room").val(room_id["_id"])
    $(e).parent('form').find(".username").val(username)
    $(e).parent('form')[0].submit();
    $(e).parent('form').find(".game_submit").prop("disabled","disabled").attr("disabled","disabled")
    return false;
}

function onload_fn(e) {
    tmp = e
    response = $(e.contentWindow.document).find("body").text()?$(e.contentWindow.document).find("body").text():$(e.contentDocument).find("body").text()
    $(e).parent("form").find(".answer").val(response)
    console.log(response)
}

function getAnswers(){
    return $(".question-wrapper input.answer").serializeArray()
}

function set_update_interval(room_id){
    update_interval_id = setInterval(function () {
        focus_q = []
        $("#navbarNavAltMarkup .nav-item.active").each(function () {
            focus_q.push($(this).text())
        })
        if(focuslog)
            console.debug("focus",focus_q)
        socket.emit("update_focus",{"focus":focus_q,"room":room_id})
    }, 1000);
}

function disable_question(key,name,uploading=0){
    let question = q_dict[key]
    if (uploading){
        console.log("upload lock")
        $(".opacity-block." + question.trim()).find("input").css("disabled", "disabled")
        $(".opacity-block." + question.trim()).find("button").css("disabled", "disabled")
        $(".opacity-block." + question.trim()).css("opacity", "0.3")
        $(".blocker." + question.trim()).find(".textspan").text(" This question is locked  ~~!")
        $(".blocker." + question.trim()).css("display", "block")
    }else if (q_dict.hasOwnProperty(key)) {
        tmp =".blocker." + question.trim()
        if(!$(".blocker." + question.trim()+":visible").length){
            $(".opacity-block." + question.trim()).find("input").css("disabled", "disabled")
            $(".opacity-block." + question.trim()).find("button").css("disabled", "disabled")
            $(".opacity-block." + question.trim()).css("opacity", "0.3")
            if(name == username){
                $(".blocker." + question.trim()).find(".textspan").text(" You alreay finished this question ~~!")
            }else{
                $(".blocker." + question.trim()).find(".textspan").text(name + " get ahead of you ~~!")
            }
            $(".blocker." + question.trim()).css("display", "block")
        }else{

        }
    }
}
function custom_json(json){
    let sstr = unescape(json.room)
    // console.log(sstr)
    return JSON.parse(sstr)
}
function finish_pop() {
    re  = /(?:\/[^\/]*)/gm
    course = window.location.href.match(re)
    course = course[course.length-1]
    let modal = "<div class=\"modal pvp-end-modal\" tabindex=\"-1\" role=\"dialog\">\n" +
        "  <div class=\"modal-dialog\" role=\"document\">\n" +
        "    <div class=\"modal-content\">\n" +
        "      <div class=\"modal-header\">\n" +
        "        <h5 class=\"modal-title\">Redirect</h5>\n" +
        "      </div>\n" +
        "      <div class=\"modal-body\">\n" +
        "        <p>Sorry you loss!</p>\n" +
        "      </div>\n" +
        "      <div class=\"modal-footer\">\n" +
        "        <a href='/town"+course+"'><button type=\"button\" class=\"btn btn-primary pull-right\">Leave</button>\n</a>" +
        "      </div>\n" +
        "    </div>\n" +
        "  </div>\n" +
        "</div>"
    $(modal).modal({backdrop: 'static', keyboard: false})
}

function win_pop(data) {
    re  = /(?:\/[^\/]*)/gm
    course = window.location.href.match(re)
    course = course[course.length-1]
    let modaltpl =
        "<div class=\"modal win-pop\" tabindex=\"-1\" role=\"dialog\">\n" +
        "  <div class=\"modal-dialog\" role=\"document\">\n" +
        "    <div class=\"modal-content\">\n" +
        "      <div class=\"modal-header\">\n" +
        "        <h5 class=\"modal-title\">Congratulation</h5>\n" +
        "        <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\">\n" +
        "          <span aria-hidden=\"true\">&times;</span>\n" +
        "        </button>\n" +
        "      </div>\n" +
        "      <div class=\"modal-body\">\n" +
        "        <p>You win this game!!!!</p>\n" +(data?("You have "+(data["wins"]+1)+" win now"):"")+
        "      </div>\n" +
        "      <div class=\"modal-footer\">\n" +
        "        <a href='/town"+course+"'><button type=\"button\" class=\"btn btn-primary pull-right\">Leave</button>\n</a>" +
        "      </div>\n" +
        "    </div>\n" +
        "  </div>\n" +
        "</div>" ;
    $(modaltpl).modal({backdrop: 'static', keyboard: false})
}

let gaminglog = 0
let positionlog = 0
let focuslog = 0
let room_id =0
let answerlog=0
let tmp2=0
function bind_event() {
    socket.on('connect', function () {
        console.log("connect")
        socket.emit("join", {}, function (data) {
            console.log("join", data)
        })
        sid = socket.id.substring(5)
    });
    socket.on('disconnect', function (data) {
        console.log("disconnect", data)
    });
    socket.on('win', function (data) {
        tmp = data["answer"]
        console.log("win", data)
        // tmp=data=custom_json(data)
        win_pop(data)
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
    socket.on('loss', function (data) {
        tmp2 = data["answer"]
        // tmp=data=custom_json(data)
        console.debug("on loss", data)
        finish_pop()
    });
    socket.on('gaming', function (data) {
        data =JSON.parse(data)
        if(gaminglog)
            console.debug("gaming", data)
        if(!update_interval_id){
            // console.debug("update_interval_id")
            set_update_interval(data.id,data["data"]["player"])
            pvpNavBar.addPlayer(data["data"]["player"])
            room_id = data["data"]
        }
        if(Object.keys(data["answer"]).length){
            if(answerlog){
                console.log(data)
            }
            for (var key of Object.keys(data["answer"])) {
                disable_question(key,data["answer"][key])
            }
        }
        // tmp = data
        // pvpNavBar.showPlayers(data["data"]["player"],data["data"])
    });
    socket.on("position",function(data){
        if(positionlog)
            console.log("position",data)
        pvpNavBar.showPlayer(data)
    })
}