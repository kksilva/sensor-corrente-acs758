#!/usr/bin/env python3
"""Le a saida serial do Arduino Due e imprime exatamente o que o .ino envia.

Equivale ao Monitor Serial da IDE. Pressione Ctrl+C para encerrar.
"""

import serial

PORTA = "/dev/ttyACM0"
BAUD = 115200

ser = serial.Serial(PORTA, BAUD, timeout=3)

try:
    while True:
        linha = ser.readline().decode(errors="replace").strip()
        if linha:
            print(linha, flush=True)
except KeyboardInterrupt:
    pass
finally:
    ser.close()
