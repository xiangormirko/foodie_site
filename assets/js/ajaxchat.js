$(document).ready(function () {

    function sync_messages() {
        $.getJSON('/lists/chat/', function(data){

            $.each(data, function(index, value){
                console.log(value)
                console.log(value.pk)
                fields = value.fields
                console.log(fields.avatar)

            })
            
        })
        setTimeout(sync_messages, 2000)
    }
    sync_messages()


}); // end ready