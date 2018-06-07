(function(b){b.fn.autoResize=function(f){let a=b.extend({onResize:function(){},animate:!0,animateDuration:150,animateCallback:function(){},extraSpace:20,limit:1E3},f);this.filter("textarea").each(function(){let d=b(this).css({"overflow-y":"hidden",display:"block"}),f=d.height(),g=function(){var c={};b.each(["height","width","lineHeight","textDecoration","letterSpacing"],function(b,a){c[a]=d.css(a)});return d.clone().removeAttr("id").removeAttr("name").css({position:"absolute",top:0,left:-9999}).css(c).attr("tabIndex","-1").insertBefore(d)}(),h=null,e=function(){g.height(0).val(b(this).val()).scrollTop(1E4);var c=Math.max(g.scrollTop(),f)+a.extraSpace,e=b(this).add(g);h!==c&&(h=c,c>=a.limit?b(this).css("overflow-y",""):(a.onResize.call(this),a.animate&&"block"===d.css("display")?e.stop().animate({height:c},a.animateDuration,a.animateCallback):e.height(c)))};d.unbind(".dynSiz").bind("keyup.dynSiz",e).bind("keydown.dynSiz",e).bind("change.dynSiz",e)});return this}})(jQuery);

function scroll_to_bottom() {
    const block = document.getElementById("chat");
    block.scrollTop = block.scrollHeight;
}

jQuery(function(){
    jQuery('textarea').autoResize();
});

$(document).ready(function () {

    $(document).mouseup(function (e) {
        const container = $("#search-results");
        if (e.target!==container[0] && !container.has(e.target).length){
            container.hide();
        }
    });

    let timer;
    $('input[name=general-search]').on('input focus', function () {
        const request = $(this).val();
        if (request) {
            clearInterval(timer);
            $('#search-results').show();
            timer = setTimeout(function () {
                $.post('/general_search/', {request: request}, function (data) {

                    const $data = data.response;
                    const dataKeys = Object.keys($data);
                    let result_html;

                    for (let i = 0; i < dataKeys.length; i++) {
                        result_html += '<tr onclick="location.href=\'' + $data[dataKeys[i]].url + '\'">\n' +
                            '<td width="40">\n' +
                            '<img width="40" height="40" src="' + $data[dataKeys[i]].avatar + '" alt="">\n' +
                            '</td>\n' +
                            '<td>' + dataKeys[i] + '</td>\n' +
                            '</tr>'
                    }
                    if (result_html) {
                        $('#results-container').html(result_html);
                    } else {
                        $('#results-container').html('<p>Ничего не нашлось</p>');
                    }
                })
            }, 500)
        }
    });

    $(function () {
        if ($('.block-menu').length) {
            const current_name_page = location.pathname.split('/').slice(-2)[0];
            const items = $('.block-menu .nav-item');
            items.removeClass('active');
            for (let i=0;i<items.length;i++) {
                if (items.eq(i).children().attr('href').split('/').slice(-2)[0] === current_name_page) {
                    items.eq(i).addClass('active');
                    break
                }
            }
        }
    });

    if ($('#id-user').text()) {

        const alerts = new WebSocket('ws://' + location.host.slice(0,-4) + '8888' + '/pages_alerts/' + $('#id-user').text() + '/');
        const current_rooms_in_counter = $('#list-rooms').text().slice(1, -1).split(',');

        alerts.onmessage = function (ev) {
            const data = JSON.parse(ev.data);
            const id = String(data.room_id);
            const path = location.pathname;

            let counter = $('#count-messages');
            const prev_counter = counter.text() ? parseInt(counter.text()) : 0;
            const alert = $('.new-m');
            const name_in_alert = $('.new-m #name');

            if (current_rooms_in_counter.indexOf(id) === -1) {
                counter.show();
                counter.text(prev_counter + 1);
                current_rooms_in_counter.push(id);
            }
            if (data.room_type === 'dialog' && path !== '/rooms/' && path.split('/')[1] !== 'room') {
                name_in_alert.text(data.user);
                alert.show(300);
                setTimeout(function () {
                    alert.hide(300)
                }, 5000)
            }

            if (path === '/rooms/') {
                let room_object = $('#' + id);
                if (room_object.length) {
                    room_object.addClass('no-read');
                    room_object.find('.last-message').html('<img height="25"' +
                        ' src="' + data.user_avatar_25x25 + '" width="25"> ' +
                        '<span class="message">' + data.text + '</span>');
                    room_object.find('.time').text(data.time);
                    room_object = room_object.remove();
                    room_object.prependTo($('#container-rooms'))
                } else {
                    $('#non-chats').remove();
                    $('#container-rooms').prepend('<tr id="' + data.room_id +'" class="no-read" onclick="location.href=\'' + data.room_url +'\'">\n' +
                        '    <td width="50"><img src="'+ data.room_logo +'" alt=""></td>\n' +
                        '    <td>\n' +
                        '    <div class="name-chat">\n' +
                        '    <b>' + data.room_name + '</b>\n' +
                        '    </div>\n' +
                        '    <div class="last-message no-read">\n' +
                        '    <img src="' + data.user_avatar_25x25 + '" alt="">\n' +
                        '    <span class="message">' + data.text + '</span>\n' +
                        '    </div>\n' +
                        '    </td>\n' +
                        '    <td style="text-align: right" class="time" width="100">' + data.time + '</td>\n' +
                        '</tr>')
                }
            }
            if (path.split('/')[1] === 'room') {
                const chat_log = $('.chat-log');
                let new_message_object = '';
                const data_user_id = String(data.user_id);
                const chat_item = $('.chat-item').last();
                const last_user_id = chat_item.attr('user');

                const last_datetime = chat_item.attr('time');

                const data_time = parseInt(data.time.split(':').slice(-1));
                const last_time = parseInt(last_datetime.split(':').slice(-1));

                if ((data_user_id === last_user_id) && (last_datetime.length === 5) && (data_time - last_time < 6) ) {
                    new_message_object = '<div user="' + data.user_id +'" time="' + data.time + '" class="chat-item other no-read">\n' +
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
                    const short_name = data.user.split(' ')[0];
                    new_message_object = '<div user="' + data.user_id +'" time="' + data.time + '" class="chat-item other no-read">\n' +
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
                scroll_to_bottom()
            }
        }
    }
});