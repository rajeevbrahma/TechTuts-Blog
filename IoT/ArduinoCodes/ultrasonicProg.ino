/*
  ULTRASONIC SENSOR WITH NODE MCU
*/

int trigPin = D0;
int echoPin = D1;

long duration;
int distance;
void setup()
{
  Serial.begin(9600);
  pinMode(trigPin,OUTPUT);
  pinMode(echoPin,INPUT);
        
}

void loop()
{
  //to let the device settle for some time
  digitalWrite(trigPin,1);
  delayMicroseconds(2);
  
  // trigger process
  digitalWrite(trigPin,1);
  delayMicroseconds(10);
  digitalWrite(echoPin,0);

  // listening process
  duration = pulseIn(echoPin,HIGH);
  distance = (0.033*duration)/2;

  Serial.print("DISTANCE - ");
  Serial.println(distance);

}  
