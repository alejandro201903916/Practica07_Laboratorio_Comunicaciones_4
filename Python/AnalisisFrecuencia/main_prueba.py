# Para la escritura del vectorize
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from AnalisisFrecuencia import AnalisisFrecuencia

# Se lee el archivo de audio x, almacenado en la actual carpeta de trabajo
fs, x = wavfile.read('y.wav')
lx = len(x)  # Cálculo del tamaño del vector de audio

# Se lee el archivo de audio y, almacenado en la actual carpeta de trabajo
fs, y = wavfile.read('yfinal.wav')
ly = len(y)  # Cálculo del tamaño del vector de audio
# Grafica de los vectores

n = np.arange(lx)
fig, axs = plt.subplots(2, 1)
axs[0].stem(n, x)
axs[0].set_title('X[n]')
axs[1].stem(n, y)
axs[1].set_title('Y[n]')
plt.show()

# Llamada a la función AnalisisFrecuencia
y, yfinal, porcentajes = AnalisisFrecuencia(x, fs)
