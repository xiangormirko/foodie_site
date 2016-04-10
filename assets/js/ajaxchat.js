$(document).ready(function () {

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


    var oldscrollHeight = ($("#chat_target").scrollTop() + 470);

    function sync_messages() {
        $.get('/lists/chat/', function (data) {
            $('#chat_target').html(data);
            var newscrollHeight = $("#chat_target").prop("scrollHeight");
            if (newscrollHeight < (oldscrollHeight + 150)) {
                var height = $('#chat_target')[0].scrollHeight;
                $('#chat_target').scrollTop(height);
            }
            ;
        });
        setTimeout(sync_messages, 1000)
    }

    sync_messages();

    $('#post_form').on('submit', function (event) {
        event.preventDefault();
        console.log("cool!");
        create_post();
    });

    function create_post() {
        // console.log("create post is rocking")
        // console.log($("#id_content").val())
        $.post('/lists/chat/', {the_post: $("#id_content").val()}, function (data) {
            $("#id_content").val('');
            console.log(data);
            console.log('success')
        });
    }


}); // end ready