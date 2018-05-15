$(document).ready(function () {
    $('textarea[name=wall]').on('focusin', function () {
        $('#button-wall').show()
    });
    $(document).mouseup(function (e) {
        const container = $(".wall");
        if (e.target!==container[0] && !container.has(e.target).length){
            $('#button-wall').hide();
        }
    });
});
