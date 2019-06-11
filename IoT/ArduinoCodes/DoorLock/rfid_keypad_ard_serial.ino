#include <SPI.h>
#include <MFRC522.h>
#include <Key.h>
#include <Keypad.h>

#include <SoftwareSerial.h>
SoftwareSerial soft_serial(6, 5);

#define RST_PIN         9
#define SS_PIN          10
MFRC522 mfrc522(SS_PIN, RST_PIN);

const byte ROWS = 4; //four rows
const byte COLS = 4; //three columns

bool keypadEnable = false; //
bool rfidEnable = true; //

String passwordActual = "";
String passwordTyped = "";
String rfidTagID_Detected = "";
String rfidTagID_Recieved = "";
bool gotComma = false;


int tempStringLength;
char tempBuf[100];
String tempStr;


char key;

char keys[ROWS][COLS] = {

  {'1', '2', '3', 'A'},

  {'4', '5', '6', 'B' },

  {'7', '8', '9', 'C'},

  {'*', '0', '#', 'D'}

};

byte rowPins[ROWS] = {3, 2, A5, A4}; //connect to the row pinouts of the keypad
byte colPins[COLS] = {A3, A2, A1, A0}; //connect to the column pinouts of the keypad

Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

void setup()
{
  Serial.begin(9600);
  soft_serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
}

void loop()
{

  if (rfidEnable == true)
  {
    RfidScan();
    Serial.println("RFID SCANNING....");
  }

  else
  {

    if (soft_serial.available() > 0)
    {

      String node_return = soft_serial.readString();
      
      if (node_return != "") {
        Serial.print("Serial Received from Node mcu --- ");
        Serial.println(node_return);
        
          if (node_return[0] == '0')
          {
            Serial.println(node_return);
        
            tempStr = "rfidalert";
            tempStringLength = tempStr.length() + 1;
            tempStr.toCharArray(tempBuf, tempStringLength);
            soft_serial.write(tempBuf, tempStringLength);
          }
          else
          {
            keypadEnable = true;
            Serial.println("KEYPAD ENABLED..");
            for (int j = 0; j < node_return.length(); j++) {

             Serial.println(node_return[j]);
             Serial.println((char)node_return[j]);
              if (node_return[j] == ',') {
                gotComma = true;
              }
              else if (node_return[j] != ',' && gotComma == false) {
                rfidTagID_Recieved += node_return[j];
              }
              else if (node_return[j] != ',' && gotComma == true) {
                passwordActual += node_return[j];
              }
            }
            gotComma = false;
          }

          Serial.print("PASSWORD ACTUAL - ");Serial.print(passwordActual); 
          
      }


    }





  }

  key = keypad.getKey();

  if (key != NO_KEY && keypadEnable == true && rfidEnable == false)
  {
    if (passwordTyped.length() <= 3)
    {
      passwordTyped += key;
     
    }
    else{
      keypadEnable = false;
      Serial.print("KEYPAD DISABLED..");
      }

     Serial.print(passwordTyped);
     Serial.print(passwordTyped.length());
  }
  
  if (keypadEnable == true && rfidEnable == false && passwordTyped.length() == 3)
  {
    if (passwordTyped == passwordActual)
    {
      // turn on the relay to open the door
      keypadEnable == false;
      rfidEnable == true;
      passwordTyped = "";
      Serial.println("OPEN THE DOOR");

    }
    else
    {
      tempStr = "passwordincorrect";
      tempStringLength = tempStr.length() + 1;
      tempStr.toCharArray(tempBuf, tempStringLength);
      soft_serial.write(tempBuf, tempStringLength);

      keypadEnable == false;
      rfidEnable == true;
      passwordTyped = "";

      Serial.println("PASSWORD INCORRECT,SCANNING AGAIN");


    }
  }

}

void dump_byte_array(byte *buffer, byte bufferSize)
{
  Serial.print("TAG ID is .....");
  for (byte i = 0; i < bufferSize; i++)
  {
    //    Serial.print(buffer[i]);
    rfidTagID_Detected += (buffer[i]);

  }

  Serial.print(rfidTagID_Detected);

  tempStr = String(rfidTagID_Detected);
  tempStringLength = tempStr.length() + 1;
  tempStr.toCharArray(tempBuf, tempStringLength);
  soft_serial.write(tempBuf, tempStringLength);

  rfidEnable = false; // switching the device into enter password mode

}

void RfidScan()
{
  if ( ! mfrc522.PICC_IsNewCardPresent())
    return;
  if ( ! mfrc522.PICC_ReadCardSerial())
    return;
  dump_byte_array(mfrc522.uid.uidByte, mfrc522.uid.size);
  if ( ! mfrc522.PICC_IsNewCardPresent())
    delay(5000);
}


