
#include <Servo.h>

#define SERVO_HORIZONTAL_PIN    15
#define SERVO_VERTICAL_PIN      13
#define SERVO_HORIZONTAL_MAX    120
#define SERVO_HORIZONTAL_MIN    60
#define SERVO_VERTICAL_MAX      120
#define SERVO_VERTICAL_MIN      60
#define CMD_START_MARK          0xfe

Servo servo_horizontal; 
Servo servo_vertical; 

int servo_h_pos;  
int servo_v_pos;  
int command_h = 0;
int command_v = 0;

const int MAX_H_CMD = SERVO_VERTICAL_MAX - SERVO_VERTICAL_MIN;
const int MAX_V_CMD = SERVO_HORIZONTAL_MAX - SERVO_HORIZONTAL_MIN;

void update_servo(){
  int target_h_angle = SERVO_HORIZONTAL_MIN + command_h;
  int target_v_angle = SERVO_VERTICAL_MIN + command_v;

  if(servo_h_pos < target_h_angle){
    servo_h_pos++;
  }else if(servo_h_pos > target_h_angle){
    servo_h_pos--;
  }

  if(servo_v_pos < target_v_angle){
    servo_v_pos++;
  }else if(servo_v_pos > target_v_angle){
    servo_v_pos--;
  }

  servo_horizontal.write(servo_h_pos);
  servo_vertical.write(servo_v_pos);
  
  delay(10); // Wait for servo to reach desired position
}

void read_command(){
  bool cmd_start_found = false;
  int rx; 
  
  if (Serial.available() > 2) {
    rx = Serial.read();
    if(rx == CMD_START_MARK){
      command_h = Serial.read();
      command_v = Serial.read();

//      Serial.print("CMD:");
//      Serial.print(command_h);
//      Serial.print(", ");
//      Serial.print(command_v);
//      Serial.print(" \n");

      if(command_h > MAX_H_CMD){
        command_h = MAX_H_CMD;
      }

      if(command_v > MAX_V_CMD){
        command_v = MAX_V_CMD;
      }      
    }    
  }  
}

void setup() {
  Serial.begin(115200);
  servo_h_pos = (SERVO_VERTICAL_MAX + SERVO_VERTICAL_MIN) / 2;
  servo_v_pos = (SERVO_HORIZONTAL_MAX - SERVO_HORIZONTAL_MIN) / 2;
  servo_horizontal.attach(SERVO_HORIZONTAL_PIN);  
  servo_vertical.attach(SERVO_VERTICAL_PIN);  
}

void loop() {
  read_command();
  update_servo();
}
