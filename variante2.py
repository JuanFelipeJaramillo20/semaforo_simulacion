from itertools import product
import random

class CruceSemaforos:
    def __init__(self, configuracion):
        self.configuracion = configuracion
        self.tiempo_simulacion = 10  # Tiempo total de la simulación en segundos

    def simular(self):
        tiempo_total_autos = 0
        for segundo in range(self.tiempo_simulacion):
            autos_en_cruce = sum(self.configuracion.values())
            tiempo_total_autos += autos_en_cruce

            for semaforo in self.configuracion:
                self.configuracion[semaforo] -= 1
                if self.configuracion[semaforo] == 0:
                    self.configuracion[semaforo] = random.randint(5, 15)

        tiempo_promedio_autos = tiempo_total_autos / self.tiempo_simulacion
        return tiempo_promedio_autos


def encontrar_configuracion_optima():
    tiempos_posibles = range(5, 16)  # Intervalo de tiempo posible para cada semáforo
    configuraciones_posibles = product(tiempos_posibles, repeat=4)  # 4 semáforos en el cruce

    mejor_configuracion = None
    mejor_tiempo_promedio = float('inf')

    for configuracion in configuraciones_posibles:
        configuracion_actual = {"Norte": configuracion[0], "Sur": configuracion[1], "Este": configuracion[2], "Oeste": configuracion[3]}
        cruce = CruceSemaforos(configuracion_actual)
        tiempo_promedio = cruce.simular()

        if tiempo_promedio < mejor_tiempo_promedio:
            mejor_tiempo_promedio = tiempo_promedio
            mejor_configuracion = configuracion_actual

    print("\nMejor configuración:")
    print(f"Configuración: {mejor_configuracion}")
    print(f"Tiempo promedio de espera de autos: {mejor_tiempo_promedio:.2f} autos/segundo")


# Ejemplo de uso
encontrar_configuracion_optima()
