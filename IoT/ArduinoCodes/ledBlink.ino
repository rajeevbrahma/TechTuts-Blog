int led = D0;
  
void setup() {
  // put your setup code here, to run once:

  // Begin the serial communication.
  Serial.begin(9600);
  pinMode(led,OUTPUT);

  
} 

void loop() {
  // put your main code here, to run repeatedly:
 
  digitalWrite(led,1);
  Serial.println("ON");
  delay(1000);
  digitalWrite(led,0);
  Serial.println("OFF");
  delay(1000);
}
