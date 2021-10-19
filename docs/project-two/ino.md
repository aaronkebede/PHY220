# Documentation for the Arduino Drive
First, we initialize variables that we will be using in the code as follows:

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

 - We then set the pinMode which configures the variable as an input or 
   output. In our case, it is an output because we  want it to be in a
   state of low-impedance so that it can provide a good amount of
   current to outside circuits.
   
 - Another constant that we will set is the baud rate. The baud rate basically specifies the amount of data that is transferred in a second. Here, we should make sure that is has the same value on our code and on the arduino instrument setting. 
 
 - We then specify a condition of start. To wait until the serial port is ready. 
 
 Here's the code that does that( ***It is important that the baud rate be the same on the serial monitor, NI Max and our setup***)
 
     void setup() {
          pinMode(ledPin, OUTPUT);  
          Serial.begin(57600);       
          while (!Serial)
          Serial.flush();
        }
On the next part of the code, we configure the board so that it reads an input if there is an input on the serial port. To make things easier, we setup our code so that with every input, a new line string is added at the end. This makes it easier for our code to communicate with LabVIEW.

    while (Serial.available() > 0) { 
        char value = Serial.read();
        Comm += value;
        if (value == '\n'){ 
              isData = true;
              }
       }
Then, we set commands on the board to configure it what to do with specific inputs. We set three commands that set the analog channel, set the voltage, and read output voltage.

If we have an invalid input(something we have not set as recognizable by the program), we have to have a condition for an error output. This makes sure that we understand our output if we encounter error(s) on execution of the arduino code or when using the program with LabVIEW.

 

      if (isData){
           isData = false;
            command = 10;             
We set command to set analog channel(pin), set voltage and read output respectively.
      
        if (Comm.substring(0,4)=="pin:"){command=1;}  
        if (Comm.substring(0,2)=="V:"){command=2;}   
        if (Comm.substring(0,2)=="A:"){command=3;}  
We set the conditions for the command along with  some output to understand what is happening.
**analogWrite** writes an analog value to a pin(*happens on case 2*) - useful to set a value, in our case voltage on the circuit.

 **analogRead** reads analog value from a specified pin(*happens in case 3*) - useful to read a value from a specified channel.
      
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

The last part delays the execution of the program for a specified time. We had to have delay the program because we were encountering time issues with the LabVIEW program that we had, having a delay on the execution seemed to avoid errors.

    }
       Comm="";
       delay(20);
    }  

     

 
    
  



     




