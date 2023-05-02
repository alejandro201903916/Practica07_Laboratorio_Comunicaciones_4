%Para la escritura del vectorize
clc
clear %limpiamos la ventana de comandos
%Se lee el archivo de audio x, almacenado en la actual carpeta de trabajo
%Establecemos en octave
pkg load signal;
[x, fs] = audioread('y.wav'); 

lx=length(x); % Cálculo del tamaño del vector de audio

%Se lee el archivo de audio y, almacenado en la actual carpeta de trabajo
[y, fs] = audioread('yfinal.wav');

ly=length(y); % Cálculo del tamaño del vector de audio

%Grafica de los vectores
n=0:lx-1;
figure(5);
subplot(2,1,1);
stem(n, x);
title('X[n]');
subplot(2,1,2);
stem(n,y);
title('Y[n]');

[y,yfinal,porcentajes]=AnalisisFrecuencia(x,fs) 