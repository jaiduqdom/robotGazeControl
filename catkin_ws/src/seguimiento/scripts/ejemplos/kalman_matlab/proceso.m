%**************************************************
% Funcion de proceso de movimiento de un robot móvil
% estado Xk=[x,y,theta]
% entrada U=[v,w] Velocidad lineal y angular
% T periodo de muestreo
%***************************************************
function [Xk] = proceso (Xk_ant,U,T)

	Xk(1)=Xk_ant(1)+U(1)*cos(Xk_ant(3))*T;
	Xk(2)=Xk_ant(2)+U(1)*sin(Xk_ant(3))*T;
   Xk(3)=Xk_ant(3)+U(2)*T;

