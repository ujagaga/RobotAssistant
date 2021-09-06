#ifndef _oled_H_
#define _oled_H_

#define WIDTH 72
#define HEIGHT 40
#define PAGES HEIGHT/8

#define IIC_CMD        0X00
#define IIC_RAM        0X40
#define command(Reg)  I2C_Write_Byte(Reg, IIC_CMD)
#define data(Data)    I2C_Write_Byte(Data, IIC_RAM)


void oled_begin();
void oled_display(uint8_t* buffer);
void oled_clear(uint8_t* buffer);
void oled_pixel(int x,int y,char color, uint8_t* buffer);
void oled_set_scan_direction(bool inverse);
void I2C_Write_Byte(uint8_t value, uint8_t Cmd);

#endif
