let timer;
let heart;
let type= "{{type}}";
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
    timer.stop();
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
    if(x[chose.name] == chose.value){
        correct();
        qnum = $('.all-questions').attr("q-num");
        heart.set(heart.value - (1/qnum*100))
    }else{
        $("#m1").m_restart()
    }
    $(".question:visible").addClass('animated zoomOutLeft')
}

// function updateHeart(){
//     qnum = $('.all-questions').attr("q-num")
//     curr = $('.question:visible').attr("q-id")
//     heart.set((1-(curr-1)/qnum)*100)
// }

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

function m_switch(num1,num2){
    $("[id*='m"+num1+"']").hide();
    $("#m"+num2).show();
}

function m_die(num1,num2){
    $("[id*='m']").hide();
    $("#m"+num2).hide();
}

function correct(){
    $("#avatar1").hide();
    $("#avatar2").m_restart();
    $("#m1").m_restart();
    setTimeout(function () {
        $("#m1").hide();
        $("#m1_1").m_restart();
        setTimeout(function () {
            $("#m1_1").hide();

            setTimeout(function () {
                $("#m1").m_restart()
            }, 200);
        }, 2000);
    }, 2000);
}

