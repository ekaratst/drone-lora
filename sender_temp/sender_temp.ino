#include <SPI.h>
#include <RH_RF95.h>
#include "DHT.h"
#include <avr/dtostrf.h>

// for feather m0  
#define RFM95_CS 8
#define RFM95_RST 4
#define RFM95_INT 3

#define RF95_FREQ 434.0

#define DHTPIN 5
#define DHTTYPE DHT22

RH_RF95 rf95(RFM95_CS, RFM95_INT);
DHT dht(DHTPIN, DHTTYPE);

void setup() 
{
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);

  delay(100);
  dht.begin();
  Serial.println("Feather LoRa TX Test!");

  // manual reset
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);

  while (!rf95.init()) {
    Serial.println("LoRa radio init failed");
    while (1);
  }
  Serial.println("LoRa radio init OK!");

  if (!rf95.setFrequency(RF95_FREQ)) {
    Serial.println("setFrequency failed");
    while (1);
  }
  Serial.print("Set Freq to: "); Serial.println(RF95_FREQ);
  rf95.setTxPower(23, false);
}

int16_t packetnum = 1;  

void loop()
{
  char tstr[5];
  char hstr[5];
  
  delay(2000); 
   
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if (isnan(h) || isnan(t)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }
  dtostrf(h, 5, 2, hstr);
  dtostrf(t, 5, 2, tstr);
  
  char radiopacket[50] = "Humidity: 74.90%  Temperature: 29.60°C  #   ";
  
  radiopacket[10] = hstr[0];
  radiopacket[11] = hstr[1];
  radiopacket[13] = hstr[3];
  radiopacket[14] = hstr[4];

  radiopacket[31] = tstr[0];
  radiopacket[32] = tstr[1];
  radiopacket[34] = tstr[3];
  radiopacket[35] = tstr[4];
    
  itoa(packetnum, radiopacket+42, 10);
  Serial.print("Messages -> "); Serial.println(radiopacket);
  
  Serial.println("Sending...");
  delay(10);
  rf95.send((uint8_t *)radiopacket, 50);
 
  delay(10);
  rf95.waitPacketSent();
 
  if(packetnum==30)
  {
    packetnum = 0;
  }
  packetnum++;
}
