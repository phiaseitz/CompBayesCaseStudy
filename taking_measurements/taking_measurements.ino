#include <Servo.h>

char incoming_message_char='0';
int incoming_message = 0;
int counter=0;
int horizontal_angle_track=90;
int horizontal_increment=1;
int reading = 0;


Servo horizontal_servo;
Servo vertical_servo;

void setup() {                
  // initialize the digital pin as an output.
  pinMode(A5, INPUT);    
  Serial.begin(9600); 
  horizontal_servo.attach(9);
  horizontal_servo.write(0);
  //myservo.write(90);
}

// the loop routine runs over and over again forever:
void loop() {
  
  //Sends data only when it is received
  if (Serial.available()>0){
    
    incoming_message_char=Serial.read();
    incoming_message = incoming_message_char - '0';
    Serial.print(incoming_message);
    
    if (incoming_message==1){ //Moves to the right
      //Serial.print("I'm about to wait");
      //delay(1000);
      horizontal_angle_track=horizontal_angle_track-horizontal_increment;
      horizontal_servo.write(horizontal_angle_track);
      //Serial.print ("I just moved the IR Sensor 1 unit to the right\r\n");
    }
    
    if (incoming_message==2){ //Moves to the left
      horizontal_angle_track=horizontal_angle_track+horizontal_increment;
      horizontal_servo.write(horizontal_angle_track);
      //Serial.print ("I just moved the IR Sensor 1 unit left\r\n");
    }

    if (incoming_message==3){ //Moves sensor all the way left
      //delay(500);
      horizontal_angle_track=90;
      horizontal_servo.write(horizontal_angle_track);
      //Serial.print ("I just moved the IR Sensor all the way to the left\r\n");
    }
    
    if (incoming_message==4){ //Moves sensor all the way left
      //delay(500);
      horizontal_angle_track=0;
      horizontal_servo.write(horizontal_angle_track);
      //Serial.print ("I just moved the IR Sensor all the way to the right\r\n");
    }


    if (incoming_message==5){
      //Print out the reading of the sensor
      int reading = analogRead(A5);
      Serial.println(reading);
      //delay(1000); 
    }
}
}
