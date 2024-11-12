const int ledPins[] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11};  
const int numLeds = 10; 

void setup() {
  for (int i = 0; i < numLeds; i++) {
    pinMode(ledPins[i], OUTPUT);  
  }
}



void pattern1() {
  for (int i = 0; i < numLeds; i++) {
    digitalWrite(ledPins[i], HIGH);  
    delay(200);                     
    digitalWrite(ledPins[i], LOW);  
  }
}






void pattern2() {
  for (int i = numLeds - 1; i >= 0; i--) {
    digitalWrite(ledPins[i], HIGH); 
    delay(200);                      
    digitalWrite(ledPins[i], LOW);   
  }
}






void loop() {
  pattern1();  
  delay(1000); 

  pattern2();  
  delay(1000); 
}