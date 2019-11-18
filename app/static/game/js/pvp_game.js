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
                // item = $(item)
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
    pvpNavBar = $(".question").ScrollNav($(".side-wrapper"))
    console.log("pvp_game.js", pvpNavBar)
    //for development
    $(".question").each(function (k,item) {
        $(item).text(item.getAttribute("id"))
    })
})