void setup() {
  Serial.begin(9600);
  Serial.println("Serial communication started. Type something:");
}

void loop() {
  if (Serial.available() > 0) {
    String incomingData = Serial.readString();
    
    Serial.print("You entered: ");
    Serial.println(incomingData);
  }
}
