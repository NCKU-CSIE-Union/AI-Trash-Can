#ifndef ULTRA_SONIC_H
#define ULTRA_SONIC_H

#include <Arduino.h>


//define sound velocity in cm/uS
#define SOUND_VELOCITY 0.034

const int trigPin = 14;
const int echoPin = 12;
double getUltraSonicDistance(){
    // Clears the trigPin
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    // Sets the trigPin on HIGH state for 10 micro seconds
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    
    // Reads the echoPin, returns the sound wave travel time in microseconds
    duration = pulseIn(echoPin, HIGH);
    
    // Calculate the distance
    distanceCm = duration * SOUND_VELOCITY/2;
    
    // Convert to inches
    
    // Prints the distance on the Serial Monitor
    Serial.print("Distance (cm): ");
    Serial.println(distanceCm);
}


#endif // ULTRA_SONIC_H