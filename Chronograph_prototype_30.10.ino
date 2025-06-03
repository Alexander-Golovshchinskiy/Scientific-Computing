

int baseline[2];
int readings1[3];
int readings2[3];
int sum1 = 0;
int sum2 = 0;
int start = 0;
int end = 0;
bool timing = false;
unsigned long startTime;
unsigned long endTime;
unsigned long elapsedTime;
float speed;

void setup() {
  // put your setup code here, to run once:
  //initialising and averaging for baseline
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  Serial.begin(9600);
  Serial.println("Calibration Started");
    for (int i = 0; i < 3; i++){
      readings1[i] = analogRead(A0);
      delay(1000);
      sum1 += readings1[i];
  }
    for (int i = 0; i < 3; i++){
      readings2[i] = analogRead(A1);
      delay(1000);
      sum2 += readings2[i];
  }
  baseline[0] = sum1 / 3;
  baseline[1] = sum2 / 3;
  for (int i = 0; i < 2; i++){
    Serial.print("Baseline "+String(i)+": ");
    Serial.println(baseline[i]);
  }

}

void loop() {
  // put your main code here, to run repeatedly:

  //detecting
  start = analogRead(A0);
  end = analogRead(A1);
  if (start < baseline[0] * 0.7){
    startTime = millis();
    timing = true;
    Serial.println("Start detected");
  }
  if (timing && end < baseline[1] * 0.7){
    endTime = millis();
    elapsedTime = endTime - startTime;
    Serial.print("Elapsed time: ");
    Serial.print(elapsedTime);
    Serial.println(" m/s");

    // calculations assumig 8cm distance travelled
    speed = (8.0/100.0)/(float(elapsedTime)/1000.0);
    Serial.print("Speed of the bullet: ");
    Serial.print(speed, 6);
    Serial.println(" ms");
    timing = false;
  }
}
