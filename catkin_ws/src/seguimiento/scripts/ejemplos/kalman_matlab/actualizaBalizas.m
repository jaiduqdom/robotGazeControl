

function [Xk, Pk] = actualizaBalizas(Xk,Pk,Hk,Zk,Zek,R)
%desv_xy=0.05;
%desv_theta=0.08;
I=[1 0 0; 0 1 0; 0 0 1];

%Hk=[1 0 0;0 1 0; 0 0 1];% Para medidas de Gps
V=[1 0 0;0 1 0; 0 0 1];% Para medidas de GPS

        
        % Calculo de la funcion del sensor H    
        H=[(Xk(1)-p1x)/((Xk(1)-p1x)^2 + (Xk(2)-p1y)^2)^(1/2) (Xk(2)-p1y)/((Xk(1)-p1x)^2 + (Xk(2)-p1y)^2)^(1/2) 0; (Xk(1)-p2x)/((Xk(1)-p2x)^2 + (Xk(2)-p2y)^2)^(1/2) (Xk(2)-p2y)/((Xk(1)-p2x)^2 + (Xk(2)-p2y)^2)^(1/2) 0; (Xk(1)-p3x)/((Xk(1)-p3x)^2+(Xk(2)-p3y)^2)^(1/2) (Xk(2)-p3y)/((Xk(1)-p3x)^2 + (Xk(2)-p3y)^2)^(1/2) 0];
                                
        %Calculo del valor esperado
        ze=[sqrt((Xk(1)-p1x)^2+(Xk(2)-p1y)^2) sqrt((Xk(1)-p2x)^2+(Xk(2)-p2y)^2) sqrt((Xk(1)-p3x)^2+(Xk(2)-p3y)^2)] ;
              
        %Calculo de la ganancia del filtro
        K=Pk*Hk*inv(Hk*inv(Pk)*Hk'+V*R*V');

        % Calculo de las variables de estados
        Xk=Xk+K*(Zk-ze');

        % Calculo de la Covarianza
        Pk=(I-K*Hk)*Pk;
    




