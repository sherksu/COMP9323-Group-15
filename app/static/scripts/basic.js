$(document).ready(() => {
    $('#rank_btn').on('click', () => {
        $('#error_page').fadeOut();
        $('#detail_page').fadeOut();
        $('#rank_page').fadeToggle();
    });

    $('#profile_btn').on('click', () => {
        $('#error_page').fadeOut();
        $('#rank_page').fadeOut();
        $('#detail_page').fadeToggle();
    });

    $('#error_btn').on('click', () => {
        $('#detail_page').fadeOut();
        $('#rank_page').fadeOut();
        $('#error_page').fadeToggle();
    });

    $('.hover_mask').on('click', function() {
        console.log('1');
        $(this).parent().fadeToggle();
    })
});