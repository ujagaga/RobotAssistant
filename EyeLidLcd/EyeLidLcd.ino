#include "oled.h"

/*
  == Hardware connection for 4 PIN module==
    OLED   =>    Arduino
  *1. GND    ->    GND
  *2. VCC    ->    3.3V
  *3. SCL    ->    SCL
  *4. SDA    ->    SDA 
*/

uint8_t oled_buf[WIDTH * HEIGHT / 8];

void setup() {
  
  /* display an image of bitmap matrix */
  oled_begin();
  oled_clear(oled_buf); 
  oled_display(oled_buf);
}

void loop() {
  delay(2000);
  eyeBlink();
}

void eyeBlink(){
  int16_t x, y;
  
  for(y = 0; y < HEIGHT; y ++) {   
      for(x = 0; x < WIDTH; x++){      
        oled_pixel(x, y, 1, oled_buf);      
      }
  }  
  oled_set_scan_direction(true);
  oled_display(oled_buf);

  oled_clear(oled_buf);
  oled_set_scan_direction(false);  
  oled_display(oled_buf);  
}
