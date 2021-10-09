int ledPin;
float voltage;
int val = 0;
int Vint;
int value;
int command;
int a;
String Comm;
String pin;
String v;
String analog;
bool isData = false;

void setup() {
  // put your setup code here, to run once:
   Serial.begin(57600); //sets baud rate of serial port as 57600
                       //make sure baud rate is the same on serial monitor & in NI Max
    while (!Serial); //waits until serial port is ready or else it will not move on
  Serial.flush();
  pinMode(ledPin, OUTPUT);  //sets pin as output
}

void loop() {
  // put your main code here, to run repeatedly:
  
  while (Serial.available() > 0){ //if there's something on the serial port, read it
    char value = Serial.read();
    Comm += value;
    
    if (value == '\n'){ //check if value we read is a specific character
      isData = true;
    }
   }

  if (isData){ //prints out command
    isData = false;
    command = 10; //sets command to 10
  

    if (Comm.startsWith("pin:")){command=1;} 
    if (Comm.startsWith("V:")){command=2;}
    if (Comm.startsWith("A:")){command=3;}
  
    switch (command){
      case 1: //sets pin
        pin = Comm.substring(4);
        ledPin = pin.toInt();
        //Serial.println(ledPin);
        break;

      case 2: //set voltage
        v = Comm.substring(2);
        Vint = v.toInt();
        analogWrite(ledPin, Vint);
        //Serial.println(Vint);
        break;
        
      case 3: //set analog channel
        analog = Comm.substring(2);
        a = analog.toInt();
        value = analogRead(a);
        voltage = value*(5.0/1023.0);
        Serial.println(voltage);
        break;

    }
 
    Comm="";
    
  }
}  


//void LED(int x, int y){
  //Serial.println(y);  //prints out the voltage to make sure the code is using the right one
  //analogWrite(x, y);   //(x = LED pin, y = voltage)
  //delay(200);
  //val = analogRead(3);
  //Serial.println(val); //prints value from A3 which is taking measurements between resistor and diode
  
//}
