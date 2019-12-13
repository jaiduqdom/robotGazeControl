

function [Xk, Pk] = actualiza(Xk,Pk,Hk,Zk,Zek,R,V)

I=[1 0 0; 0 1 0; 0 0 1];

%Hk=[1 0 0;0 1 0; 0 0 1];% Para medidas de Gps
%V=[1 0 0;0 1 0; 0 0 1];% Para medidas de GPS

K=Pk*Hk'*inv(Hk*Pk*Hk'+V*R*V');

%K=[0 0 0; 0 0 0; 0 0 0];
Zk
Zek
Xk=Xk+K*(Zk-Zek);
Pk=(I-K*Hk)*Pk;

