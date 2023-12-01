import simpy
import random

class Puente:
    def __init__(self, env, semaforo_norte, semaforo_sur):
        self.env = env
        self.puente_disponible = True
        self.semaforo_norte = semaforo_norte
        self.semaforo_sur = semaforo_sur
        self.tiempos_espera = []

    def pasar_puente(self):
        inicio_espera = self.env.now
        yield self.env.timeout(1)
        fin_paso = self.env.now
        tiempo_espera = fin_paso - inicio_espera
        #self.tiempos_espera.append(tiempo_espera)
        self.tiempos_espera.append(self.env.now)

def llegada_carro(env, direccion, puente):
    while True:
        yield env.timeout(random.expovariate(1/3 if direccion == 'norte' else 1/5))
        print(f"Carro desde {direccion} llega al puente en el tiempo {env.now}")
        with (puente.semaforo_norte.request() if direccion == 'norte' else puente.semaforo_sur.request()) as req:
            yield req
            print(f"Semaforo en verde desde {direccion} en el tiempo {env.now}")
            yield env.process(puente.pasar_puente())

def simular(tiempo_simulacion, tiempo_verde_norte, tiempo_rojo_norte, tiempo_verde_sur, tiempo_rojo_sur):
    env = simpy.Environment()

    semaforo_norte = simpy.Resource(env, capacity=1)
    semaforo_sur = simpy.Resource(env, capacity=1)
    
    puente = Puente(env, semaforo_norte, semaforo_sur)

    env.process(llegada_carro(env, 'norte', puente))
    env.process(llegada_carro(env, 'sur', puente))

    env.run(until=tiempo_simulacion)

    tiempo_promedio_espera = sum(puente.tiempos_espera) / len(puente.tiempos_espera)
    print(f"Tiempo promedio de espera: {tiempo_promedio_espera} minutos")
    return tiempo_promedio_espera

best_config = None
min_time = float('inf')

configs = {}

green_light_durations = [3, 5, 8]
red_light_durations = [3, 5, 8]

for green_norte in green_light_durations:
    for red_norte in red_light_durations:
        for green_sur in green_light_durations:
            for red_sur in red_light_durations:
                print(f"Testing combination: G_Norte={green_norte}, R_Norte={red_norte}, G_Sur={green_sur}, R_Sur={red_sur}")
                tiempo_espera = simular(
                    tiempo_simulacion=30,
                    tiempo_verde_norte=green_norte,
                    tiempo_rojo_norte=red_norte,
                    tiempo_verde_sur=green_sur,
                    tiempo_rojo_sur=red_sur
                )
                configs[f"{green_norte}-{red_norte}-{green_sur}-{red_sur}"] = tiempo_espera
                
                if tiempo_espera < min_time:
                    min_time = tiempo_espera
                    best_config = f"{green_norte}-{red_norte}-{green_sur}-{red_sur}"

print(f"\nBest Configuration: {best_config} with time {min_time} minutes")
