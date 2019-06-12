import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import scipy.integrate as integrate

#constantes
r=0.2905

archivo = pd.read_csv('Accelerometer Data 2019-04-10 10-30-56.txt', sep=',', header=None,skiprows=4)
archivo = np.array(archivo)

tiempo = np.zeros(len(archivo))
aceleracion_carro = np.zeros(len(archivo))

for i in range (len(archivo)):
    tiempo[i] = archivo[i][0]
    aceleracion_carro[i] = archivo[i][2]
t_0=650#500
t_f=1065#1060-1692
aceleracion_carro= gaussian_filter(aceleracion_carro,19)

velocidad_carro= integrate.cumtrapz(aceleracion_carro,tiempo)

distancia_carro= integrate.cumtrapz(velocidad_carro,tiempo[1:])

velocidad_angular_RPM= velocidad_carro*60/r/(2*np.pi)*10

potencia = 1400/746*aceleracion_carro[1:]*velocidad_carro
torque= 1400*aceleracion_carro[1:]*r/20

plt.plot(velocidad_angular_RPM[t_0:t_f],potencia[t_0:t_f],label='Potencia')
plt.plot(velocidad_angular_RPM[t_0:t_f],torque[t_0:t_f],label='Torque')
plt.legend(loc='lower right')
plt.grid()
plt.title('Nissan_march_K13')
plt.xlabel('RPM')
plt.ylabel('hp')
