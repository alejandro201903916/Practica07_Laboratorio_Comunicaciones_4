import sys
import scipy.signal as signal
import numpy as np
from scipy.io.wavfile import write
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
from scipy.signal import freqz
from scipy.io import wavfile

# Se lee el archivo de audio x, almacenado en la actual carpeta de trabajo
fs, x = wavfile.read('y.wav')
lx = len(x)  # Cálculo del tamaño del vector de audio

if len(sys.argv) == 2:
    fs = int(sys.argv[1])
    print('Ha ingresado la frecuencia de muestreo fs =', fs)
else:
    print('No ha ingresado la frecuencia de muestreo fs, por lo tanto tomará el valor por default fs=16000 Hz')
    print('Esto provocara una mala grabación de las funciones finales si no coinciden los fs')
    fs = 16000

# Ajuste de escala para frecuencia
fac = 1

# Frecuencias de corte para filtros
Wn = [fac * 0.2, fac * 0.5]
Wn1 = [fac * 0.2, fac * 0.26]
Wn2 = [fac * 0.26, fac * 0.32]
Wn3 = [fac * 0.32, fac * 0.38]
Wn4 = [fac * 0.38, fac * 0.44]
Wn5 = [fac * 0.44, fac * 0.50]

# Cálculo de coeficientes para filtros
b, a = signal.butter(20, Wn, 'band')   # filtro principal
b1, a1 = signal.butter(10, Wn1, 'band') # filtro banda 1
b2, a2 = signal.butter(10, Wn2, 'band') # filtro banda 2
b3, a3 = signal.butter(10, Wn3, 'band') # filtro banda 3
b4, a4 = signal.butter(10, Wn4, 'band') # filtro banda 4
b5, a5 = signal.butter(10, Wn5, 'band') # filtro banda 5

# Aplicación de filtros
y = signal.filtfilt(b, a, x)
y1 = signal.filtfilt(b1, a1, y)
y2 = signal.filtfilt(b2, a2, y)
y3 = signal.filtfilt(b3, a3, y)
y4 = signal.filtfilt(b4, a4, y)
y5 = signal.filtfilt(b5, a5, y)

# Cálculo de energía
energiatotal = 0
energiade2a5 = 0
energia1 = 0
energia2 = 0
energia3 = 0
energia4 = 0
energia5 = 0

for i in range(len(x)):
    energiatotal = energiatotal + np.sqrt(x[i] * x[i])
    energiade2a5 = energiade2a5 + np.sqrt(y[i] * y[i])
    energia1 = energia1 + np.sqrt(y1[i] * y1[i])
    energia2 = energia2 + np.sqrt(y2[i] * y2[i])
    energia3 = energia3 + np.sqrt(y3[i] * y3[i])
    energia4 = energia3 + np.sqrt(y4[i] * y4[i])
    energia5 = energia5 + np.sqrt(y5[i] * y5[i])

# energía total para cada banda
E = [energiatotal, energiade2a5, energia1, energia2, energia3, energia4, energia5]

# cálculo de porcentajes
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

# Cálculo de coeficientes para eliminación bandas en audio, si la banda es aceptada el coeficiente será 1 y si no será 0
G = np.zeros(5)

for i in range(5):
    if P[i] > 0.25: # porcentaje de aceptación
        G[i] = 1 # ganancia unitaria

yfinal = G[0] * y1 + G[1] * y2 + G[2] * y3 + G[3] * y4 + G[4] * y5

# Guardando archivos de audio en la carpeta contenerdora de la funci�n
write('y.wav', fs, y)
write('yfinal.wav', fs, yfinal)

# Graficas
# Funciones
n = np.arange(1, len(x) + 1)
plt.figure(1)
plt.subplot(3, 1, 1)
plt.stem(n, x)
plt.title('x[n]')
plt.subplot(3, 1, 2)
plt.stem(n, y)
plt.title('y[n]')
plt.subplot(3, 1, 3)
plt.stem(n, yfinal)
plt.title('yfinal[n]')


w, h = signal.freqz(b, a)
w1, h1 = signal.freqz(b1, a1)
w2, h2 = signal.freqz(b2, a2)
w3, h3 = signal.freqz(b3, a3)
w4, h4 = signal.freqz(b4, a4)
w5, h5 = signal.freqz(b5, a5)

plt.figure()
plt.subplot(2,1,1)
plt.plot(w/(2*np.pi), 20*np.log10(abs(h)), label='Filtro completo')
plt.plot(w1/(2*np.pi), 20*np.log10(abs(h1)), label='Primer filtro')
plt.plot(w2/(2*np.pi), 20*np.log10(abs(h2)), label='Segundo filtro')
plt.plot(w3/(2*np.pi), 20*np.log10(abs(h3)), label='Tercer filtro')
plt.plot(w4/(2*np.pi), 20*np.log10(abs(h4)), label='Cuarto filtro')
plt.plot(w5/(2*np.pi), 20*np.log10(abs(h5)), label='Quinto filtro')
plt.title('Respuesta de frecuencia')
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Amplitud [dB]')
plt.legend()

plt.subplot(2,1,2)
plt.plot(w/(2*np.pi), np.unwrap(np.angle(h))*180/np.pi, label='Filtro completo')
plt.plot(w1/(2*np.pi), np.unwrap(np.angle(h1))*180/np.pi, label='Primer filtro')
plt.plot(w2/(2*np.pi), np.unwrap(np.angle(h2))*180/np.pi, label='Segundo filtro')
plt.plot(w3/(2*np.pi), np.unwrap(np.angle(h3))*180/np.pi, label='Tercer filtro')
plt.plot(w4/(2*np.pi), np.unwrap(np.angle(h4))*180/np.pi, label='Cuarto filtro')
plt.plot(w5/(2*np.pi), np.unwrap(np.angle(h5))*180/np.pi, label='Quinto filtro')
plt.title('Respuesta de fase')
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Fase [grados]')
plt.legend()

plt.show()



'''# Filtro de 2 a 5 KHz
freqz(b, a)
plt.title('FILTRO PARA BANDA PRINCIAPAL (2.0-5.0)KHz')

# Filtros aplicados a la banda
freqz(b1, a1)
plt.title('PRIMER FILTRO: (2.0-2.6)KHz')
freqz(b2, a2)
plt.title('SEGUNDO  FILTRO: (2.6-3.2)KHz')
freqz(b3, a3)
plt.title('TERCER FILTRO: (3.2-3.8)KHz')
freqz(b4, a4)
plt.title('CUARTO FILTRO: (3.8-4.2)KHz')
freqz(b5, a5)
plt.title('QUINTO FILTRO: (4.2-5.0)KHz')
#freqz(b, a, b1, a1, b2, a2, b3, a3, b4, a4, b5, a5)
#plt.title('RELACION TOTAL DE FILTROS')
plt.show()'''