var sys = require('sys');
var net = require('net');
var mqtt = require('mqtt')
var io  = require('socket.io').listen(3000);

var mqtt = require('mqtt'), url = require('url');
// Parse 
var mqtt_url = url.parse(process.env.CLOUDMQTT_URL || 'mqtt://localhost:1883');
var auth = (mqtt_url.auth || ':').split(':');
var url = "mqtt://" + mqtt_url.host;


var options = {
  port: mqtt_url.port,
  //clientId: 'Esp0011',
  username: 'sammy',
  password: 'rfid',
};

// Create a client connection
var client = mqtt.connect(url, options);

client.on('connect', function() { // When connected
console.log("connected");
  // subscribe to a topic
  client.subscribe('test', function() {
	  console.log("subscribe");
  });
  
    client.on('message', function(topic, message){
      console.log(message.toString());
	  sys.puts(topic+'='+message+'/=0001');
	  io.sockets.emit('mqtt',{'topic':String(topic),
		'payload':String(message+'/=0001')});
	});
  
});




