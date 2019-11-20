var tmp
(function ($) {
    let ScrollNav = function (contents, target = $("body")) {
        this.contents = contents
        this.target = target
        this.init()
        let sn=this
        $(window).scroll(function (e) {
            sn.scrollHandler(sn)
        })
    }

    ScrollNav.prototype = {
        init: function () {
            let tpl = "    <nav class=\"navbar navbar-expand-sm navbar-light \" id='ScrollNav'>\n" +
                "                <a class=\"navbar-brand\" href=\"#\">Navbar</a>\n" +
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
        }
    }

    $.fn.ScrollNav = function (...args) {
        return new ScrollNav($(this), ...args)
    }
}(jQuery))
/////////////////////////////////////////

let pvpNavBar
$(document).ready(function () {
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