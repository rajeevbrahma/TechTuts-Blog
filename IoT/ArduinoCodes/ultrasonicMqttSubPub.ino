#include <PubSubClient.h>
#include <ESP8266WiFi.h>


// 2 - wifi variables definition
char *ssid = "*******";
char *password = "******";

// mqtt variables definition
char *broker = "test.mosquitto.org";
int port = 1883;
char *CLIENT_ID = "node";
char *PUB_TOPIC = "ece-pub";
char *SUB_TOPIC = "ece-sub";


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
  WiFi.begin(ssid, password);

  // 2 - connection establish loop
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  // 3 - connected message  , ip address
  Serial.println(WiFi.localIP());

}


void reConnect()
{

  while (!mqttConnect.connected())
  {
    Serial.print(".");
    delay(500);
    mqttClient.connect(CLIENT_ID);

  }

  Serial.println("RECONNECTED");
  mqttClient.subscribe(SUB_TOPIC);

}



void distanceMesurement()
{
  //to let the device settle for some time
  digitalWrite(trigPin, 0);
  delayMicroseconds(2);

  // trigger process
  digitalWrite(trigPin, 1);
  delayMicroseconds(10);
  digitalWrite(echoPin, 0);

  // listening process
  duration = pulseIn(echoPin, HIGH);
  distance = (0.033 * duration) / 2;

  Serial.print("DISTANCE - ");
  Serial.println(distance);

  payload = "Dis-"; payload += String(distance);
  payload.toCharArray(message, 10);


}

void sendMessage()
{
  if (mqttClient.connect(CLIENT_ID))
  {
    mqttClient.publish(PUB_TOPIC, message);
  }
}

void callback(char* topic, byte *payload, unsigned int length)
{
  if ((char)payload[0] == '1')
  {
    distanceMeasurement();
    sendMessage();
  }

}
void setupMqtt()
{
  mqttClient.setServer(broker, port);

  mqttClient.subscribe(SUB_TOPIC);
  mqttClient.setCallback(callback);

  if (mqttClient.connect(CLIENT_ID)) {
    mqttClient.publish(PUB_TOPIC, "SUCCESSFULLY CONNECTED");
  }

}


void setup()
{
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  setupWifi();
  setupMqtt();


}

void loop()
{

  if (mqttClient.connected()) {
    mqttClient.loop()
  }
  else {
    reConnect();
  }



  delay(1000);
}
