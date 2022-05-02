
int data;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); //initialize serial COM at 9600 baudrate
  pinMode(13, OUTPUT); //make the LED pin (13) as output
  digitalWrite (13, LOW);
  Serial.println("Hello");
}

void loop() {
  // put your main code here, to run repeatedly:
 if (Serial.available()> 0)
  {
    data = Serial.read();
  }
   if (data == '1')
    {
    digitalWrite (13, HIGH);
    Serial.println(digitalRead(13));
    data = '2';
    }
   else if (data == '0')
    {
    digitalWrite (13, LOW);
    Serial.println(digitalRead(13));
    data = '2';
    }
}
