// Feather9x_RX
// -*- mode: C++ -*-
// Example sketch showing how to create a simple messaging client (receiver)
// with the RH_RF95 class. RH_RF95 class does not provide for addressing or
// reliability, so you should only use RH_RF95 if you do not need the higher
// level messaging abilities.
// It is designed to work with the other example Feather9x_TX

#include <SPI.h>
#include <RH_RF95.h>

// for feather m0 RFM9x
#define RFM95_CS 8
#define RFM95_RST 4
#define RFM95_INT 3

//#if defined(ESP8266)
//  /* for ESP w/featherwing */ 
//  #define RFM95_CS  2    // "E"
//  #define RFM95_RST 16   // "D"
//  #define RFM95_INT 15   // "B"
//
//#elif defined(ESP32)  
//  /* ESP32 feather w/wing */
//  #define RFM95_RST     27   // "A"
//  #define RFM95_CS      33   // "B"
//  #define RFM95_INT     12   //  next to A
//
//#elif defined(NRF52)  
//  /* nRF52832 feather w/wing */
//  #define RFM95_RST     7   // "A"
//  #define RFM95_CS      11   // "B"
//  #define RFM95_INT     31   // "C"
//  
//#elif defined(TEENSYDUINO)
//  /* Teensy 3.x w/wing */
//  #define RFM95_RST     9   // "A"
//  #define RFM95_CS      10   // "B"
//  #define RFM95_INT     4    // "C"
//#endif


// Change to 434.0 or other frequency, must match RX's freq!
#define RF95_FREQ 434.0

// Singleton instance of the radio driver
RH_RF95 rf95(RFM95_CS, RFM95_INT);

// Blinky on receipt
#define LED 13

void setup()
{
  pinMode(LED, OUTPUT);
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);

  Serial.begin(115200);
  while (!Serial) {
    delay(1);
  }
  delay(100);

  Serial.println("Feather LoRa RX Test!");

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

  // Defaults after init are 434.0MHz, modulation GFSK_Rb250Fd250, +13dbM
  if (!rf95.setFrequency(RF95_FREQ)) {
    Serial.println("setFrequency failed");
    while (1);
  }
  Serial.print("Set Freq to: "); Serial.println(RF95_FREQ);
  rf95.setTxPower(23, false);
}

int16_t packetnum = 0;

void loop()
{
  if (rf95.available())
  {
    uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
    uint8_t len = sizeof(buf);

    if (rf95.recv(buf, &len))
    {
      digitalWrite(LED, HIGH);
      Serial.print("Got: ");
      Serial.println((char*)buf);
       Serial.print("RSSI: ");
      Serial.println(rf95.lastRssi(), DEC);
      packetnum++;
    }
    else
    {
      Serial.println("Receive failed");
    }
    if(packetnum==30)
    {
      Serial.println("Completed!!");
      while(1);
    }
  }
}
