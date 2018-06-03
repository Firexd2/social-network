$(document).ready(function () {
    $('textarea[name=message]').on('focusin', function () {
        $('#button-wall').show()
    });
    $(document).mouseup(function (e) {
        const wall = $(".wall");
        const input = $('input[name=status]');

        if (e.target!==wall[0] && !wall.has(e.target).length){
            $('#button-wall').hide();
        }
        if (e.target!==input[0] && !input.has(e.target).length && input.is(':visible')){
            $('form[name=status]').submit()
        }
    });

    $('.status').on('click', function () {
        $(this).hide();
        $('input[name=status]').show().focus()
    });

    $('form[name=new-message]').on('submit', function (e) {
        e.preventDefault();
        const to_redirect = '/rooms/';
        const data = $(this).serializeArray();
        $.post('/send_message/', data, function () {
            location.href=to_redirect
        })
    });

});
