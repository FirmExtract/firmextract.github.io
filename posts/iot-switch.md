# Background

I tried to buy and use an IoT switch that was sold on the market, but everyone was supposed to use it through their own servers.

So I made it myself.

---

# Circuit configuration

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Making%20a%20Wifi%20light%20switch%20based%20on%20the%20ESP-01S%20(ESP8266)%20module/esp01s.jpg" width="100%">

I used the `ESP-01S` module that I bought at a low price before.

It is a module that uses an Espressif ESP8266 SoC with a `Tensilica L106` RISC processor and 17 GPIO pins.

The 'NC' (normal closed) contact of the relay was used to turn off and on the light through the wall switch even when the Wifi connection is disconnected or there is a problem with booting.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Making%20a%20Wifi%20light%20switch%20based%20on%20the%20ESP-01S%20(ESP8266)%20module/spdt.png" width="100%">

The 'NC' (Normal Closed) contact of the relay is a contact that is connected to 'COMMON' when no signal is received and then disconnected from 'COMMON' when a signal is received.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Making%20a%20Wifi%20light%20switch%20based%20on%20the%20ESP-01S%20(ESP8266)%20module/ESP8266BootOptions.jpg" width="100%">

The ESP-01S module that uses 'ESP8266EX' SoC supports three IOs, but all of them are [pins that affect booting](https://www.esp8266.com/viewtopic.php?p=85184).

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Making%20a%20Wifi%20light%20switch%20based%20on%20the%20ESP-01S%20(ESP8266)%20module/gpio4.jpg" width="100%">

I connected the wire to the 'GPIO4' pin that does not affect booting from the module [unused pin](https://hackaday.com/2015/05/31/more-gpios-for-the-esp8266/)

AC-DC converters and linear regulators were used for use in relays and ESP-01S modules by receiving AC power.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Making%20a%20Wifi%20light%20switch%20based%20on%20the%20ESP-01S%20(ESP8266)%20module/acdc.png" width="100%">

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Making%20a%20Wifi%20light%20switch%20based%20on%20the%20ESP-01S%20(ESP8266)%20module/1117.png" width="100%">

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Making%20a%20Wifi%20light%20switch%20based%20on%20the%20ESP-01S%20(ESP8266)%20module/sch.png" width="100%">

It is the final circuit diagram.

---

# Code

I made it work as a Wifi client and show pages to an HTTP server.

```c
#include <ESP8266WebServer.h>
#include <ESP8266WiFi.h>
#include <ESP8266mDNS.h>
#include <WiFiClient.h>

#ifndef STASSID
#define STASSID {Wifi SSID}
#define STAPSK {Wifi Password}
#endif

const char pagemain[] PROGMEM = R"=====(
<!doctype html>
<html>
	<script>
		window.setInterval("(async() => { await refreshStat(); })();", 3000);
		function up() {
			fetch('/up');
		};
		function down() {
			fetch('/down');
		};
		async function refreshStat() {
			fetch("/status")
		.then((response) => response.text())
		.then((data) => document.getElementById("stat").innerText = 'current status: ' + data)
		};
	</script>
<head>
  <title>Light panel</title>
</head>
<body>
	<p id="stat">current status: up</p>
	<button onclick=up()>power up</button>
	<button onclick=down()>power down</button>
</body>
</html>
)=====";

const char *ssid = STASSID;
const char *password = STAPSK;

ESP8266WebServer server(80);

const int out = 4;

int stat = 1;

void handleRoot() {
	String html = pagemain;
	server.send(200, "text/html", html);
}

char *up() {
	stat = 1;
	return "up ok";
}

char *down() {
	stat = 0;
	return "down ok";
}

char *getstatus() {
	if (stat == 0)
		return "down";
	else
		return "up";
}

void handleNotFound() {
	String message = "File Not Found\n\n";
	message += "URI: ";
	message += server.uri();
	message += "\nMethod: ";
	message += (server.method() == HTTP_GET) ? "GET" : "POST";
	message += "\nArguments: ";
	message += server.args();
	message += "\n";
	for (uint8_t i = 0; i < server.args(); i++)
		message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
	server.send(404, "text/plain", message);
}

void setup(void) {
	pinMode(out, OUTPUT);
	Serial.begin(115200);
	WiFi.mode(WIFI_STA);
	WiFi.begin(ssid, password);
	Serial.println("");

	while (WiFi.status() != WL_CONNECTED) {
		delay(500);
		Serial.print(".");
	}

	Serial.println("");
	Serial.print("Connected to ");
	Serial.println(ssid);
	Serial.print("IP address: ");
	Serial.println(WiFi.localIP());

	if (MDNS.begin("light")) {
		Serial.println("MDNS responder started");
	}

	server.on("/", handleRoot);

	server.on("/status", []() {
		Serial.println("stat.. 0");
		server.send(200, "text/plain", getstatus());
	});

	server.on("/up", []() {
		Serial.println("output 1");
		server.send(200, "text/plain", up());
	});

	server.on("/down", []() {
		Serial.println("output 0");
		server.send(200, "text/plain", down());
	});

	server.onNotFound(handleNotFound);

	server.begin();
	Serial.println("HTTP server started");
}

void loop(void) {
	server.handleClient();
	MDNS.update();
	if (stat == 0)
		digitalWrite(out, 1);
	else
		digitalWrite(out, 0);
}

```

In `setup()`, which is executed only once during booting, it defines output pins, connects to Wifi, and configures HTTP server.

The server shows the main page or changes the value of the variable `stat` according to the request and returns the current status.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Making%20a%20Wifi%20light%20switch%20based%20on%20the%20ESP-01S%20(ESP8266)%20module/panel.png" width="100%">

The main page prints the current state and buttons that send requests to the `up` and `down` paths.


When a request is made to the server's `up` path, the value of `stat` becomes 1.

Conversely, when a request is received in the `down` path, the value of `stat` becomes 0.

In `loop()`, which is repeatedly executed after the `setup()` function is executed, a signal is sent to the GPIO pin according to the value of the variable `stat`.

According to the signal of the GPIO pin, the relay contact operates to turn the light on and off.

---

# Make hardware

Wiring and soldering on the prototyping board according to the prepared circuit diagram.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Making%20a%20Wifi%20light%20switch%20based%20on%20the%20ESP-01S%20(ESP8266)%20module/b1.jpg" width="100%">

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Making%20a%20Wifi%20light%20switch%20based%20on%20the%20ESP-01S%20(ESP8266)%20module/b2.jpg" width="100%">

I [connected the `DTR` and `RTS` pins](https://acoptex.com/project/289/basics-project-021b-how-to-update-firmware-esp8266-esp-01-wi-fi-module-at-acoptexcom/) and flashed it so that the Arduino IDE could automatically switch the module to flashing mode and reset it.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Making%20a%20Wifi%20light%20switch%20based%20on%20the%20ESP-01S%20(ESP8266)%20module/f1.jpg" width="100%">

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Making%20a%20Wifi%20light%20switch%20based%20on%20the%20ESP-01S%20(ESP8266)%20module/ide.png" width="100%">

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Making%20a%20Wifi%20light%20switch%20based%20on%20the%20ESP-01S%20(ESP8266)%20module/flashing1.png" width="100%">

---

# Install

I installed it between the wiring coming from the ceiling and the wiring of the lighting.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Making%20a%20Wifi%20light%20switch%20based%20on%20the%20ESP-01S%20(ESP8266)%20module/i1.jpg" width="100%">

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Making%20a%20Wifi%20light%20switch%20based%20on%20the%20ESP-01S%20(ESP8266)%20module/i2.jpg" width="100%">

---

# Test

It works well as intended.

<video src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Making%20a%20Wifi%20light%20switch%20based%20on%20the%20ESP-01S%20(ESP8266)%20module/light1.mp4" controls width="100%"></video>

<video src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Making%20a%20Wifi%20light%20switch%20based%20on%20the%20ESP-01S%20(ESP8266)%20module/light2.mp4" controls width="100%"></video>

Thanks for reading!
