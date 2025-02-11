#include <Wire.h>

/*
* Code für den Arduino des Project GreenPi für den Infotag der Bertha-Benz-Schule Sigmaringen
* geschrieben von Esad Sahin der Klasse EKIT 2025
*/

void setup() {
  Wire.begin(0x08); // Arduino als I2C-Slave mit der Adresse 0x08 setzen
  Wire.onRequest(requestEvent); // Definiert was auf Datenanfrage passiert
}

void loop() {
  // Nichts hier. Daten werden nur auf Anfrage des Pis gesendet
}

void requestEvent() {
  int val1 = analogRead(A1) / 4; // X-Achse des ersten Joysticks
  int val2 = analogRead(A2) / 4; // Y-Achse des ersten Joysticks

  int val3 = analogRead(A3) / 4; // X-Achse des zweiten Joysticks
  int val4 = analogRead(A4) / 4; // Y-Achse des zweiten Joysticks

  // Die Werte weitergeben
  Wire.write(val1); 
  Wire.write(val2); 
  Wire.write(val3); 
  Wire.write(val4);  
}
