Net = {
	address: "46.19.34.217",
	port: 7777,
}

Net.connect = function (address, port) {
	var address = address || this.address;
	var port = port || this.port;
	this.socket = Titanium.Network.createTCPSocket(address, port);
	console.log("[Net] open", address, port)
	
	var receivingFunction = this._receive;
	var context = this
	this.socket.onRead(function (data) {
		console.log("[Net] connect callbacks", context.receiveCallbacks);
		receivingFunction.apply(context, [JSON.parse(data.toString())]);
	});

	this.socket.onError(function (e) {
		console.warn("[Net] error:", e)
	})
}


Net.addListener = function (eventCmd, callback) {
	if (this.receiveCallbacks == null) this.receiveCallbacks = {};
	this.receiveCallbacks[eventCmd] = callback;
	// console.log("[Net] listeners", this.receiveCallbacks )
}

Net._receive = function (dataObj) {
	// if (this.receiveCallbacks == null) this.receiveCallbacks = {};
	// console.log("[Net] _receive", dataObj.cmd, dataObj);
	var receiveCallbacks = this.receiveCallbacks;
	for (cmd in receiveCallbacks) {
		if (cmd == dataObj.cmd) {
			console.log("[Net] calling handler of", dataObj.cmd)
			receiveCallbacks[cmd](dataObj);
		}
	}
}

Net.send = function (cmd, params) {
	var socket = this.socket;
	var data = JSON.stringify({"cmd":cmd, "params": params});
	// console.log("[Net] sending", data);
	if (socket.isClosed()){
		// console.log("[Net] send: closed, opening")
		socket.connect();
		setTimeout(function() {
			if (socket.isClosed()){
				console.log("[Net] send: closed, opening, sending")
				setTimeout(function() {
					socket.write(data)
					console.log("[Net] sent", data);
				}, 2000);
			} else {
				socket.write(data)
				console.log("[Net] sent", data);
			}
		}, 2000);
	} else {
		console.log("[Net] sent", data);
		socket.write(data)
	}
}

Net.echo = function () {
	Net.addListener("echo", function (obj){
		console.log("server says:", obj)
	})
	Net.send("echo", {"msg":"hello"})
}