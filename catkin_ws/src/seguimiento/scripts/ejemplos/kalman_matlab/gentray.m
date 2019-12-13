% Eduardo Zalama Casanova
% =======================================================

rand('state',sum(100*clock));

% Proceso del sistema -------------------------
Npasos=80;

% Paso de tiempo
T=0.5;
tiempo=0.0;
% Cada cuantos ciclos se recibe una medidad

% Condiciones iniciales
x=0;
y=0;
theta=0;
v=0.5;		% Velocidad Lineal m/s
w=0.02;	% Velocidad angular rad/s

Xk=[x y theta]';
U=[v,w];
% desviacion error

desv_xy=0.1;
desv_theta=0.017;;

% Salvar valores
XF=zeros(Npasos,3);
ZF=zeros(Npasos,3);
ZE=zeros(Npasos,3);
TF=zeros(Npasos,1);

XFreal=zeros(Npasos,3);
nmedidas=0;
for k=1:Npasos
   % Proceso real desconocido
   
   Xk=proceso(Xk,U,T)';
   tiempo=tiempo+T;
   TF(k)=tiempo;
   
   XF(k:k,:)=Xk';
      
  	Zk=Xk+ ((rand(3,1)*2-1)'*diag([desv_xy desv_xy desv_theta]))';
   ZF(k:k,:)=Zk';
     
   % Estimación de velocidad
   j=70;	% Numero de pasos anteriores sobre los que se realiza el ajuste
   desp=0;
   ang=0;
   
   if k>j
      [PX,S1]=polyfit(TF(k-j:k),ZF(k-j:k,1),2);
      [PY,S1]=polyfit(TF(k-j:k),ZF(k-j:k,2),2);
   else 
      [PX,S1]=polyfit(TF(1:k),ZF(1:k,1),2);
      [PY,S1]=polyfit(TF(1:k),ZF(1:k,2),2);
	end

      xe=polyval(PX,tiempo);
      ye=polyval(PY,tiempo);
      ZE(k:k,1)=xe;
      ZE(k:k,2)=ye;
      
   desp=0.0;   
   if k>j 
      for l=0:j-1
            	desp=desp+sqrt( (ZE(k-l,1)-ZE(k-l-1,1)) * (ZE(k-l,1)-ZE(k-l-1,1))+ (ZE(k-l,2)-ZE(k-l-1,2))*(ZE(k-l,2)-ZE(k-l-1,2)));
      end
		vest=desp/(tiempo-TF(k-j))

   elseif k>1
     for l=0:k-2
            	desp=desp+sqrt( (ZE(k-l,1)-ZE(k-l-1,1)) * (ZE(k-l,1)-ZE(k-l-1,1))+ (ZE(k-l,2)-ZE(k-l-1,2))*(ZE(k-l,2)-ZE(k-l-1,2)));
     end
	  vest=desp/(tiempo-TF(1))

   end
          %atan2(ZF(k,2)-ZF(k-l-1,2),ZF(k,1)-ZF(k-l-1,1))

   %      ang=ang+atan2(ZF(k-l,2)-ZF(k-l-1,2),ZF(k-l,1)-ZF(k-l-1,1));
   %	desp=desp+sqrt( (ZE(k-l,1)-ZE(k-l-1,1)) * (ZE(k-l,1)-ZE(k-l-1,1))+ (ZE(k-l,2)-ZE(k-l-1,2))*(ZE(k-l,2)-ZE(k-l-1,2)));
         %desp=desp+sqrt( (XF(k-l,1)-XF(k-l-1,1)) * (XF(k-l,1)-XF(k-l-1,1))+ (XF(k-l,2)-XF(k-l-1,2))*(XF(k-l,2)-XF(k-l-1,2)));

			

   
    %  vestr=sqrt( (ZF(k,1)-ZF(k-j,1)) * (ZF(k,1)-ZF(k-j,1))+ (ZF(k,2)-ZF(k-j,2))*(ZF(k,2)-ZF(k-j,2)))/(tiempo-TF(k-j));
	%[P,S]=polyfit(ZF(k-j:j,1),ZF(k-j:j,1),2);

     % wang=ang/(tiempo-TF(k-j));

	
end


[PX,S1]=polyfit(TF,ZF(:,1),2);
[PY,S1]=polyfit(TF,ZF(:,2),2);
X=polyval(PX,TF');
Y=polyval(PY,TF');

figure(1);

%plot(XF(:,1:1),XF(:,2:2),'b+-',ZF(:,1:1),ZF(:,2:2),'r.',ZE(:,1:1),ZE(:,2:2),'g.-',X,Y,'m.-');
plot(XF(:,1:1),XF(:,2:2),'b+-',ZF(:,1:1),ZF(:,2:2),'r.',ZE(:,1:1),ZE(:,2:2),'g.--');
%axis([5 15 0 2]);

title('Posicion x-y');
legend('Teorico','Medida','Estimación');
figure(2);
plot(1:Npasos,XF(:,3:3),'b+-',1:Npasos,ZF(:,3:3),'r.');
title('Angulo');
legend('Teorico','Medida','Estimación');
