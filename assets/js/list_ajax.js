var csrftoken = $.cookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$('.btn.btn-danger.delete').click(function () {
    rest_pk = $(this).attr('rest_pk');
    list_pk = $(this).attr('list_pk');
    $(this).remove();
    $.post('/lists/' + list_pk + '/', {rest_pk: rest_pk}, function (data) {

        $("div[div_id=" + data + "]").remove();
    })
});