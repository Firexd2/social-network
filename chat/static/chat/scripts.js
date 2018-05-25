if (document.querySelector(".chat-log")) {document.querySelector(".chat-log").scrollTop = document.querySelector(".chat-log").scrollHeight;}

$(document).ready(function () {

    $(function () {
        $('textarea[name=action-new-message]').keypress(function (e) {
            if (e.which === 13) {
                //submit form via ajax, this is not JS but server side scripting so not showing here
                // $("#chatbox").append($(this).val() + "<br/>");
                // $(this).val("");
                e.preventDefault();
                $('form[name=new-message]').submit();
            }
        });


    });

    $(function () {
        $('.chat').animate({height: $(window).height() - 300}, 100)
    })
    
});
