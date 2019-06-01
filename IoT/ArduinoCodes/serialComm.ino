  
void setup() {
  // put your setup code here, to run once:

  // Begin the serial communication.
  Serial.begin(9600);
  
  
} 

void loop() {
  // put your main code here, to run repeatedly:
  
  // Message to PC
  Serial.println("Hello world");
  delay(1000);

}
