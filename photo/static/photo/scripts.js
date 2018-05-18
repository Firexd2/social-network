$(document).ready(function () {

    const token = $('input[name=csrfmiddlewaretoken]').val();

    $('.photo p').on('click', function () {
        const cover_url = $(this).attr('cover');
        $.post('', {cover: cover_url, csrfmiddlewaretoken: token});
        $(this).text('Готово!');
    });
});