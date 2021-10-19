//initializes variables
int ledPin;
float voltage;
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
  pinMode(ledPin, OUTPUT);    //sets pin as output
  Serial.begin(57600);       //sets baud rate of serial port as 57600
                              //make sure baud rate is the same on serial monitor & in NI Max
   
  while (!Serial);          //waits until serial port is ready or else it will not move on
  
  Serial.flush();
  
}

void loop() {
 
  while (Serial.available() > 0){ //if there's something on the serial port, read it
    char value = Serial.read();
    Comm += value;
    
    if (value == '\n'){           //check if value we read is a specific character
      isData = true;
    }
   }

  if (isData){
    isData = false;
    command = 10; //sets command to 10
  
    if (Comm.substring(0,4)=="pin:"){command=1;}  //command for setting pin
    if (Comm.substring(0,2)=="V:"){command=2;}    //command for setting voltage
    if (Comm.substring(0,2)=="A:"){command=3;}    //command for reading voltage on channel
  
    switch (command){
      case 1: //sets pin
        pin = Comm.substring(4);      //pin is the number after the command "pin:"
        ledPin = pin.toInt();   //converts pin string value to integer
        Serial.println("Congrats, you set the pin"); 
        break;

      case 2: //set voltage
        v = Comm.substring(2);        //value that determines voltage is the number after "V:"
        Vint = v.toInt();             
        analogWrite(ledPin, Vint);    //writes voltage to LED pin determined in the previous command
        Serial.println("Congrats, you set the voltage");
        break;
        
      case 3: //set analog channel
        analog = Comm.substring(2);   //analog channel is value after "A:"
        a = analog.toInt();           
        value = analogRead(a);        //sets value as that read from analog channel 
        voltage = value*(5.0/1023.0); //calculates voltage in Voltz
        Serial.println(voltage);      //prints voltage
        break;
       case 10: //set analog channel
        Serial.println("invalid");      //prints voltage
        break;

    }
 
   
  }
   Comm="";
   delay(20);
}  
