var http = require('http');
var server = http.createServer().listen(4000);
var io = require('socket.io').listen(server);

var redis = require('socket.io/node_modules/redis');

io.sockets.on('connection', function (socket) {

	
    var sub = redis.createClient();
    var kitty_ID;

    socket.on('join_room', function(kittyID) {
        //Subscribe to the Redis channel for this kitty
        kitty_ID = kittyID;
        sub.subscribe(kittyID);
        console.log('Subscribe to kitty channel: '+kittyID);
    });

    socket.on('disconnect', function() {
       sub.unsubscribe(kitty_ID);
       sub.quit();
       console.log('Unsubscribe to kitty channel: '+kitty_ID);
       kitty_ID = '';
    }); 

    sub.on('message', function(channel, message){
            console.log('send data on channel: '+channel);
            if (channel == kitty_ID) {
                console.log(message);
                json = JSON.parse(message);
                socket.emit(json.action, json);
            }
    });
    
});
