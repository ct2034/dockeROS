#include <FastLED.h>

#define NUM_LEDS 3

#define DATA_PIN A5

CRGB leds[NUM_LEDS];
int inByte = 0;        
int r, g, b;

void setup() {
   	delay(2000);
    FastLED.addLeds<WS2811, DATA_PIN, RGB>(leds, NUM_LEDS);
    Serial.begin(9600);
    while (!Serial) {
      ; // wait
    }
    for(int led = 0; led < NUM_LEDS; led = led + 1) {
      leds[led].setRGB(0, 0, 0);
      FastLED.show();
    }
}

void loop() {
  if (Serial.available() > 0) {
    inByte = Serial.read();
    r = 0;
    g = 0;
    b = 0;
    if(inByte == 'r'){
      r = 255;
    }
    else if(inByte == 'g'){
      g = 255;
    }
    else if(inByte == 'b'){
      b = 255;
    } 
    else if(inByte == 'c'){
      g = 255;
      b = 255;
    } 
    else if(inByte == 'm'){
      r = 255;
      b = 255;
    } 
    else if(inByte == 'y'){
      r = 255;
      g = 255;
    } 
    else if(inByte == 'w'){
      r = 255;
      g = 255;
      b = 255;
    } 
    for(int led = 0; led < NUM_LEDS; led = led + 1) {
      leds[led].setRGB(r, g, b);
      FastLED.show();
    }
  }
}
