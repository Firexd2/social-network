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
                        $('#results-container').html('Ничего не нашлось');
                    }
                })
            }, 500)
        }
    })
});