const result = document.querySelector('#result-div');
$(document).ready(function() {
    // Connect to the Socket.IO server.
    // The connection URL has the following format, relative to the current page:
    //     http[s]://<domain>:<port>[/<namespace>]
    var socket = io();

    // Event handler for new connections.
    // The callback function is invoked when a connection with the
    // server is established.
    // 新規接続時
    socket.on('connect', function() {
        socket.emit('my_event', {data: 'connected'});
    });

    window.setInterval(function() {
        //サーバーにデータを送信する
        //$('form#emit').submit(function(event) {
        //    socket.emit('my event', {data: $('#emit_data').val()});
        //    return false;
        //});
        socket.emit('stt_result', {data: stt_result});

        // Event handler for server sent data.
        // The callback function is invoked whenever the server emits data
        // to the client. The data is then displayed in the "Received"
        // section of the page.
        // サーバーからjumanppで解析済みデータを受信する
        socket.on('jumanpp_parser', function(msg, cb) {
            //表示だけ
            $('#log').replaceWith('<div id="log">' + msg.data + '</div>');
            //if ( msg.data.match('【相槌可能】')) {
            //    $('.bg').css( { 'background-color' : 'rgba(255,255,255,.8)'});
            //} else {
            //    $('.bg').css( { 'background-image' : 'linear-gradient(45deg, red, blue)'});
            //}
            if (cb)    // 名前空間
                cb();
        });
    }, 100);    //100ミリ秒間隔で通信

    // Interval function that tests message latency by sending a "ping"
    // message. The server then responds with a "pong" message and the
    // round trip time is measured.
    // PING
    var ping_pong_times = [];
    var start_time;
    window.setInterval(function() {
        start_time = (new Date).getTime();
        $('#transport').text(socket.io.engine.transport.name);
        socket.emit('my_ping');
    }, 1000);

    // Handler for the "pong" message. When the pong is received, the
    // time from the ping is stored, and the average of the last 30
    // samples is average and displayed.
    socket.on('my_pong', function() {
        var latency = (new Date).getTime() - start_time;
        ping_pong_times.push(latency);
        ping_pong_times = ping_pong_times.slice(-30); // keep last 30 samples
        var sum = 0;
        for (var i = 0; i < ping_pong_times.length; i++)
            sum += ping_pong_times[i];
        $('#ping-pong').text(Math.round(10 * sum / ping_pong_times.length) / 10);
    });
});