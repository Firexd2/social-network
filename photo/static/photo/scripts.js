$(document).ready(function () {

    const token = $('input[name=csrfmiddlewaretoken]').val();

    $('.photo p').on('click', function () {
        const cover_url = $(this).attr('cover');
        const id = $(this).attr('id');
        const csrf =
        $.post('', {cover: cover_url, id: id, csrfmiddlewaretoken: token});
        $(this).text('Готово!');
    });

    $('form[name=edit-album]').on('submit', function (e) {
        e.preventDefault();
        const form_array = $(this).serializeArray();
        $.post('', form_array);
        location.reload()
    });
});