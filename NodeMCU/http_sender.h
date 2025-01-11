#ifndef HTTP_SENDER_H
#define HTTP_SENDER_H

#include <WiFiClient.h>
#include <WiFiClientSecure.h>

#include "env.h"
#define HTTP_SERVER_PORT aiot(SERVER_PORT)

class HTTPSender {
public:
    HTTPSender() {
        #ifdef SERVER_PROTOCOL == "HTTP"
            client = new WiFiClient();
        #else
            client = new WiFiClientSecure();
        #endif
    }

    ~HTTPSender() {
        delete client;  // Clean up dynamically allocated client
    }


    void init_https(const char* fingerprint) {
        #ifdef SERVER_PROTOCOL == "HTTP"
            Serial.println("Cannot set fingerprint for HTTP");
            return;
        #else // HTTPS
            client->setFingerprint(fingerprint);
        #endif
    }

    void get(String host, String url) {
        if (client->connect(host.c_str(), SERVER_PROTOCOL == "HTTP" ? HTTP_SERVER_PORT : 443)) {
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
        if (client->connect(host.c_str(), SERVER_PROTOCOL == "HTTP" ? HTTP_SERVER_PORT : 443)) {
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
    #ifdef SERVER_PROTOCOL == "HTTP"
        WiFiClient *client;
    #else
        WiFiClientSecure *client;
    #endif
};


#endif