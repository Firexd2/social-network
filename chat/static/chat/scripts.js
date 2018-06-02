function scroll_to_bottom() {if (document.querySelector(".chat-log")) {document.querySelector(".chat-log").scrollTop = document.querySelector(".chat-log").scrollHeight;}}

scroll_to_bottom();

$(document).ready(function () {

    $(function () {
        $('textarea[name=action-new-message]').keypress(function (e) {
            if (e.which === 13) {
                //submit form via ajax, this is not JS but server side scripting so not showing here
                // $("#chatbox").append($(this).val() + "<br/>");
                // $(this).val("");
                e.preventDefault();
                $('form[name=message]').submit();
                scroll_to_bottom()
            }
        });
    });

    $('form[name=message]').on('submit', function (e) {
        e.preventDefault();
        const form_data = $(this).serializeArray();
        $.post($(this).attr('action'), form_data, function (json) {

            const chat_log = $('.chat-log');


            const data = JSON.parse(json);
            const data_user_id = String(data.user_id);

            let new_message_object = '';


            const chat_item = $('.chat-item').last();
            const last_user_id = chat_item.attr('user');
            const last_datetime = chat_item.attr('time');

            const data_time = parseInt(data.time.split(':').slice(-1));
            const last_time = parseInt(last_datetime.split(':').slice(-1));


            if ((data_user_id === last_user_id) && (last_datetime.length === 5) && (data_time - last_time < 6) ) {
                new_message_object = '<div user="' + data.user_id +'" time="' + data.time + '" class="chat-item no-read">\n' +
                    '<table class="table table-sm table-item-chat">\n' +
                    '<tbody>\n' +
                    '<tr>\n' +
                    '<td width="50"></td>\n' +
                    '<td class="text">' + data.text + '</td>\n' +
                    '</tr>\n' +
                    '</tbody>\n' +
                    '</table>\n' +
                    '</div>'
            } else {

                const short_name = data.short_name;

                new_message_object = '<div user="' + data.user_id +'" time="' + data.time + '" class="chat-item no-read">\n' +
                    '<table class="table table-sm table-item-chat">\n' +
                    '<tbody>\n' +
                    '<tr class="title-message">\n' +
                    '<td width="50"><img src="' + data.user_avatar_40x40 + '" alt=""></td>\n' +
                    '<td class="info">\n' +
                    '<b class="name-item-chat">' + short_name + '</b>\n' +
                    '<br>\n' +
                    '<span class="time-messages">' + data.time + '</span>\n' +
                    '</td>\n' +
                    '</tr>\n' +
                    '<tr>\n' +
                    '<td width="50"></td>\n' +
                    '<td class="text">' + data.text + '</td>\n' +
                    '</tr>\n' +
                    '</tbody>\n' +
                    '</table>\n' +
                    '</div>'
            }
            chat_log.append(new_message_object);
            $('textarea[name=action-new-message]').val('')
        })
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

    $('form[name=new-message]').on('submit', function (e) {
        e.preventDefault();

        const to_redirect = '/rooms/';

        let data = $(this).serializeArray();
        data[1].value = $('.selected').attr('id');
        $.post(to_redirect, data, function () {
            location.href=to_redirect
        })
    });

    $('form[name=create-room]').on('submit', function (e) {
        e.preventDefault();
        let data = $(this).serializeArray();

        const friends_selected = $('.selected');
        let ids = '';
        for (let i=0;i<friends_selected.length;i++) {
            ids += friends_selected.eq(i).attr('id') + ','
        }
        data[2].value = ids.slice(0, -1);

        $.post('', data, function () {
            location.href='/rooms/'
        })
    });

    const reading_messages = new WebSocket('ws://' + '127.0.0.1:8888' + '/reading_messages/' + $('#id-user').text() + '/');

    reading_messages.onmessage = function (ev) {
        const data = JSON.parse(ev.data);
        const path = location.pathname.split('/');

        if (path[1] === 'rooms') {
            let room_object = $('#' + data);
            room_object.find('.last-message').removeClass('no-read')
        } else {
            if ($('#room').text()) {
                $('.chat-item').removeClass('no-read')
            }
        }

    }

});
