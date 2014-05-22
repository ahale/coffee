
#include "TSIC.h"
#include <Wire.h>
#include <stdlib.h>

#define TSICPIN     16
#define TSICVCCPIN  17

#define SLAVE_ADDR 0x04
#define SAMPLES 10
#define BUFLEN 6

float temperature = 0.0;
int i = 0;
int n = 0;
float total = 0.0;
float readings[SAMPLES];
static char temp_str_buffer[BUFLEN];

TSIC tsic(TSICVCCPIN, TSICPIN);

void setup() {
    Wire.begin(SLAVE_ADDR);
    Serial.begin(115200);
    Wire.onRequest(senddata);
    for (int thisReading = 0; thisReading < SAMPLES; thisReading++) {
        readings[thisReading] = 0.0;
    }
}

void senddata(){
    Wire.write(temp_str_buffer[n]);
    ++n;
    if (n > sizeof(temp_str_buffer)) {
      n = 0;
    }
}

void loop() {
    if (i >= SAMPLES) {
            i = 0;
            Serial.print("temperature: ");
            Serial.println(temp_str_buffer);
    }
    float f = tsic.readTemperature();
    if(isnan(f)) {
        Serial.println("TEMP READ ERROR");
    } else {
        total = total - readings[i];
        readings[i] = f;
        total = total + f;
        i = i + 1;
        temperature = total / 10;
        dtostrf(temperature, 6, 2, temp_str_buffer);
    }
    delay(100);
}
