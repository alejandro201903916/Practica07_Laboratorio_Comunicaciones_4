import sys
import scipy.signal as signal
import numpy as np
from scipy.io.wavfile import write
from scipy.signal import butter, filtfilt, cheby2
from scipy.signal import firwin, convolve
import matplotlib.pyplot as plt
from scipy.signal import freqz
from scipy.io import wavfile

fs, x = wavfile.read('y.wav')

Ganancias = 20 * np.log10(np.max(np.abs(x)))

#definir vector de ganancias
Ganancias = np.linspace(0, 1, 10)

if len(sys.argv) < 3:
    print("No ha ingresado la frecuencia de muestreo fs, por lo tanto tomara el valor por default fs=48000 Hz")
    print("Esto provocara una mala grabacion de las funciones finales si no coinciden los fs")
    fs = 16000
else:
    fs = int(sys.argv[2])

G = Ganancias
fac = 1  # Normalizacion de la frecuencia

# Frecuencias de corte para filtros
Wn1 = [fac * 0.01098, fac * 0.02150]  # filtro banda 1
Wn2 = [fac * 0.02150, fac * 0.04150]  # filtro banda 2
Wn3 = [fac * 0.05250, fac * 0.07250]  # filtro banda 3
Wn4 = [fac * 0.08500, fac * 0.11500]  # filtro banda 4
Wn5 = [fac * 0.11500, fac * 0.18300]  # filtro banda 5
Wn6 = [fac * 0.19400, fac * 0.29700]  # filtro banda 6
Wn7 = [fac * 0.30000, fac * 0.40500]  # filtro banda 7
Wn8 = [fac * 0.41000, fac * 0.60500]  # filtro banda 8
Wn9 = [fac * 0.60000, fac * 0.76040]  # filtro banda 9
Wn10 = [fac * 0.77000, fac * 0.92465]  # filtro banda 10

# Filtros Butter
b1, a1 = signal.butter(2, Wn1, 'band')
y1 = signal.filtfilt(b1, a1, x)
write('filtro1.wav', fs, y1)

b2, a2 = signal.butter(3, Wn2, 'band')
y2 = signal.filtfilt(b2, a2, x)
write('filtro2.wav', fs, y2)

# Filtros Cheby1
b3, a3 = signal.cheby1(5, 10, Wn3, 'band')
y3 = signal.filtfilt(b3, a3, x)
write('filtro3.wav', fs, y3)

b4, a4 = signal.cheby1(5, 10, Wn4, 'band')
y4 = signal.filtfilt(b4, a4, x)
write('filtro4.wav', fs, y4)

# Filtros Ellip
b5, a5 = signal.ellip(5, 10, 500, Wn5, 'band')
y5 = signal.filtfilt(b5, a5, x)
write('filtro5.wav', fs, y5)

b6, a6 = signal.ellip(5, 1, 200, Wn6, 'band')
y6 = signal.filtfilt(b6, a6, x)
write('filtro6.wav', fs, y6)

# Filtro Cheby2 1
b7, a7 = cheby2(10, 50, Wn7, btype="band", fs=fs)
y7 = filtfilt(b7, a7, x)
wavfile.write('filtro7.wav', fs, y7)

# Filtro Cheby2 2
b8, a8 = cheby2(10, 40, Wn8, btype="band", fs=fs)
y8 = filtfilt(b8, a8, x)
wavfile.write('filtro8.wav', fs, y8)

# Filtro FIR 1
y9 = y8
b9 = firwin(61, Wn9)
ym9 = convolve(x, b9, mode='same')
wavfile.write('filtro9.wav', fs, y9)

# Filtro FIR 2
y10 = y9
b10 = firwin(61, Wn10)
ym10 = convolve(x, b10, mode='same')
wavfile.write('filtro10.wav', fs, y10)

# Arreglo de vectores
y9 = ym9
y10 = ym10

v = np.shape(G)
if v[0] == 10:
    G = np.transpose(G)

y = G[0]*y1 + G[1]*y2 + G[2]*y3 + G[3]*y4 + G[4]*y5 + G[5]*y6 + G[6]*y7 + G[7]*y8 + G[8]*y9 + G[9]*y10

# Guardando el archivo de audio
wavfile.write('y.wav', fs, y)

#Graficas
#Funciones
plt.figure(1)
n = np.arange(1, len(x) + 1)
plt.subplot(2, 1, 1)
plt.stem(n, x)
plt.title('x[n]')
plt.subplot(2, 1, 2)
plt.stem(n, y)
plt.title('y[n]')

# Graficas
# Funciones
w1, h1 = signal.freqz(b1, a1)
w2, h2 = signal.freqz(b2, a2)
w3, h3 = signal.freqz(b3, a3)
w4, h4 = signal.freqz(b4, a4)
w5, h5 = signal.freqz(b5, a5)
w6, h6 = signal.freqz(b6, a6)
w7, h7 = signal.freqz(b7, a7)
w8, h8 = signal.freqz(b8, a8)
w9, h9 = signal.freqz(b9, [1])
w10, h10 = signal.freqz(b10, [1])

