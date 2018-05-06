$(document).ready(function () {

    $('.photo p').on('click', function () {
        const cover_url = $(this).attr('cover');
        const id = $(this).attr('id');
        $.post('/edit_cover_album/cover/', {cover: cover_url, id: id});
        $(this).text('Готово!');
    });

    $('form[name=edit-album]').on('submit', function (e) {
        e.preventDefault();
        const form_array = $(this).serializeArray();
        $.post($(this).attr('action'), form_array);
        location.reload()
    });
});