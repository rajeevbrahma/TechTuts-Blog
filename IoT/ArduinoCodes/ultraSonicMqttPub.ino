#include <PubSubClient.h>                             // Library for MQTT connection
#include <ESP8266WiFi.h>                              // WiFi connection Library

// 2 - wifi variables definition
char *ssid = "*******";                               // wifi username
char *password = "********";                          // wifi password

// mqtt variables definition
char *broker = "test.mosquitto.org";                  // MQTT Broker URL
int port = 1883;                                      // MQTT Broker port
char *CLIENT_ID = "node";                             // NODE MCU client name (our choice of string)

WiFiClient wificlient;                                // Initialising the wificlient variable (will be used for the mqtt connection)
PubSubClient mqttClient(wificlient);                  // Initialising the mqttclient variable


String payload;                                       // String variable to store the message to be sent
char message[10];                                     // character array variable to store the message to be sent
                                                      // since mqtt publish command accepts only the character array
                                                      // we have to convert our message to character array

int trigPin = D0;
int echoPin = D1;

long duration;
int distance;

// ******** FUNCTION TO SETUP WIFI CONNECTION ********** //
void setupWifi()
{
  // 1 - ssid,password begin
  WiFi.begin(ssid,password);

  // 2 - connection establish loop
  // This while condition will not get terminated until and unless we have the successful internet connection
  while(WiFi.status()!= WL_CONNECTED){
    Serial.print(".");
    delay(500);
    }
  // 3 - connected message  , ip address
  Serial.println(WiFi.localIP());
  
}

// ****** FUNCTION TO SETUP MQTT CONNECTION ****** //
void setupMqtt()
{
    // STEP 1 : just giving the information about the broker we are getting connected to
    mqttClient.setServer(broker,port);

    // STEP 2 : connecting to the broker and sending a message if we get a successful connection.
    if(mqttClient.connect(CLIENT_ID)){
      
      // command to publish message
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
  digitalWrite(trigPin,0);

  // listening process
  duration = pulseIn(echoPin,HIGH);
  distance = (0.033*duration)/2;

  Serial.print("DISTANCE - ");
  Serial.println(distance);

    
  payload = "Dis-";
  
  // converting our integer type distance value to a string in order to convert it to character array.
  payload+=String(distance);
  
  // character array conversion line.
  payload.toCharArray(message,10);

  // publishing the distance message after checking for the connection status.
  if(mqttClient.connect(CLIENT_ID)){
      mqttClient.publish("rajeev",message);
      }
  
  delay(1000);
}  
