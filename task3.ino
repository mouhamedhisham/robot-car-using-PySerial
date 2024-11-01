#define laserPin 8
int laserState = LOW;
#define speedL 3
#define IN1 5
#define IN2 6
#define IN3 9
#define IN4 10
#define speedR 11

void setup() {
  Serial.begin(9600);
  pinMode(laserPin, OUTPUT);
  for (int i = 5; i <= 10; i++) {
    pinMode(i, OUTPUT);
  }
}

void laser() {
  if(laserState == HIGH) {
    digitalWrite(laserPin, LOW);
    laserState = LOW;
  } else {
    digitalWrite(laserPin, HIGH);
    laserState = HIGH;
  }
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
  if (Serial.available() > 0) {
    char command = Serial.read();  // Read the incoming character

    if (command == 'F') {  // Forward
      forward();
    } else if (command == 'B') {  // Backward
      backward();
    } else if (command == 'L') {  // Left
      left();
    } else if (command == 'R') {  // Right
      right();
    } else if (command == 'S') {  // Stop
      stop();
    } else if (command == 'E') {  // Lasser
      laser();
    }
  }
}
