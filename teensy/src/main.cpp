#include <Arduino.h>
#include <SD.h>
#include <SPI.h>

#define SD_CS 10 // Teensy Audio Shield uses pin 10 for SD card
#define RX_PIN 0 // Teensy RX1 (UART1)
#define TX_PIN 1 // Teensy TX1 (UART1)

File wavFile;
bool recording = false;

void setup() {
  Serial1.begin(115200); // UART1
  Serial.begin(115200);  // Debugging
  if (!SD.begin(SD_CS)) {
    Serial.println("SD Card initialization failed!");
    return;
  }
}

void loop() {
  static char buffer[512];
  static int index = 0;

  while (Serial1.available()) {
    char c = Serial1.read();

    if (!recording && c == 'S') { // Look for START signal
      if (Serial1.read() == 'T') {
        wavFile = SD.open("received.wav", FILE_WRITE);
        if (!wavFile) {
          Serial.println("Failed to open file");
          return;
        }
        recording = true;
        index = 0;
        Serial.println("Receiving...");
      }
    } else if (recording && c == 'E') { // Look for END signal
      if (Serial1.read() == 'N') {
        wavFile.close();
        recording = false;
        Serial.println("File received!");
      }
    } else if (recording) { // Store data
      buffer[index++] = c;
      if (index >= sizeof(buffer)) {
        wavFile.write((uint8_t *)buffer, index);
        index = 0;
      }
    }
  }
}
