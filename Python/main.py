import numpy as np
from scipy.signal import butter, filtfilt
from scipy.io import wavfile
import matplotlib.pyplot as plt
from scipy import signal

fs, x = wavfile.read('AnalisisFrecuencia/y.wav')
lx = len(x)

if fs is None:
    print("No ha ingresado la frecuencia de muestreo fs, por lo tanto tomara el valor por default fs=16000 Hz")
    print("Esto provocara una mala grabaci�n de las funciones finales si no coinciden los fs")
    fs = 16000

# Frecuancias de corte para Filtros
fac = 1
Wn = np.array([0.2, 0.5]) * fac
Wn1 = np.array([0.2, 0.26]) * fac
Wn2 = np.array([0.26, 0.32]) * fac
Wn3 = np.array([0.32, 0.38]) * fac
Wn4 = np.array([0.38, 0.44]) * fac
Wn5 = np.array([0.44, 0.50]) * fac

# Calculo de coeficientes para filtros
b, a = butter(20, Wn, 'band')
b1, a1 = butter(10, Wn1, 'band')
b2, a2 = butter(10, Wn2, 'band')
b3, a3 = butter(10, Wn3, 'band')
b4, a4 = butter(10, Wn4, 'band')
b5, a5 = butter(10, Wn5, 'band')

# Aplicaci�n de filtros
y = filtfilt(b, a, x)
y1 = filtfilt(b1, a1, y)
y2 = filtfilt(b2, a2, y)
y3 = filtfilt(b3, a3, y)
y4 = filtfilt(b4, a4, y)
y5 = filtfilt(b5, a5, y)

# calculo de energ�a
energiatotal = np.sqrt(np.sum(x ** 2))
energiade2a5 = np.sqrt(np.sum(y ** 2))
energia1 = np.sqrt(np.sum(y1 ** 2))
energia2 = np.sqrt(np.sum(y2 ** 2))
energia3 = np.sqrt(np.sum(y3 ** 2))
energia4 = np.sqrt(np.sum(y4 ** 2))
energia5 = np.sqrt(np.sum(y5 ** 2))

# energia totales para cada banda
E = np.array([energiatotal, energiade2a5, energia1, energia2, energia3, energia4, energia5])

# Cálculo de porcentajes
p = energiade2a5 / energiatotal
p1 = energia1 / energiade2a5
p2 = energia2 / energiade2a5
p3 = energia3 / energiade2a5
p4 = energia4 / energiade2a5
p5 = energia5 / energiade2a5

P = [p1, p2, p3, p4, p5]
porcentajes = P

# Funciones finales de audio
y = y1 + y2 + y3 + y4 + y5

# Cálculo de coeficientes para eliminación bandas en audio
# Si la banda es aceptada el coeficiente será 1 y si no será 0
G = [0, 0, 0, 0, 0]  # Definición de vector de coeficientes
for i in range(5):
    if P[i] > 0.25:  # Porcentaje de aceptación
        G[i] = 1  # Ganancia unitaria

yfinal = G[0] * y1 + G[1] * y2 + G[2] * y3 + G[3] * y4 + G[4] * y5

# Guardando archivos de audio en la carpeta contenedora de la función
import scipy.io.wavfile as wav

wav.write('AnalisisFrecuencia/y.wav', fs, y)
wav.write('AnalisisFrecuencia/yfinal.wav', fs, yfinal)

# Graficas
# Funciones
n = np.arange(len(x))
fig, axs = plt.subplots(3, 1, figsize=(8, 6))
axs[0].stem(n, x)
axs[0].set_title('x[n]')
axs[1].stem(n, y)
axs[1].set_title('y[n]')
axs[2].stem(n, yfinal)
axs[2].set_title('yfinal[n]')
plt.tight_layout()

# Filtro de 2 a 5 KHz
fig, ax = plt.subplots()
w, h = signal.freqz(b, a)
ax.plot(w / np.pi * fs / 2, 20 * np.log10(np.abs(h)))
ax.set_xlabel('Frecuencia (Hz)')
ax.set_ylabel('Magnitud (dB)')
ax.set_title('FILTRO PARA BANDA PRINCIAPAL (2.0-5.0)KHz')

# Filtros aplicados a la banda
fig, axs = plt.subplots(5, 1, figsize=(8, 12))
w, h = signal.freqz(b1, a1)
axs[0].plot(w / np.pi * fs / 2, 20 * np.log10(np.abs(h)))
axs[0].set_title('PRIMER FILTRO: (2.0-2.6)KHz')
w, h = signal.freqz(b2, a2)
axs[1].plot(w / np.pi * fs / 2, 20 * np.log10(np.abs(h)))
axs[1].set_title('SEGUNDO  FILTRO: (2.6-3.2)KHz')
w, h = signal.freqz(b3, a3)
axs[2].plot(w / np.pi * fs / 2, 20 * np.log10(np.abs(h)))
axs[2].set_title('TERCER FILTRO: (3.2-3.8)KHz')
w, h = signal.freqz(b4, a4)
axs[3].plot(w / np.pi * fs / 2, 20 * np.log10(np.abs(h)))
axs[3].set_title('CUARTO FILTRO: (3.8-4.2)KHz')
w, h = signal.freqz(b5, a5)
axs[4].plot(w / np.pi * fs / 2, 20 * np.log10(np.abs(h)))
axs[4].set_title('QUINTO FILTRO: (4.2-5.0)KHz')
plt.tight_layout()