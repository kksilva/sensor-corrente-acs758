const int sensorDeCorrente = A0;
const float sensibilidade = 0.0066;  

float offsetSensor = 0.0; 

void setup() {
  analogReadResolution(12);
  Serial.begin(115200);

  float soma = 0.0;
  for (int i = 0; i < 500; i++) {
    soma += analogRead(sensorDeCorrente);
  }
  float adcMedioOffset = soma / 500.0;
  offsetSensor = adcMedioOffset * 3.3 / 4095.0; 

  Serial.print("Offset calibrado: ");
  Serial.print(offsetSensor, 4);
  Serial.println(" V");
}

void loop() {
  float soma = 0.0;
  for (int i = 0; i < 100; i++) {
    soma += analogRead(sensorDeCorrente);
  }
  float adcMedio = soma / 100.0;
  float tensao = adcMedio * 3.3 / 4095.0;
  float corrente = (offsetSensor - tensao) / sensibilidade;

  Serial.print("ADC: ");
  Serial.print(adcMedio, 1);

  Serial.print("  Tensao: ");
  Serial.print(offsetSensor - tensao, 4);
  Serial.print(" V");

  Serial.print("  Corrente: ");
  Serial.print(corrente, 1);
  Serial.println(" A");

  delay(500);
}