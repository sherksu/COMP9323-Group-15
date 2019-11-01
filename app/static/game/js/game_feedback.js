let question_list = [];
let correct_rate = 0;
let gain;

function feedback_build(result) {
    for (let res in result) {
        let data = {};
        let ob = result[res];
        data.question = ob.name;
        data.answer = ob.value;
        let correct = (x[data.question] == data.answer)? true : false;
        let qh = '#'+data.question+'head';
        if(correct){
            correct_rate += 1;
            refresh_level(1);
            $(qh).append("<span class='glyphicon glyphicon-ok' style='color:greenyellow; float:right'></span>");
        }else{
            refresh_level(0.2);
            $(qh).append("<span class='glyphicon glyphicon-remove' style='color:darkred; float:right'></span>");
            question_list.push(data);
        }
    }
}

function refresh_level(rate){
    level_info.exp += rate*10;
    if (level_info.exp > level_info.next_level) {
        alert('level up!!');
        gain = level_info.exp - exp;
        level_info.exp -= level_info.next_level;
        level_info.next_level += level_info.level * 10;
        level_info.level += 1;
    }
}

function user_data_refresh() {
    $("#level").text(level_info.level);
    $("#exp").text(level_info.exp);
    $("#gain_exp").text(gain);
    $("#next_level").text(level_info.next_level);
    $("#correct_rate").text(parseFloat(correct_rate*10)+'%');
    $.post("/game/level_save", JSON.stringify(level_info), (x) => {
        console.log('level save ' + x)
    });
}