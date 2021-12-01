from kafka import KafkaConsumer
import numpy as np
# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer('bigdata',bootstrap_servers=['localhost:9092'])

lista = []
for PRICE in consumer:
        valor = PRICE.value.decode('utf-8')
        mod = valor.strip('"')
        valor = int(mod)
        lista.append( valor )
        print(chr(27)+"[1;32m"+f'Promedio: {sum(lista)/len(lista)} ׀ Maximo: {max(lista)} ׀ Minimo: {min(lista)} / dst: {2*np.std(lista)}')

        if valor < (2 * np.std(lista)):
          print(chr(27)+"[1;32m"+f' EL valor {valor} està dos veces debajo de la desviacion estandar')
        if valor > (2* np.std(lista)):
          print(chr(27)+"[1;31m"+f' El valor {valor} està dos veces arriba de la desviacion estandar')