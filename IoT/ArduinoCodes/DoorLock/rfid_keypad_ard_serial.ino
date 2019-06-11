

/*

  Automated DoorLock Arduino code version 1.0

  version features : 
          

*/

// ***************** Libraries ********************* // 
#include <deprecated.h>
#include <MFRC522.h>
#include <MFRC522Extended.h>
#include <require_cpp11.h>                    //  MFRC522 LIBRARY FOR RFID MODULE

#include <Key.h>
#include <Keypad.h>                           // KEYPAD MODULE LIBRARY



// **********  VARIABLES & GLOBAL INTIALIZATIONS  ****** //

const byte ROWS = 4;                                                                // NUMBER OF ROWS IN KEYPAD
const byte COLS = 4;                                                                // NUMBER OF COLUMNS IN KEYPAD

char keypadKeys[ROWS][COLS] = {                                                     // VALUE DECLARATION FOR THE KEYS IN THE KEYPAD
      {'z','2','3','A'},
      {'y','5','6','B'},
      {'f','8','9','C'},
      {'*','0','#','D'}
  };
byte rowPins[ROWS] = {3,2,A5,A4};                                                   // INTIALISING ROW PINS
byte colPins[COLS] = {A3,A2,A1,A0};                                                 // INTIALISING COLUMN PINS      

Keypad otpPad = Keypad (makeKeymap(keypadKeys),rowPins,colPins,ROWS,COLS);          // KEYPAD MAPPING WITH THE VALUES AND PIN NUMBERS 


#define RST_PIN         9                                                           // RESET PIN
#define SS_PIN          10                                                          // SERIAL CLOCK
MFRC522 mfrc522(SS_PIN, RST_PIN);                                                   // MFRC VARIABLE INTIALISATION

String tagID_detected ;                                                             // VARIABLE TO STORE RFID TAG ID.

bool rfid_keypad = true;                                                            // true - ENABLE RFID, false - ENABLE KEYPAD

const int detectedLED   =  4; 
const int processLED    =  5;
const int accessLED     =  6;
const int deniedLED     =  7;

const int doorLockRelay =  8;

char pressedKey ;
String enteredOTP ;
String receivedOTP ;

  

String nodeMessage;


void dump_byte_array(byte *buffer, byte bufferSize)
{
  
  for (byte i = 0; i < bufferSize; i++)
  {
    //    Serial.print(buffer[i]);
    tagID_detected += buffer[i];

  }


  // -------------------------
 
  /*
   SEND THIS DETECTED TAG ID TO THE NODE MCU THROUGH SERIAL COMMUNICATION.

  */
  Serial.print(tagID_detected);
  delay(500);
  tagID_detected = "";
   
 
 //  --------------------------

  rfid_keypad = false;

  
}
void RfidScan()
{
//  Serial.println("SCANNING");
  if ( ! mfrc522.PICC_IsNewCardPresent())
    return;
  if ( ! mfrc522.PICC_ReadCardSerial())
    return;
  dump_byte_array(mfrc522.uid.uidByte, mfrc522.uid.size);
  if ( ! mfrc522.PICC_IsNewCardPresent())
    delay(5000);
}


void KeyPress(){
  pressedKey = otpPad.getKey();
  
  if (enteredOTP.length()<4){
    enteredOTP+=pressedKey;
    }
  else{
    enteredOTP = "";
    return;
    }  
  
  }



void setup() {
  
  Serial.begin(9600);                                                               // COMMUNICATION BETWEEN ARDUINO UNO AND NODE MCU AND PC

  SPI.begin();                                                                     // RFID TO UNO COMMUNICATION BEGIN
  mfrc522.PCD_Init();                                                              // RFID MODULE WILL START READING


}

void loop() {

  if (Serial.available() && rfid_keypad == false){
    nodeMessage = Serial.readString();

    if (nodeMessage != ""){
      // extract the otp received and store in the variable.
//      Serial.println(nodeMessage);
      receivedOTP = nodeMessage;
      }
    
    }

  if (enteredOTP.length() == 4){
    
    // compare entered OTP with received OTP and if equal open lock. 
    if (receivedOTP == enteredOTP){
    // TURN ON THE RELAY.
    digitalWrite(doorLockRelay,HIGH);
    delay(10000);
    // TURN OFF THE RELAY.
    digitalWrite(doorLockRelay,LOW);      
      }
    else{
      
      
      }  


      
    }


    
  if (rfid_keypad == true){
      RfidScan();  
    }
  else if (rfid_keypad == false){
      KeyPress();
    }  
  

  delay(500);





  
}
