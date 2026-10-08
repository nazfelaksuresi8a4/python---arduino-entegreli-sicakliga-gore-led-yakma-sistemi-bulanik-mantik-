#include <DHT.h>

#define DHTPIN 3
#define DHTTYPE DHT11


DHT dht(DHTPIN,DHTTYPE);

int d0 = 7;
int d1 = 8;
int d2 = 9;

void setup(){
  Serial.begin(9600);
  dht.begin();

  pinMode(d0,OUTPUT);
  pinMode(d1,OUTPUT);
  pinMode(d2,OUTPUT);
}

void loop(){
  delay(100);
  
  float f = dht.readTemperature();
  Serial.println(f);

  if (Serial.available() > 0 ){
    int dig = Serial.readStringUntil('\n').toInt();

    if (dig == 1){
      digitalWrite(d0,HIGH);
      digitalWrite(d1,LOW);
      digitalWrite(d2,LOW);
    }

    else if (dig == 2){
      digitalWrite(d0,LOW);
      digitalWrite(d1,HIGH);
      digitalWrite(d2,LOW);
    }

    else if (dig == 3){
      digitalWrite(d0,LOW);
      digitalWrite(d1,LOW);
      digitalWrite(d2,HIGH);
    }

    else{
      digitalWrite(d0,LOW);
      digitalWrite(d1,LOW);
      digitalWrite(d2,LOW);
    }


  }
}
