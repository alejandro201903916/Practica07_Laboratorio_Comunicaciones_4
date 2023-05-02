import sounddevice as sd
import scipy.io.wavfile as wavfile

duration = 5  # duración de la grabación en segundos
fs = 44100    # frecuencia de muestreo

# grabando la señal
print("Grabando...")
x = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()  # espera hasta que la grabación esté completa

# almacenando la señal en un archivo wav
wavfile.write("grabacion.wav", fs, x)

# leyendo el archivo de audio
fs, x = wavfile.read("grabacion.wav")

# reproduciendo la señal grabada
sd.play(x, fs)
sd.wait()