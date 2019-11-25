$('document').ready(function() {
   document.onkeydown = function() {
       if (event.keyCode === 13) {
           let chat = $('.chat-input');
           $('#chats').fadeIn();
           if ( chat.val() ) {
               console.log(chat.val()); // emit to socket
               chat.val(""); // clear up textfield
           } else {
               chat.focus();
           }
       } else if (event.keyCode === 27) {
           $('#chats').fadeOut();
       }
   };

   $('.single_btn').on('click', () => {
       $('#single_content').fadeIn();
       $('#multiple_content').css('display', 'none');
   });

   $('.multiple_btn').on('click', () => {
       $('#multiple_content').fadeIn();
       $('#single_content').css('display', 'none');
   });

   $('#beginner').on('click', () => {
        $('#beginner_content').fadeIn();
        $('#expert_content').css('display', 'none');
    });

    $('#expert').on('click', () => {
        $('#beginner_content').css('display', 'none');
        $('#expert_content').fadeIn();
    });
});