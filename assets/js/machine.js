$(document).ready(function () {

    console.log("being called!")
    var machine1 = $("#machine1").slotMachine({
        active: 0,
        delay: 500
    });


    function onComplete(active) {
        switch (this.element[0].id) {
            case 'machine1':
                $("#machine1Result").text("Index: " + this.active);
                break;
        }
    }

    $("#rec_btn").on('submit', function(event) {
        console.log("hola")
        event.preventDefault()
        machine1.shuffle(5, onComplete);
    })
});
