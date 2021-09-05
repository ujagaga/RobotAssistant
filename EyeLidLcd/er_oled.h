#ifndef _er_oled_H_
#define _er_oled_H_

#include <avr/pgmspace.h>

#define WIDTH 72
#define HEIGHT 40
#define PAGES HEIGHT/8

#define OLED_RST  8 
//I2C
#define IIC_CMD        0X00
#define IIC_RAM        0X40
#define command(Reg)  I2C_Write_Byte(Reg, IIC_CMD)
#define data(Data)    I2C_Write_Byte(Data, IIC_RAM)


void er_oled_begin();
void er_oled_display(uint8_t* buffer);
void er_oled_set_scan_direction(bool inverse);
void er_oled_clear(uint8_t* buffer);
void er_oled_pixel(int x,int y,char color, uint8_t* buffer);
void I2C_Write_Byte(uint8_t value, uint8_t Cmd);

#endif
