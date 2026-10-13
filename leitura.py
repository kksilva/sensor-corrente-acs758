#!/usr/bin/env python3
"""Replica no PC exatamente a logica do sketch Sensor_de_Corrente_ACS758.ino.

Requisito: o .ino ja deve estar gravado e rodando no Due (ele envia as
leituras pela serial a cada 500 ms).

O que este script faz, igual ao .ino:
  1. setup(): media das leituras com o motor desligado -> offset (V);
  2. loop(): para cada leitura, converte ADC -> tensao e calcula
     corrente = (tensao - offset) / 0.0066;
  3. imprime no mesmo formato do Monitor Serial:
     "ADC: ...  Tensao: ... V  Corrente: ... A"

Pressione Ctrl+C para encerrar.
"""

import sys
import time

import serial

PORTA = "/dev/ttyACM0"
BAUD = 115200
SENSIBILIDADE = 0.0066  # V/A
N_CALIB = 20  # 20 linhas x 100 amostras embarcadas = 2000 amostras (~10 s)


def ler_adc(ser):
    """Le uma linha da serial e extrai o valor bruto do ADC."""
    while True:
        linha = ser.readline().decode(errors="replace")
        if "ADC:" in linha:
            return float(linha.split("ADC:")[1].split()[0])


print("Conectando na porta", PORTA, file=sys.stderr)
ser = serial.Serial(PORTA, BAUD, timeout=3)
time.sleep(2)  # aguarda o reset da placa
ser.reset_input_buffer()

# ---- setup(): calibracao do offset (motor desligado) ----
print("Calibrando offset... mantenha o motor DESLIGADO.", file=sys.stderr)
soma = sum(ler_adc(ser) for _ in range(N_CALIB))
offset = (soma / N_CALIB) * 3.3 / 4095.0
print(f"Offset calibrado: {offset:.4f} V", file=sys.stderr)

# ---- loop(): mesmas contas e mesmo formato do .ino ----
try:
    while True:
        adc = ler_adc(ser)
        tensao = adc * 3.3 / 4095.0
        corrente = (tensao - offset) / SENSIBILIDADE
        print(
            f"ADC: {adc:.1f}  Tensao: {tensao - offset:.4f} V"
            f"  Corrente: {corrente:.1f} A",
            flush=True,
        )
except KeyboardInterrupt:
    pass
finally:
    ser.close()
