#include <PubSubClient.h>
#include <ESP8266WiFi.h>

// 2 - wifi variables definition
char *ssid = "*******";
char *password = "********";

// mqtt variables definition
char *broker = "test.mosquitto.org"; 
int port = 1883;
char *CLIENT_ID = "node";

WiFiClient wificlient;
PubSubClient mqttClient(wificlient);


String payload;
char message[10];

int trigPin = D0;
int echoPin = D1;

long duration;
int distance;

void setupWifi()
{
  // 1 - ssid,password begin
  WiFi.begin(ssid,password);

  // 2 - connection establish loop
  while(WiFi.status()!= WL_CONNECTED){
    Serial.print(".");
    delay(500);
    }
  // 3 - connected message  , ip address
  Serial.println(WiFi.localIP());
  
}

void setupMqtt()
{
    mqttClient.setServer(broker,port);

    if(mqttClient.connect(CLIENT_ID)){
      mqttClient.publish("rajeev","SUCCESSFULLY CONNECTED");
      }
  
}


void setup()
{
  Serial.begin(9600);
  pinMode(trigPin,OUTPUT);
  pinMode(echoPin,INPUT);
  setupWifi();
  setupMqtt();
  
        
}

void loop()
{
  //to let the device settle for some time
  digitalWrite(trigPin,0);
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

  payload = "Dis-";payload+=String(distance);
  payload.toCharArray(message,10);

  if(mqttClient.connect(CLIENT_ID)){
      mqttClient.publish("rajeev",message);
      }
  
  delay(1000);
}  
