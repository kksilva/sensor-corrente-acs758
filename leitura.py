import serial
import time

sensibilidade = 0.0066

offsetSensor = 0.0

ser = serial.Serial("/dev/ttyACM0", 115200, timeout=3)
time.sleep(2)
ser.reset_input_buffer()

nome = input("Nome do arquivo CSV (ex.: serieA_vazio.csv): ")
arquivo = open(nome, "x")  # "x" nao sobrescreve: da erro se o arquivo ja existir
arquivo.write("adc;tensao_v;corrente_a\n")

# setup
soma = 0.0
for i in range(500):
    linha = ""
    while "ADC:" not in linha:
        linha = ser.readline().decode(errors="replace")
    soma += float(linha.split("ADC:")[1].split()[0])
adcMedioOffset = soma / 500.0
offsetSensor = adcMedioOffset * 3.3 / 4095.0

print("Offset calibrado: " + str(round(offsetSensor, 4)) + " V")

# loop
while True:
    soma = 0.0
    for i in range(100):
        linha = ""
        while "ADC:" not in linha:
            linha = ser.readline().decode(errors="replace")
        soma += float(linha.split("ADC:")[1].split()[0])
    adcMedio = soma / 100.0
    tensao = adcMedio * 3.3 / 4095.0
    corrente = (tensao - offsetSensor) / sensibilidade

    print("ADC: " + str(round(adcMedio, 1))
          + "  Tensao: " + str(round(tensao - offsetSensor, 4)) + " V"
          + "  Corrente: " + str(round(corrente, 1)) + " A")

    arquivo.write(str(round(adcMedio, 1)) + ";"
                  + str(round(tensao - offsetSensor, 4)) + ";"
                  + str(round(corrente, 1)) + "\n")
    arquivo.flush()

    time.sleep(0.5)
