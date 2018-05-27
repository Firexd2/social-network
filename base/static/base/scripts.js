(function(b){b.fn.autoResize=function(f){let a=b.extend({onResize:function(){},animate:!0,animateDuration:150,animateCallback:function(){},extraSpace:20,limit:1E3},f);this.filter("textarea").each(function(){let d=b(this).css({"overflow-y":"hidden",display:"block"}),f=d.height(),g=function(){var c={};b.each(["height","width","lineHeight","textDecoration","letterSpacing"],function(b,a){c[a]=d.css(a)});return d.clone().removeAttr("id").removeAttr("name").css({position:"absolute",top:0,left:-9999}).css(c).attr("tabIndex","-1").insertBefore(d)}(),h=null,e=function(){g.height(0).val(b(this).val()).scrollTop(1E4);var c=Math.max(g.scrollTop(),f)+a.extraSpace,e=b(this).add(g);h!==c&&(h=c,c>=a.limit?b(this).css("overflow-y",""):(a.onResize.call(this),a.animate&&"block"===d.css("display")?e.stop().animate({height:c},a.animateDuration,a.animateCallback):e.height(c)))};d.unbind(".dynSiz").bind("keyup.dynSiz",e).bind("keydown.dynSiz",e).bind("change.dynSiz",e)});return this}})(jQuery);

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


});