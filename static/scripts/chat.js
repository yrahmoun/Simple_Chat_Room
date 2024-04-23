$(document).ready(function() {
    let socket = io.connect('http://127.0.0.1:5000');

    socket.on("message", function(message) {
        $('.chat').append("<p class='message'>" + message + "</p>");
    });

    $(".button").click(function() {
        let message = $(".input");
        let msg = message.val().trim();
        if (msg !== '') {
            socket.emit('message', msg);
            message.val('');
        }
    });

    /*$(".logout").click(function() {
        socket.emit('logout');
    });*/
});