#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h> 
#include <WiFiClientSecure.h> // for http request to Google API
//#include "404.h"

// 4x1 keypad
const uint8_t Key1 = D1;
const uint8_t Key2 = D2;
const uint8_t Key3 = D3;
const uint8_t Key4 = D4;

const int buttonPin[4] = {Key1 , Key2 ,Key3 ,Key4 };

// light 
const uint8_t GreenPin = D7;
const uint8_t RedPin = D6;

// Wifi setting 
const char SSID[] = "TP-Link_02B8";
const char WIFIpassword[] = "32974560";

// Admin user setting 
const char USERNAME[] = "admin";
const char PASSWORD[] = "admin";

// Door password
String DoorPassword= "123";
uint8_t DoorPasswordLen = 3;
uint8_t idx = 0 ;
bool Open = false ; 

const char Host[] = "192.168.1.103";
String URL = "/";


// fingerprint:
// 9A:71:DE:E7:1A:B2:25:CA:B4:F2:36:49:AB:CE:F6:25:62:04:E4:3C
const char fingerprint[] = "9A:71:DE:E7:1A:B2:25:CA:B4:F2:36:49:AB:CE:F6:25:62:04:E4:3C";


void setup(){
    /*---- software setup----*/
    // init Serial 
    Serial.begin(9600);
    // start connect to AP
    WiFi.begin( SSID , WIFIpassword );

    // Wait for connection 

    while( WiFi.status() != WL_CONNECTED ){
        delay(500);
        Serial.print(".");
    }
    // after connection 
    Serial.println("Connected to WiFi !");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
}


void TryGetPythonHTTPServer(){
    if(WiFi.status()!= WL_CONNECTED){
      Serial.println("Bad connection!");
      return ;
    }
    Serial.println("Try to get python server");
    WiFiClientSecure broswer;
    // set fingerprint
    broswer.setFingerprint(fingerprint);
    // https request
    if( broswer.connect(Host , 8888)){
        broswer.print(String("GET ") + URL + " HTTP/1.1\r\n" +
                  "Host: " + Host + "\r\n" +
                  "User-Agent: NodeMCU\r\n" +
                  "Connection: close\r\n\r\n");
        
        Serial.println("Send Request");

        //  received data
        while (broswer.connected()){
            while (broswer.available()){
                String str = broswer.readStringUntil('\n'); // 每次讀取到換行時輸出資料
                Serial.println(str);
            }
        }
    }
    else{
        Serial.println("Connection failed");
    }
}

void loop(void){

    TryGetPythonHTTPServer();
    delay(500);
}
