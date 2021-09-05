/***************************************************
//Web: http://www.buydisplay.com
EastRising Technology Co.,LTD
Examples for ER-OLEDM0.42-1
Display is Hardward I2C 2-Wire I2C Interface 
Tested and worked with:
Works with Arduino 1.6.0 IDE  
Test OK : Arduino DUE,Arduino mega2560,Arduino UNO Board 
****************************************************/
#include <Wire.h>
#include "er_oled.h"

/*
  == Hardware connection for 4 PIN module==
    OLED   =>    Arduino
  *1. GND    ->    GND
  *2. VCC    ->    3.3V
  *3. SCL    ->    SCL
  *4. SDA    ->    SDA 
*/
#define STEP    10
uint8_t oled_buf[WIDTH * HEIGHT / 8];

void setup() {
  Serial.begin(115200);
  Serial.print("OLED Example\n");
  Wire.begin();
  
  /* display an image of bitmap matrix */
  er_oled_begin();
  er_oled_clear(oled_buf); 
  er_oled_display(oled_buf);
}

void loop() {
  delay(2000);
  eyeBlink();
}

void eyeBlink(){
  int16_t x, y;
  
  for(y = 0; y < HEIGHT; y ++) {   
      for(x = 0; x < WIDTH; x++){      
        er_oled_pixel(x, y, 1, oled_buf);      
      }
  }  
  er_oled_set_scan_direction(true);
  er_oled_display(oled_buf);

  er_oled_clear(oled_buf);
  er_oled_set_scan_direction(false);  
  er_oled_display(oled_buf);  
}
