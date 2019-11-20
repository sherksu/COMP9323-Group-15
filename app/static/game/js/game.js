let timer;
let heart;
let aniP = new Promise(((resolve, reject) => {resolve()}));
// var tmp
$( document ).ready(function() {
    $(".question").on('animationend', function(e) {
        // console.log("animationed",e.currentTarget.nextElementSibling == null,e)
        $(e.currentTarget).css("display","none");
        if (e.currentTarget.nextElementSibling == null){
            timer.stop();
            // heart.set(0)
            feedback()
        }else{
            $(e.currentTarget.nextElementSibling).fadeIn()
        }
        cur_answer()
    });

    timer = $('.timer').FlipClock(100, {
        clockFace: 'MinuteCounter',
        countdown: true,
        callbacks: {
            stop: function () {
                if(timer.getTime()==0){
                    alert("timeout");
                    // heart.set(0)
                    feedback()
                }
            }
        }
    });

    $(".option").on("click",function (e) {
        console.log("option click", e);
        e.stopImmediatePropagation();
        $(e.currentTarget).parentsUntil(".question").find("input").prop("checked",false);
        $(e.currentTarget).find("input").prop("checked", true);
    });

    heart = new ldBar($(".heart")[0]);

    window.Moster = function(){
        return false
    };

    console.log("js loaded");

    // feedback ---------------------
    $("#accordion").on('click', 'button', function(){
        window.open('/solutions/'+$(this).attr("value"));
    });

    $("#result_close").click(function(){
       open("", '_self').close()
    });

    $("#shows").click(() => {
        alert(JSON.stringify(question_list));
    });

    $("#error_save").click(() => {
        $.post("/game/error_save", JSON.stringify(question_list), (res) => {
            alert(res);
        })
    })
    // ---------------------------------

    cur_answer()
});

function cur_answer(){
    console.log(x[$(".question:visible input").prop("name")])
}

function nextQ(e) {
    if ($(".question:visible input").serializeArray().length == 0){
        alert("Please choose yout answer! ");
        return false
    }
    let chose = $(".question:visible input").serializeArray()[0];
    $(".question:visible").addClass('animated bounceOutLeft')
    if(x[chose.name] == chose.value){
        aniP = aniP.then(()=>{
            return new Promise(correct);
        })
        qnum = $('.all-questions').attr("q-num");
        heart.set(heart.value - (1/qnum*100))
    }else{
        $(".monster:visible").m_restart()
    }
}

// function updateHeart(){
//     qnum = $('.all-questions').attr("q-num")
//     curr = $('.question:visible').attr("q-id")
//     heart.set((1-(curr-1)/qnum)*100)
// }

function test_aniP(){
    aniP = aniP.then(()=>{
            return new Promise(correct);
        })
}

function feedback(){
    console.log('final!');
    // feed_back ------------
    feedback_build(getAnswers());
    user_data_refresh();
    $("#result").fadeIn();
    // ----------------------
}

function getAnswers(){
    return $(".all-questions input").serializeArray()
}

jQuery.fn.m_restart = function () {
    if(this.css("display")){
        this.show()
    }
    let imgSrc = this.prop("src");
    this.prop("src", imgSrc);
    return this
};

function correct(resolve){
    $("#avatar1").hide();
    $("#avatar2").m_restart();
    let alive,die,next
    alive = "#"+$(".monster:visible")[0].id
    die= alive.substring(0,3)+"_1"
    if (alive.substring(0, 3) == "#m1") {
        next="#m2"
    } else {
        next="#m1"
    }
    $(alive).m_restart();
    setTimeout(function () {
        $(alive).hide();
        $(die).m_restart();
        setTimeout(function () {
            $(die).hide();
            setTimeout(function () {
                $(next).m_restart()
                resolve()
            }, 200);
        }, 2000);
    }, 2000);
}

