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
    });

    let arrayIdsFriend = [];
    $('.friend').on('click', function () {
        const id = $(this).attr('id');
        const name = $(this).find('.name').text();
        if ($.inArray(id, arrayIdsFriend) === -1) {
            $('.selected-friends').append('<div class="selected" id="' + id + '" >' + name + ' <i class="fas fa-times"></i></div>');
            arrayIdsFriend.push(id);
            info_create_room()
        }
    });

    Array.prototype.remove = function(el) {
        return this.splice(this.indexOf(el), 1);
    };

    $('body').on('click', '.fa-times', function () {
        const elem = $(this).parent();

        arrayIdsFriend.remove(elem.attr('id'));
        elem.remove();
        info_create_room()

    });

    function info_create_room() {

        const count_span = $('.count-friend');
        const type_btn = $('.type-room');
        const btn = $('button');

        const count_friend = $('.selected').length;

        if (count_friend) {
            count_span.text(count_friend);
            if (count_friend < 2) {
                btn.css({'display': 'inline-block'}).attr('data-target', '.new-message');
                type_btn.text('Написать сообщение')
            } else {
                btn.css({'display': 'inline-block'}).attr('data-target', '.create-room');
                type_btn.text('Создать беседу')
            }
        } else {
            btn.css({'display': 'none'});
            count_span.text(0)
        }
    }

    $('input[name=search-friend]').on('input', function () {
        const val = $(this).val().toLowerCase();
        const friends = $('.friend');
        if (val) {
            friends.hide();
            for (let i=0;i<friends.length;i++) {
                const name = friends.eq(i).find('.name').text().toLowerCase();
                if (name.indexOf(val) !== -1) {
                    friends.eq(i).show()
                }
            }
        } else {
            friends.show()
        }
    });

    $('form[name="new-message"]').on('submit', function (e) {
        e.preventDefault();

        const to_redirect = '/rooms/';

        let data = $(this).serializeArray();
        data[1].value = $('.selected').attr('id');
        $.post(to_redirect, data, function () {
            location.href=to_redirect
        })
    })

});
