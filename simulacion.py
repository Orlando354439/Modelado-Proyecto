import logging
from typing import Tuple
from math import factorial, log
from datetime import datetime
import time
import random
from tabulate import tabulate
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import os
# Configuración básica del logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


app = FastAPI(
    tittle = "Simulación de un sistema de atencion a clientes"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def tiempo_entre_llegadas(num_llegadas):
    """Calcula el tiempo entre llegadas usando el número rectangular."""
    return -6 * log(num_llegadas)

def calcular_hora_salida(tiempo_llegada, tiempo_servicio):
    """Calcula la hora de salida sumando tiempo de llegada y tiempo de servicio."""
    return tiempo_llegada + tiempo_servicio

def lugares_disponibles(horas_salida, tiempo_actual, max_lugares):
    ocupados = [hs for hs in horas_salida if hs > tiempo_actual]
    return len(ocupados) < max_lugares

def ResoluciónProblema():
    tiempo = 0
    clientes = 0
    horas_salida = []
    lugar_disponible = 6
    capacidad = 6
    data = []
    rechazados = 0
    suma_espacios_disponibles = 0

    while tiempo <= 60:
        cliente_actual = []
        cliente_actual.append(clientes + 1)
        num_llegadas = random.random()
        cliente_actual.append(round(num_llegadas, 2))

        tiempo_llegadas = tiempo_entre_llegadas(num_llegadas)
        cliente_actual.append(round(tiempo_llegadas, 2))

        tiempo += tiempo_llegadas
        cliente_actual.append(round(tiempo, 2))

        # Libera lugares de clientes que ya salieron
        horas_salida = [hs for hs in horas_salida if hs > tiempo]

        espacios_disponibles = lugar_disponible - len(horas_salida)
        suma_espacios_disponibles += espacios_disponibles

        if lugares_disponibles(horas_salida, tiempo, lugar_disponible):
            hora_servicio = random.random()
            cliente_actual.append(round(hora_servicio, 2))

            tiempo_servicio = 10 + 20 * hora_servicio
            cliente_actual.append(round(tiempo_servicio, 2))

            hora_salida = calcular_hora_salida(tiempo, tiempo_servicio)
            cliente_actual.append(round(hora_salida, 2))

            horas_salida.append(hora_salida)
            cliente_actual.append("✅")
        else:
            cliente_actual += ["-", "-", "-", "❌"]
            rechazados += 1

        data.append(cliente_actual)
        clientes += 1

    tabulación = tabulate(
        data,
        headers=["Cliente", "R(llegadas)", "Tiempo entre llegadas", "Hora de llegada(min)", "R(servicio)","Tiempo de servicio", "hora de salida(min)", "Lugar disponible"],
        tablefmt="grid",
    )
    print(tabulación)

    # Calcula los indicadores y los retorna
    porcentaje_rechazados = (rechazados / clientes) * 100
    probabilidad_encontrar_espacio = ((clientes - rechazados) / clientes) * 100
    promedio_espacios_disponibles = suma_espacios_disponibles / clientes

    return tabulación, porcentaje_rechazados, probabilidad_encontrar_espacio, promedio_espacios_disponibles, capacidad
@app.get("/ejecución/simulación", response_class=HTMLResponse)
def main():
    tabulación, porcentaje_rechazados, probabilidad_encontrar_espacio, promedio_espacios_disponibles, capacidad = ResoluciónProblema()
    resultado = (
        f"<pre>{tabulación}\n"
        f"a) Porcentaje de clientes rechazados: {porcentaje_rechazados:.2f}%\n"
        f"b) Probabilidad de encontrar espacio: {probabilidad_encontrar_espacio:.2f}%\n"
        f"c) Porcentaje promedio de espacios disponibles: {promedio_espacios_disponibles / capacidad * 100:.2f}%\n"
        f"</pre>"
    )
    
    return resultado


# Punto de entrada del programa
if __name__ == "__main__":
    logger.info("Iniciando servidor FASTAPI...")
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
    