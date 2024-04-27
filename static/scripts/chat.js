$(document).ready(function() {
    let socket = io();

    socket.on("my_message", function(message) {
        let div = $('<div>').addClass('my_message');
        let p = $('<p>').addClass('message');
        p.text(message);
        div.append(p)
        $('.chat').append(div);
    });

    socket.on("message", function(message) {
        let p = $('<p>').addClass('message');
        p.text(message);
        $('.chat').append(p);
    });

    socket.on("server_message", function(message) {
        let div = $('<div>').addClass('server_message');
        let p = $('<p>').text(message);
        div.append(p)
        $('.chat').append(div);
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
