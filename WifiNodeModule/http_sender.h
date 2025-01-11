#ifndef HTTP_SENDER_H
#define HTTP_SENDER_H

#include <WiFiClient.h>
#include <WiFiClientSecure.h>

#include "env.h"


// HTTP Method enum

enum HTTPMethod{
    GET,
    POST,
    PUT,
    DELETE
};

enum HTTPProtocol{
    HTTP,
    HTTPS
};

class HTTPSender {
public:
    HTTPSender(HTTPProtocol protocol) {
        if (protocol == HTTP) {
            client = new WiFiClient();  // Create a new WiFiClient for HTTP
        } else {
            client = new WiFiClientSecure();  // Create a new WiFiClientSecure for HTTPS
        }
        this->protocol = protocol;
    }

    ~HTTPSender() {
        delete client;  // Clean up dynamically allocated client
    }

    void init_https(const char* fingerprint) {
        if(protocol == HTTP) {
            Serial.println("Cannot set fingerprint for HTTP");
            return;
        }
        client->setFingerprint(fingerprint);
    }

    void get(String host, String url) {
        if (client->connect(host.c_str(), protocol == HTTP ? SERVER_PORT : 443)) {
            client->print(String("GET ") + url + " HTTP/1.1\r\n" +
                          "Host: " + host + "\r\n" +
                          "User-Agent: HTTPSender\r\n" +
                          "Connection: close\r\n\r\n");

            while (client->connected()) {
                while (client->available()) {
                    String line = client->readStringUntil('\n');
                    Serial.println(line);
                }
            }
        } else {
            Serial.println("Connection failed");
        }
    }

    void post(String host, String url, String payload) {
        if (client->connect(host.c_str(), protocol == HTTP ? SERVER_PORT : 443)) {
            client->print(String("POST ") + url + " HTTP/1.1\r\n" +
                          "Host: " + host + "\r\n" +
                          "User-Agent: HTTPSender\r\n" +
                          "Content-Type: application/x-www-form-urlencoded\r\n" +
                          "Content-Length: " + String(payload.length()) + "\r\n" +
                          "Connection: close\r\n\r\n" +
                          payload);

            while (client->connected()) {
                while (client->available()) {
                    String line = client->readStringUntil('\n');
                    Serial.println(line);
                }
            }
        } else {
            Serial.println("Connection failed");
        }
    }

private:
    HTTPProtocol protocol;
    Client* client;  // Base class pointer for polymorphism
};


#endif