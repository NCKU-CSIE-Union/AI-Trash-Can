#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h> 
#include <WiFiClientSecure.h> // for http request to Google API

#include "env.h"
#include "http_sender.h"
#include "ultra_sonic.h"

HTTPSender *sender;

void TryGetPythonHTTPServer(HTTPSender *sender){
    if(WiFi.status()!= WL_CONNECTED){
      Serial.println("Bad connection!");
      return ;
    }
    Serial.println("Try to get python server");
    sender->get(SERVER_HOST, TEST_URL);
}


void setup(){
    /*---- software setup----*/
    // init Serial 
    Serial.begin(9600);
    // start connect to AP
    WiFi.begin( SSID , WIFI_PASSWORD );
    // Wait for connection 
    while( WiFi.status() != WL_CONNECTED ){
        delay(500);
        Serial.print(".");
    }
    // after connection 
    Serial.println("Connected to WiFi !");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());


    sender = new HTTPSender();
    #ifdef SERVER_PROTOCOL == "HTTP"
    #else
        sender->init_https(HTTPS_FINGERPRINT);
    #endif
}

int buttonState = 0;
int lastState = 0;
void loop(void){
    lastState = buttonState;
    buttonState = digitalRead(buttonPin);


    if (buttonState == HIGH && buttonState != lastState) {
        TryGetPythonHTTPServer();
    }
}
