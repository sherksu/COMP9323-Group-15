$('document').ready(function() {
    let join = io.connect(window.location.origin+"/chat?course="+(c_code?c_code:"''"));

    join.on('chat_message', function(input) {
        console.log(input);
        $('.user_list').append("        <div id=\"user_ids\" class=\"tiny_HUD\">\n" +
            "            <div class=\"tiny_avatar\">\n" +
            "                <img src=\"" + input['avatar'] + "\" alt=\"\" height=\"100%\" width=\"100%\">\n" +
            "            </div>\n" +
            "            <div class=\"tiny_heading\">\n" +
            "                <p style=\"font-size:12pt; margin:0\">"+ input['name'] +"</p><p style=\"font-size:10pt; margin:0\">lv. "+ input['level'] +"</p>\n" +
            "            </div>\n" +
            "        </div>");
    });

   document.onkeydown = function() {
       if (event.keyCode === 13) {
           let chat = $('.chat-input');
           $('#chats').fadeIn();
           if ( chat.val() ) {
               join.emit('broadcast_chat', chat.val(), () => {
                   //call back
               }); // emit to socket
               chat.val(""); // clear up textfield
           } else {
               chat.focus();
           }
       } else if (event.keyCode === 27) {
           $('#chats').fadeOut();
       }
   };



   $('#beginner').on('click', () => {
        $('#beginner_content').fadeIn();
        $('#expert_content').css('display', 'none');
    });

    $('#expert').on('click', () => {
        $('#beginner_content').css('display', 'none');
        $('#expert_content').fadeIn();
    });
});