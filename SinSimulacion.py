import logging
from typing import Tuple
from math import factorial
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

#CALCULAR EL TIEMPO PROMEDIO DE SERVICIO

# CALCULAR LA TASA DE SERVICIO MIU

#USAR MODELO M/M/c/c
#USAR EL MODELO ERLANG B


def TasaServicio(tiempo: float) -> int:
    """ 
    Obtener la tasa de servicio que es el inverso del tiempo promedio de estancia
    """
    
    return int((1 / tiempo)) # Servicios por hora, dado que el tiempo es en horas


def TiempoPromedio(minimo:int, maximo:int) -> Tuple[float, int]:
    """
    Calcula la tasa de servicio (estancia) sabiendo que sigue una distribución uniforme entre 10 y 30 minutos
    """
    promedio = (minimo + maximo) / 2 # Promedio en minutos
    diferencia = (minimo + maximo) / 2/ 60 # Convertir a horas
    return (round(diferencia,2), promedio)



def ModeloErlangB(tasa_servicio: int, C: int, razon_media: int) -> Tuple[float, float]:
    """Utilizamos el modelo Erlang B para la tasa de llegada efectiva entre todos los servidores"""
    #C es el número de servidores
    P = (razon_media / tasa_servicio)
    
    numerador = (P ** C) / factorial(C)
    
    suma = 0
    for num in range(0, C + 1):
        suma +=  (P ** num) / factorial(num) 
    return (round(numerador / suma, 5), P) # Probabilidad de que el sistema esté ocupado
    

def ProbabilidadLugarDisponible(Modelo: float) -> float:
    """
    Probabilidad de que espacios disponibles
    """
    return round((1 - Modelo)*100, 2) # Probabilidad de que haya un lugar disponible

def PorcentajesPromedioEspaciosDisponibles(Modelo: float, TareaA:float, P:float) -> float:
    L = (P * (TareaA/100) )
    return ((Modelo - L ) / Modelo) * 100 # Porcentaje promedio de espacios disponibles
    
def Main():
    logger.info("Iniciando el programa 5.14 lote de estacionamientos...")
    
    # Definir los parámetros del sistema
    lugar_disponible = 6
    razon_media = 10 #Diez clientes por hora
    tiempo_minimo = 10 #Minutos
    tiempo_maximo = 30 #Minutos
    
    logger.info("Parametros del sistema")
    logger.info(f"lugares disponibles: {lugar_disponible}")
    logger.info(f"razon media: {razon_media}")
    logger.info(f"tiempo minimo: {tiempo_minimo}")
    logger.info(f"tiempo maximo: {tiempo_maximo}")
    
    # Calcular el tiempo promedio de servicio (estancia)
    tiempo_promedio = TiempoPromedio(tiempo_minimo, tiempo_maximo) # tipo de datos: int
    logger.info(f"Tiempo promedio de servicio: {tiempo_promedio} horas")
    # Calcular la tasa de servicio
    tasa_servicio = TasaServicio(tiempo_promedio[0]) # tipo de datos: float
    logger.info(f"Tasa de servicio: {tasa_servicio} clientes por hora")
    
    
    """HASTA AQUÍ SE EMPIEZAN A OBTENER LOS RESULTADOS"""
    logger.info("--------------------------Resultados--------------------------")
    #Usar el modelo Erlang B para calcular la tasa de llegada efectiva
    modelo_erlangb = ModeloErlangB(tasa_servicio, lugar_disponible, razon_media)
    logger.info(f"Porcentaje de Clientes rechazados: {modelo_erlangb[0]*100}%")
    
    # Calcular la probabilidad de que haya un lugar disponible
    TareaA = ProbabilidadLugarDisponible(modelo_erlangb[0])
    logger.info(f"Probabilidad de que haya un lugar disponible: {TareaA}%")
    
    # Calcular el porcentaje promedio de espacios disponibles
    TareaB = PorcentajesPromedioEspaciosDisponibles(lugar_disponible, TareaA, modelo_erlangb[1])    
    logger.info(f"Porcentaje promedio de espacios disponibles: {TareaB}%")
    
    
    
    return tiempo_promedio, tasa_servicio

print(Main())


