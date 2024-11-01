#define speedL 3
#define IN1 5
#define IN2 6
#define IN3 9
#define IN4 10
#define speedR 11
#define buzzer 7


void setup() {
  for (int i = 5; i <= 10; i++) {
    pinMode(i, OUTPUT);
  }
  pinMode(buzzer,OUTPUT);
  Serial.begin(9600);  // Start serial communication
}


void forward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(speedL, 65);
  analogWrite(speedR, 80);
}

void backward() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(speedL, 65);
  analogWrite(speedR, 80);
}

void left() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(speedL, 0);
  analogWrite(speedR, 70);
}

void right() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(speedL, 55);
  analogWrite(speedR, 0);
}

void stop() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(speedL, 0);
  analogWrite(speedR, 0);
}

void loop() {
  if (Serial.available()) {
    char sign = Serial.read();  // Read a single character
    Serial.println(sign);  // Print the received character for debugging

    if (sign == 'F') {  // 'F' for forward
      forward();
    } else if (sign == 'B') {  
    digitalWrite(buzzer, HIGH);
    delay(1000);
    digitalWrite(buzzer, LOW);
    }else if (sign == 'S') {  // 'S' for stop
      backward();
      
    }
  }
}
