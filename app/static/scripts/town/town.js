$('document').ready(function() {
   document.onkeydown = function() {
       if (event.keyCode === 13) {
           let chat = $('.chat-input');
           console.log(chat.val()); // emit to socket
           chat.val("");  // clear textfield
           chat.fadeToggle();
       }
   }
});