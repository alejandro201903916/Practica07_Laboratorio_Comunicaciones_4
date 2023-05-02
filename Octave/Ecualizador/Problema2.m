%Para la escritura del vectorize
clc
clear %limpiamos la ventana de comandos
%Se lee el archivo de audio x, almacenado en la actual carpeta de trabajo
%Establecemos en octave
pkg load signal;
pkg load symbolic;
pkg load optim;

[x, fs] = audioread('y.wav'); 

Ganancias = 20*(log10(max(abs(x))));

% definir vector de ganancias
Ganancias = linspace(0, 1, 10);

% calcular ganancias y graficar formas de onda
for i = 1:length(Ganancias)
  % aplicar ganancia
  x_ganancia = x * Ganancias(i);
  
  % calcular ganancia
  Ganancia = 20*(log10(max(abs(x_ganancia))));
endfor
lx=length(x); % Cálculo del tamaño del vector de audio

%Se lee el archivo de audio y, almacenado en la actual carpeta de trabajo
%[y, fs] = audioread('yfinal.wav');

%ly=length(y); % Cálculo del tamaño del vector de audio

%Grafica de los vectores
n=0:lx-1;
figure(2);
subplot(1,1,1);
stem(n, x);
title('X[n]');
%subplot(2,1,2);
%stem(n,y);
%title('Y[n]');


[y]=Ecualizador(Ganancias,x,fs)