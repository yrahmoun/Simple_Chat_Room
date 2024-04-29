$(document).ready(function() {
    let socket = io();

    socket.on("my_message", function(data) {
        let div = $('<div>').addClass('my_message');
        let picdiv = $('<div>').addClass('picbox');
        let p = $('<p>').addClass('message');
        p.text(data.message);
        console.log(data.pic);
        let img = $('<img>').attr('src', 'static/images/' + data.pic);
        img.addClass('profile_pic');
        picdiv.append(img);
        div.append(picdiv);
        div.append(p)
        $('.chat').append(div);
    });

    socket.on("message", function(data) {
        let div = $('<div>').addClass('user_message');
        let picdiv = $('<div>').addClass('picbox');
        let p = $('<p>').addClass('message');
        p.text(data.message);
        let img = $('<img>').attr('src', 'static/images/' + data.pic);
        img.addClass('profile_pic');
        picdiv.append(img);
        div.append(picdiv);
        div.append(p)
        $('.chat').append(div);
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