plt.plot(w1/np.pi, 20*np.log10(abs(h1)), label='FILTRO CON FRECUENCIA CENTRAL EN:  31.5 Hz')
plt.plot(w2/np.pi, 20*np.log10(abs(h2)), label='FILTRO CON FRECUENCIA CENTRAL EN:  63 Hz')
plt.plot(w3/np.pi, 20*np.log10(abs(h3)), label='FILTRO CON FRECUENCIA CENTRAL EN:  125 Hz')
plt.plot(w4/np.pi, 20*np.log10(abs(h4)), label='FILTRO CON FRECUENCIA CENTRAL EN:  250 Hz')
plt.plot(w5/np.pi, 20*np.log10(abs(h5)), label='FILTRO CON FRECUENCIA CENTRAL EN:  500 Hz')
plt.plot(w6/np.pi, 20*np.log10(abs(h6)), label='FILTRO CON FRECUENCIA CENTRAL EN:  1 kHz')
plt.plot(w7/np.pi, 20*np.log10(abs(h7)), label='FILTRO CON FRECUENCIA CENTRAL EN:  2 kHz')
plt.plot(w8/np.pi, 20*np.log10(abs(h8)), label='FILTRO CON FRECUENCIA CENTRAL EN:  4 kHz')
plt.plot(w9/np.pi, 20*np.log10(abs(h9)), label='FILTRO CON FRECUENCIA CENTRAL EN:  8 kHz')
plt.plot(w10/np.pi, 20*np.log10(abs(h10)), label='FILTRO CON FRECUENCIA CENTRAL EN:  16 kHz')

plt.legend()
plt.xlabel('Frecuencia Normalizada')
plt.ylabel('Magnitud (dB)')
plt.title('RELACION TOTAL DE FILTROS GON GANANCIA UNITARIA')
plt.show()


'''# Funciones
n = range(len(x))
fig, axs = plt.subplots(2, 1)
axs[0].stem(n, x)
axs[0].set_title('x[n]')
axs[1].stem(n, y)
axs[1].set_title('y[n]')

# Filtros
fig = plt.figure(figsize=(12, 8))
plt.subplots_adjust(hspace=0.5)

plt.subplot(5, 2, 1)
w, h = signal.freqz(b1, a1)
plt.plot(w/np.pi, abs(h))
plt.title('FILTRO CON FRECUENCIA CENTRAL EN:  31.5 Hz')
plt.xlabel('Normalized frequency')
plt.ylabel('Amplitude')

plt.subplot(5, 2, 2)
w, h = signal.freqz(b2, a2)
plt.plot(w/np.pi, abs(h))
plt.title('FILTRO CON FRECUENCIA CENTRAL EN:  63 Hz')
plt.xlabel('Normalized frequency')
plt.ylabel('Amplitude')

plt.subplot(5, 2, 3)
w, h = signal.freqz(b3, a3)
plt.plot(w/np.pi, abs(h))
plt.title('FILTRO CON FRECUENCIA CENTRAL EN: 125 Hz')
plt.xlabel('Normalized frequency')
plt.ylabel('Amplitude')

plt.subplot(5, 2, 4)
w, h = signal.freqz(b4, a4)
plt.plot(w/np.pi, abs(h))
plt.title('FILTRO CON FRECUENCIA CENTRAL EN:  250 Hz')
plt.xlabel('Normalized frequency')
plt.ylabel('Amplitude')

plt.subplot(5, 2, 5)
w, h = signal.freqz(b5, a5)
plt.plot(w/np.pi, abs(h))
plt.title('FILTRO CON FRECUENCIA CENTRAL EN:  500 Hz')
plt.xlabel('Normalized frequency')
plt.ylabel('Amplitude')

plt.subplot(5, 2, 6)
w, h = signal.freqz(b6, a6)
plt.plot(w/np.pi, abs(h))
plt.title('FILTRO CON FRECUENCIA CENTRAL EN:  1 kHz')
plt.xlabel('Normalized frequency')
plt.ylabel('Amplitude')

plt.subplot(5, 2, 7)
w, h = signal.freqz(b7, a7)
plt.plot(w/np.pi, abs(h))
plt.title('FILTRO CON FRECUENCIA CENTRAL EN:  2 kHz')
plt.xlabel('Normalized frequency')
plt.ylabel('Amplitude')

plt.subplot(5, 2, 8)
w, h = signal.freqz(b8, a8)
plt.plot(w/np.pi, abs(h))
plt.title('FILTRO CON FRECUENCIA CENTRAL EN:  4 kHz')
plt.xlabel('Normalized frequency')
plt.ylabel('Amplitude')

plt.subplot(5, 2, 9)
w, h = signal.freqz(b9, 1)
plt.plot(w/np.pi, abs(h))
plt.title('FILTRO CON FRECUENCIA CENTRAL EN:  8 kHz')
plt.xlabel('Normalized frequency')
plt.ylabel('Amplitude')

plt.subplot(5, 2, 10)
w, h = signal.freqz(b10, 1)
plt.plot(w/np.pi, abs(h))
plt.title('FILTRO CON FRECUENCIA CENTRAL EN:  16 kHz')
plt.xlabel('Normalized frequency')
plt.ylabel('Amplitude')'''