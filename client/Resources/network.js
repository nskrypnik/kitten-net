Net = {}

Net.echo = function () {
	mysocket = Titanium.Network.createTCPSocket("46.19.34.217", 7777);
	console.log("echoing...");
	mysocket.onRead(function (data) {
		console.log("server says:", data.toString());
	}); 
	str = JSON.stringify({"cmd": "echo", params: {"msg":"hello"}});
	setTimeout(function() {
		mysocket.connect();
		setTimeout(function() {
			console.log(mysocket.isConnected)
			mysocket.write(str)
		}, 2000);
	}, 2000);
	mysocket.close();
}