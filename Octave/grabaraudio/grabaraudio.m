%function [x]=grabaraudio(t,fs) 
%función a traves de la cual se graba un archivo de audio con el nobre "grabacion"
%Da como resultado un vector x y su frecuencia de muestreo, almacena la
%señal grabada en la carpeta 'grabaraudio'
n = 20;

x = audiorecorder(t*fs, fs, 1); %wavrecord(t*fs, fs, 1);
N=16;
audiowrite('grabacion.wav',x,fs,N); %wavwrite(x,fs,N,'grabacion') %almacenamiento de la funcion
[x,fs,bits] = audioread('grabacion.wav');
audioplayer(x,fs);%reproduce señal grabada