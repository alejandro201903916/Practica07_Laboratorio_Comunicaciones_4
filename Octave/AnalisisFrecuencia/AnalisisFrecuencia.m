function [y,yfinal,porcentajes]=AnalisisFrecuencia(x,fs) 
  %Establecemos en Octave
  pkg load signal;
  pkg load symbolic;
  pkg load optim;

    if nargin==1 % revisa si se ingreso fs o si no toma como valor fs=8000
    disp('No ha ingresado la frecuencia de muestreo fs, por lo tanto tomara el valor por default fs=16000 Hz')
    disp('Esto provocara una mala grabaci�n de las funciones finales si no coinciden los fs')
    fs=16000;
    end 
        fac=1; %ajuste de escala para frecuencia
%Frecuancias de corte para Filtros
      Wn  = fac*[0.2 ,  0.5]; 
      Wn1 = fac*[0.2 ,  0.26]; 
      Wn2 = fac*[0.26 , 0.32]; 
      Wn3 = fac*[0.32 , 0.38]; 
      Wn4 = fac*[0.38 , 0.44]; 
      Wn5 = fac*[0.44 , 0.50]; 

  %Calculo de coeficientes para filtros
         [b,a]   = butter(20,Wn); %filtro principal
         [b1,a1] = butter(10,Wn1);%filtro banda 1
         [b2,a2] = butter(10,Wn2);%filtro banda 2
         [b3,a3] = butter(10,Wn3);%filtro banda 3
         [b4,a4] = butter(10,Wn4);%filtro banda 4
         [b5,a5] = butter(10,Wn5);%filtro banda 5
 
 %Aplicaci�n de filtros
     y = filter(b,a,x);
         y1=filter(b1,a1,y);
         y2=filter(b2,a2,y);
         y3=filter(b3,a3,y);
         y4=filter(b4,a4,y);
         y5=filter(b5,a5,y);
   
 %calculo de energ�a
 
     energiatotal=0;
     energiade2a5=0;
        energia1=0;
        energia2=0;
        energia3=0;
        energia4=0;
        energia5=0;
     
     for i=1:length(x)
        energiatotal = energiatotal+sqrt(x(i,1)*x(i,1));
        energiade2a5 =  energiade2a5+sqrt(y(i,1)*y(i,1));
            energia1 =  energia1+sqrt(y1(i,1)*y1(i,1));
            energia2 =  energia2+sqrt(y2(i,1)*y2(i,1));
            energia3 =  energia3+sqrt(y3(i,1)*y3(i,1));
            energia4 =  energia3+sqrt(y4(i,1)*y4(i,1));
            energia5 =  energia5+sqrt(y5(i,1)*y5(i,1));
     end

     %energia totales para cada banda
     E=[energiatotal energiade2a5  energia1  energia2 energia3  energia4 energia5];

 %Calculo de porcentajes
     p=energiade2a5/energiatotal;
     p1=energia1/energiade2a5;
     p2=energia2/energiade2a5; 
     p3=energia3/energiade2a5; 
     p4=energia4/energiade2a5; 
     p5=energia5/energiade2a5;
 
    P=[p1 p2 p3 p4 p5];
    porcentajes=P;
% Funciones finales de audio
    y=y1+y2+y3+y4+y5;
    %Calculo de coeficientes para eleminicaci�n bandas en audio, si la
    %banda es aceptada el coeficiente ser� 1 y si no ser� 0
    
       G=1:5; %definci�n de vector de coeficnetes
       G=0*G;
       for i=1:5
           if P(i)>.25   %porcentaje de acepataci�n
            G(i)=1; %ganancia unitaria
           end
       end
        yfinal=G(1)*y1+G(2)*y2+G(3)*y3+G(4)*y4+G(5)*y5;

  %Guardando archivos de audio en la carpeta contenerdora de la funci�n
     audiowrite('y.wav',y,fs); %wavwrite(y,fs,'y'); 
     audiowrite('yfinal.wav', yfinal,fs); %wavwrite(yfinal,fs,'yfinal');
   
  %Graficas
    %Funciones
        figure(1)
      n=1:length(x);
      subplot(3,1,1)
            stem(n,x)
            title('x[n]')
      subplot(3,1,2)
            stem(n,y)
            title('y[n]')
      subplot(3,1,3)
            stem(n,yfinal)
            title('yfinal[n]')
     %Filtro de 2 a 5 KHz
         fvtool(b,a)
         title('FILTRO PARA BANDA PRINCIAPAL (2.0-5.0)KHz')
     %Filtros aplicados a la banda
        fvtool(b1,a1)
            title('PRIMER FILTRO: (2.0-2.6)KHz')    
        fvtool(b2,a2)
            title('SEGUNDO  FILTRO: (2.6-3.2)KHz')  
        fvtool(b3,a3)
            title('TERCER FILTRO: (3.2-3.8)KHz')  
        fvtool(b4,a4)
            title('CUARTO FILTRO: (3.8-4.2)KHz')  
        fvtool(b5,a5)
            title('QUINTO FILTRO: (4.2-5.0)KHz') 
        fvtool(b,a,b1,a1,b2,a2,b3,a3,b4,a4,b5,a5)
            title('RELACION TOTAL DE FILTROS')

  
