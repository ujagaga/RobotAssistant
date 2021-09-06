#include <Wire.h>
#include "oled.h"
#include "Arduino.h"

void I2C_Write_Byte(uint8_t value, uint8_t Cmd)
{
  uint8_t Addr = 0x3c;
  Wire.beginTransmission(Addr);
  Wire.write(Cmd);
  Wire.write(value);
  Wire.endTransmission();
}

void oled_begin()
{
  Wire.begin();
  Wire.setClock(200000);

  command(0xae);//--turn off oled panel

  command(0xd5);//--set display clock divide ratio/oscillator frequency
  command(0x80);//--set divide ratio

  command(0xa8);//--set multiplex ratio
  command(0x27);//--1/40 duty

  command(0xd3);//-set display offset
  command(0x00);//-not offset

  command(0xad);//--Internal IREF Setting	
  command(0x30);//--

  command(0x8d);//--set Charge Pump enable/disable
  command(0x14);//--set(0x10) disable

  command(0x40);//--set start line address

  command(0xa6);//--set normal display

  command(0xa4);//Disable Entire Display On

  command(0xa1);//--set segment re-map 128 to 0

  command(0xC8);//--Set COM Output Scan Direction 64 to 0

  command(0xda);//--set com pins hardware configuration
  command(0x12);

  command(0x81);//--set contrast control register
  command(0xaf);

  command(0xd9);//--set pre-charge period
  command(0x22);

  command(0xdb);//--set vcomh
  command(0x20);

  command(0xaf);//--turn on oled panel
    
}

void oled_clear(uint8_t* buffer)
{
	int i;
	for(i = 0;i < WIDTH * HEIGHT / 8;i++)
	{
		buffer[i] = 0;
	}
}


void oled_pixel(int x, int y, char color, uint8_t* buffer)
{
    if(x > WIDTH || y > HEIGHT)return ;
    if(color)
        buffer[x+(y/8)*WIDTH] |= 1<<(y%8);
    else
        buffer[x+(y/8)*WIDTH] &= ~(1<<(y%8));
}

void oled_display(uint8_t* pBuf)
{    
    uint8_t page,i;   
    for (page = 0; page < PAGES; page++) {         
        command(0xB0 + page);/* set page address */     
        command(0x0c);   /* set low column address */      
        command(0x11);  /* set high column address */           
        for(i = 0; i< WIDTH; i++ ) {
          data(pBuf[i+page*WIDTH]);// write data one
        }        
    }
}

void oled_set_scan_direction(bool inverse)
{    
    if(inverse){
      command(0xC0);
    }else{
      command(0xC8);
    }
}
