App = {}

App.log = function (data) {
	document.getElementById("log").innerHTML += "<br>" + data;
}

App.netRegistration = function (email, password) {
	Net.addListener("register", function(data){
		console.log("registered", data);
		if (data.params.result == "Ok"){
			Titanium.App.Properties.setString("user_token", data.params.token);
			App.log("registration successfull. Token '" + data.params.token +"'");
		} else {
			App.log("registration failed due to " + data.params.errormsg);
		}
	})
	Net.send("register", {"email": email, "password": password})
}

App.Registration = function () {
	// App.netRegistration()
}

App.netAuth = function (email, paswoken) {	
	var paswoken = paswoken || Titanium.App.Properties.getString("user_token");
	Net.addListener("auth", function (data) {
		if (data.params.result == "Ok") {
			Titanium.App.Properties.setString("user_token", data.params.token);
			App.log("auth successfull. Token '" + data.params.token +"'");
			console.log("auth successfull. Token '" + data.params.token +"'");
		} else {
			App.log("auth failed due to " + data.params.errormsg);
			console.log("auth failed because '" + data.params.errormsg + "'");
		}
	})
	Net.send("auth", {"email": email, "token": paswoken})
}

App.DB = {};
App.DB.open = function () {
	App.DB = Titanium.Database.open();
}
App.DB.close = function () {
	App.DB.close()
}

App.Friends = {};

App.Friends.add = function (email) {
	App.DB.execute('CREATE TABLE IF NOT EXISTS friends (id INTEGER PRIMARY KEY, email VARCHAR(16) NOT NULL, name VARCHAR(16) NOT NULL)');

	Net.addListener("add_friend", function (data) {
		if (data.params.result == "Ok") {
			App.DB.execute('INSERT INTO products (email,name) VALUES (?,?)', email, data.result.name);
			App.log("user " + email +" added succesfully");
			console.log("user " + email +" added succesfully");
		} else {
			App.log("user " + email + " not added because " + data.params.errormsg);
			console.log("user " + email + " not added because " + data.params.errormsg);
		}
	});
	var token = Titanium.App.Properties.getString("user_token")
	Net.send("add_friend", {"email": email, "token": token})
}

App.Friends.render = function (template) {
	var res = App.DB.execute('SELECT * FROM friends');
	var output = "";
	while (res.isValidRow())
	{
		var id = res.fieldByName('id');
		var email = res.fieldByName('email');
		var name = res.fieldByName('name');
		output += template.replace(/%email%/, email).replace(/%name%/, name)
		res.next();
	}
	res.close();
	return output;
}

App.Products = {}

App.Products.add = function () {
	
}

function main() {
	Net.connect();
	$id = document.getElementById;
	 
	if (!Titanium.App.Properties.hasProperty("user_token")){
		// App.register()
	} else {
		
	}
	document.getElementById("log").innerHTML += "<br>" + " token:" + Titanium.App.Properties.getString("user_token");
	
	
}