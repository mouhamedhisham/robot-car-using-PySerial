#define speedL 3
#define IN1 5
#define IN2 6
#define IN3 9
#define IN4 10
#define speedR 11
#define sensorL 2
#define sensorR 12

int sl = 0;
int sr = 0;
int speedleft = 53;
int speedright = 68;

void setup() {
  for(int i = 5; i <= 10; i++) {
    pinMode(i, OUTPUT);
  }
  pinMode(sensorR, INPUT);
  pinMode(sensorL, INPUT);
}

void forword() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(speedL, speedleft);
  analogWrite(speedR, speedright);
}

void backword() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(speedL, speedleft);
  analogWrite(speedR, speedright);
}

void left() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(speedL, 0);
  analogWrite(speedR, speedright);
}

void right() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(speedL, speedleft);
  analogWrite(speedR, 0);
}

void stopp() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(speedL, 0);
  analogWrite(speedR, 0);
}

void loop() {
  sl = digitalRead(sensorL);
  sr = digitalRead(sensorR);
  
  if (sl == 0 && sr == 0) {
    forword();
  } else if (sl == 0 && sr == 1) {
    right();
  } else if (sl == 1 && sr == 0) {
    left();
  } else if (sl == 1 && sr == 1) {
    stopp();
  }
}