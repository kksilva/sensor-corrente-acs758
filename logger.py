#!/usr/bin/env python3
"""Registrador serial do sensor ACS758 -> CSV.

Uso:
    python3 logger.py --porta /dev/ttyACM0 --saida ensaio_serieA.csv

Durante o ensaio, pressione ENTER no terminal para marcar um degrau/evento
(ex.: mudanca de PWM). A marca fica gravada no CSV com a corrente atual.
Ctrl+C encerra e fecha o arquivo.
"""

import argparse
import csv
import datetime
import re
import sys
import time

import serial

PADRAO = re.compile(
    r"ADC:\s*([\d.]+)\s+Tensao:\s*([\d.-]+)\s*V\s+Corrente:\s*([\d.-]+)\s*A"
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--porta", default="/dev/ttyACM0")
    ap.add_argument("--baud", type=int, default=115200)
    ap.add_argument("--saida", required=True)
    args = ap.parse_args()

    ser = serial.Serial(args.porta, args.baud, timeout=2)
    time.sleep(2)  # aguarda reset da placa
    ser.reset_input_buffer()

    t0 = time.time()
    with open(args.saida, "w", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["t_s", "adc", "tensao_v", "corrente_a", "marcador"])
        f.flush()
        print(f"Gravando em {args.saida}. ENTER=marca degrau, Ctrl+C=encerra.")
        try:
            while True:
                linha = ser.readline().decode(errors="replace").strip()
                m = PADRAO.search(linha)
                if not m:
                    continue
                adc, tensao, corrente = m.groups()
                marcador = ""
                # marca de degrau sem bloquear a leitura serial
                if sys.stdin.isatty():
                    import select

                    if select.select([sys.stdin], [], [], 0)[0]:
                        sys.stdin.readline()
                        try:
                            marcador = input(
                                "Descricao do degrau (ex.: PWM=40%): "
                            ).strip()
                        except EOFError:
                            pass
                w.writerow(
                    [f"{time.time() - t0:.2f}", adc, tensao, corrente, marcador]
                )
                f.flush()
                print(f"{time.time() - t0:8.1f}s  I = {corrente} A   {marcador}")
        except KeyboardInterrupt:
            print("\nEncerrado.")
        finally:
            ser.close()


if __name__ == "__main__":
    main()
