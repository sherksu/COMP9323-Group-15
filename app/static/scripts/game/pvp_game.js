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
                // tmp = $(item)
                let domRect = item.getBoundingClientRect()
                if ((domRect.top < 0 && domRect.bottom >= 50)
                    || (domRect.top >= 0 && domRect.top < (window.innerHeight - 50))) {
                    item = $(item)
                    let ele = sn.e.find(".nav-link[href='#" + item.prop("id") + "']")
                    if (!inViewPort)
                        inViewPort = ele
                    ele.addClass("active")
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
$(document).ready(function () {
    socket = io.connect(window.location.origin+"/pvp")
    bind_event()
    pvpNavBar = $(".question-block").ScrollNav($(".side-wrapper"))
    console.log("pvp_game.js", pvpNavBar)

    $(".question-block .download-btn").click(function (e) {
        console.log(this)
        window.open(this.getAttribute("data-file"))
        return false
    })
    $(window).trigger("scroll")


})

function file_change(e){
    console.log('onchange');
    $(e).parent('form')[0].submit();
    $(e).parent('form').find(".game_submit").prop("disabled","disabled").attr("disabled","disabled")
    return false;
}

function onload_fn(e) {
    tmp = e
    response = $(e.contentWindow.document).find("body").text()?$(e.contentWindow.document).find("body").text():$(e.contentDocument).find("body").text()
    $(e).parent("form").find(".answer").val(response)
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
<<<<<<< HEAD
        // console.debug("focus",focus)
        socket.emit("update_focus",{"focus":focus_q,"room":room_id})
    }, 1000);
}

=======
        if(focuslog)
            console.debug("focus",focus_q)
        socket.emit("update_focus",{"focus":focus_q,"room":room_id})
    }, 1000);
}
let gaminglog = 0
let positionlog = 0
let focuslog = 0
>>>>>>> 1bd37a36e86039fdc5d7ac25c702cf2af83f3936
function bind_event() {
    socket.on('connect', function () {
        console.log("connect\n\n\n\n")
        socket.emit("join", {}, function (data) {
            console.log("join", data)
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
    socket.on('gaming', function (data) {
        data =JSON.parse(data)
<<<<<<< HEAD
        console.debug("gaming", data)
=======
        if(gaminglog)
            console.debug("gaming", data)
>>>>>>> 1bd37a36e86039fdc5d7ac25c702cf2af83f3936
        if(!update_interval_id){
            // console.debug("update_interval_id")
            set_update_interval(data.id,data["data"]["player"])
            pvpNavBar.addPlayer(data["data"]["player"])
        }
        // tmp = data
        // pvpNavBar.showPlayers(data["data"]["player"],data["data"])
    });
    socket.on("position",function(data){
<<<<<<< HEAD
        // console.log("position",data)
=======
        if(positionlog)
            console.log("position",data)
>>>>>>> 1bd37a36e86039fdc5d7ac25c702cf2af83f3936
        pvpNavBar.showPlayer(data)
    })
}