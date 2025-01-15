#ifndef ULTRA_SONIC_H
#define ULTRA_SONIC_H

#include <Arduino.h>
#include "env.h"


//define sound velocity in cm/uS
#define SOUND_VELOCITY 0.034


double getUltraSonicDistance(){
    // Clears the atoi(TRIG_PIN)
    digitalWrite(atoi(TRIG_PIN), LOW);
    delayMicroseconds(2);
    // Sets the atoi(TRIG_PIN) on HIGH state for 10 micro seconds
    digitalWrite(atoi(TRIG_PIN), HIGH);
    delayMicroseconds(10);
    digitalWrite(atoi(TRIG_PIN), LOW);
    
    // Reads the atoi(ECHO_PIN), returns the sound wave travel time in microseconds
    int duration = pulseIn(atoi(ECHO_PIN), HIGH);
    
    // Calculate the distance
    int distanceCm = duration * SOUND_VELOCITY/2;
    
    // Convert to inches
    
    // Prints the distance on the Serial Monitor
    Serial.print("Distance (cm): ");
    Serial.println(distanceCm);

    return distanceCm;
}


#endif // ULTRA_SONIC_H