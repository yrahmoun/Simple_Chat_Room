$(document).ready(function() {
    let socket = io();

    socket.on("my_message", function(message) {
        $('.chat').append("<div class='my_message'><p class='message'>" + message + "</p></div>");
    });

    socket.on("message", function(message) {
        $('.chat').append("<p class='message'>" + message + "</p>");
    });

    socket.on("server_message", function(message) {
        $('.chat').append("<div class='server_message'><p>" + message + "</p></div>");
    })

    $(".button").click(function() {
        let message = $(".input");
        let msg = message.val().trim();
        if (msg !== '') {
            socket.emit('message', msg);
            message.val('');
        }
    });
});
