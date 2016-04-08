$(document).ready(function() {

    $('.like').click(function(e){
        $(this).prop("disabled",true);
        var listid;
        listid = $(this).attr("data-listid")
        e.preventDefault();
        $.get('/lists/', {list_id : listid}, function(data){
            console.log(data)
            $(e.target).children("span").text(data);
        })
    })

}); // end ready