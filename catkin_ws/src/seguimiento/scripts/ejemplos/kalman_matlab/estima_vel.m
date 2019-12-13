%**************************************************
% Funcion que estima la velocidad lineal y angular a partir de un vector de posiciones
% estado X=[x,y,theta]
% entrada T vector de tiempos
% T periodo de muestreo
%***************************************************
function [v,w,theta] = estima_vel (X,T,n)

%n=length(T);
if n==1
   v=0;
   w=0;
   return;
end;
tpar=1;	% Tiempo para el calculo de la velocidad, se supone constante en el intervalo
desp=0;
theta=0;
k=n;
while k>1 & (T(n)-tpar) < T(k)
   despx=X(k,1)-X(k-1,1);
   despy=X(k,2)-X(k-1,2);
   
  
   desp=desp+sqrt(despx*despx+ despy*despy);
   k=k-1;
end
v=desp/(T(n)-T(k));
theta=theta+atan2(X(n,2)-X(n-1,2),X(n,1)-X(n-1,1))*180/pi;
w=0;

