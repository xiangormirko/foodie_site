$(document).ready(function () {

    function sync_messages() {
        $.getJSON('/lists/chat/', function(data){
            console.log(data)
            
        })

        setTimeout(sync_messages, 2000)

    }
    sync_messages()


}); // end ready