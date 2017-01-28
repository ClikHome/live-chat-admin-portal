/**
 * Created by Eugene on 16.01.2017.
 */

var api_url = 'http://127.0.0.1:8000/api/v1.0/';
var socket_url = 'http://127.0.0.1:5000/echo';
var messages = document.getElementById('log');
var username = null;


function message_html(username, body, date) {
    var output_date = new Date(date + ' UTC');
    console.log(username);

    return '<div class="msg"><div class="media-body"><small class="actions pull-right">' +
        '<a href="#">Delete</a>&nbsp</small><h5 class="media-heading">' + username + '&nbsp&nbsp&nbsp' +
        '<small class="time"> <i class="fa fa-clock-o"></i>&nbsp' + output_date.toLocaleDateString() +
        '</small> </h5><small class="col-sm-11">' + body + '</small> </div></div>'
}

function chat_connection(url, channel) {
    var sock = new SockJS(url);

    console.log('Started connection...');

    // After socket connection
    sock.onopen = function(e) {
        console.log('Connection opened');

        socket.send(JSON.stringify({
            'data_type': 'auth',
            'channel': channel,
            'username': 'admin_' + channel
        }));

        console.log('admin_' + channel);
    };

    // Chat messages
    sock.onmessage =  function (event) {
        data = jQuery.parseJSON(event.data);

        // Not authorized
        if (data.data_type == 'auth_error') {
            throw data.data.message;

        // Authorized
        } else if (data.data_type == 'auth_success') {
            console.log('Connected!');

        // Message
        } else if (data.data_type == 'message') {
            console.log(data.data);
            $('#log').append(message_html(data.data.username, data.data.body, data.data.created_at));

        } else {
            console.log('Wrong type: ' + data.data_type);
        }
    };

    return sock;
}