% Filtro de Kalman: Estimación posicion robot movil  
% Eduardo Zalama Casanova
% =======================================================

clear all
rand('state',sum(100*clock));
%rand('state',0);
%--------------------------------------------------------------------------
%                 Interfaz de Usuario
%--------------------------------------------------------------------------

fprintf('De los distintos tipos de Casos que se presentan a continuación:\n\n');
fprintf('1) Sensor que me da directamente las medidas\n');
fprintf('2) Sensor que me da las medidas a balizas conocidas\n\n');

caso=input('Seleccione una opción: ');


    
    


% Proceso del sistema -------------------------
Npasos=1200;

% Paso de tiempo
T=0.1;
% Cada cuantos ciclos se recibe una medidad
Nciclos=50;

% Condiciones iniciales
x=0;
y=0;
theta=0;
v=0.8;		% 0.8 Velocidad Lineal
w=0.1;	% 0.1 Velocidad angular

% desviacion error

desv_xy=0.3;%0.3
desv_theta=0.01;%0.01
desv_v=0.5;%0.5
desv_w=0.1;%0.1

%q=0.005;


Xk=[x y theta]';
Xkreal=Xk;

Pk=[1 0 0; 0 1 0; 0 0 0.1];
%Q=[10 0; 10 0];
Q=[0.01 0; 0 0.01];

Uk=[v,w]';
%R=0.01;

if caso==1  % Medidas con GPS
    Hk=[1 0 0;0 1 0; 0 0 1];% Para medidas de Gps
    V=[1 0 0;0 1 0; 0 0 1];% Para medidas de GPS
    R=[desv_xy^2 0 0;0 desv_xy^2 0;0 0 desv_theta^2]; % para medidas con GPS
    %R=[0 0 0; 0 0 0; 0 0 0];
    
elseif caso==2  % Medidas a balizas
    % Posiciones de las balizas
   
    
    xbalmin=0; % valor minimo de la coordandad x de la baliza
    ybalmin=0;    % valor minimo de la coordandad y de la baliza
    xbalmax=50;
    ybalmax=60;
    intervalx=10;  % Distancia entre balizas
    intervaly=10;
    
    numbal=0;           % numero de balizas
    for xbal=xbalmin:intervalx:xbalmax
        for ybal=ybalmin:intervaly:ybalmax
            numbal=numbal+1;
            bal(numbal,1)= xbal;  % La x
            bal(numbal,2)=ybal;   % La y
            
        end
    end
    %bal=[4 8; -6 4; 2 -10]; 
    V=1;
    %R=desv_xy^2;
    R=0.5;
    Hk=zeros(1,numbal);
end;
    


% Salvar valores
XF=zeros(Npasos,3);
ZF=zeros(Npasos,3);
XFreal=zeros(Npasos,3);
nmedidas=0;
XF(1:1,:)=Xk'; % Trayectoria estimada por filtro despues propagación y actualización si existe
	
XFreal(1:1,:)=Xkreal'; % Trayectoria Real

for k=1:Npasos
    %v=v+0.5*T*cos(k*T);
    %w=w-0.1*T*sin(k*T);
     w=0.1*sin(0.1*k*T); 
    
   % Proceso real desconocido
   Uk=[v,w]';
   Ukreal=[v*(1+(rand(1)*2-1)*desv_v),w*(1+(rand(1)*2-1)*desv_w)];
   
   Xkreal=proceso(Xkreal,Ukreal,T)';
   
   [Xk_ant,Pk_ant]=propaga(Xk,Uk,Pk,T,Q);
   
   if mod(k,Nciclos)==0 % Llega medida
   	%Zk=observa(Xkreal);
   	
    if caso==1      % Localización mediante GPS
      Zk=Xkreal+ ((rand(3,1)*2-1)'*diag([desv_xy desv_xy desv_theta]))';  % Observaciones reales
      Zek=Xk_ant;   % Observaciones estimadas
      [Xk,Pk]=actualiza(Xk_ant,Pk_ant,Hk,Zk,Zek,R,V);
      ZF(k:k,:)=Zk';
      nmedidas=nmedidas+1;
      
    elseif caso==2  % Localización mediante balizas
      for i=1:numbal  
        Zk=observaBalizas(Xkreal,bal,i)+(rand(1)*2-1)*desv_xy;         % Observaciones Reales
        Zek=observaBalizas(Xk_ant,bal,i);        % Observaciones estimadas
      
           Hk=[(Xk_ant(1)-bal(i,1))/sqrt((Xk_ant(1)-bal(i,1))^2 + (Xk_ant(2)-bal(i,2))^2) (Xk_ant(2)-bal(i,2))/sqrt((Xk_ant(1)-bal(i,1))^2 + (Xk_ant(2)-bal(i,2))^2) 0];
           [Xk,Pk]=actualiza(Xk_ant,Pk_ant,Hk,Zk,Zek,R,V); 
      end
           
    end
      
   
   else
      Xk=Xk_ant; 
      Pk=Pk_ant;
   end
	
	

	
	% Vector de observación
	%Z=Xk+ ((rand(5,1)*2-1)'*diag([desv_xy desv_xy desv_theta desv_v desv_w]))'; 

	% Guarda resultados 
	XF(k:k,:)=Xk'; % Trayectoria estimada por filtro despues propagación y actualización si existe
	
	XFreal(k:k,:)=Xkreal'; % Trayectoria Real

end
	

if caso==1      % Medidas GPS
    figure(1);
    plot(XF(:,1:1),XF(:,2:2),'r--',ZF(:,1:1),ZF(:,2:2),'r+',XFreal(:,1:1),XFreal(:,2:2),'g--')
    title('Posicion x-y');
    legend('Estimación','Medida','Real');
    xlabel('x');
    ylabel('y');
    figure(2);
    plot(1:Npasos,XF(:,3:3),'b.-',1:Npasos,ZF(:,3:3),'r+',1:Npasos,XFreal(:,3:3),'g.-');
    title('Angulo');
    legend('Estimación','Medida','Real');

elseif caso==2      % Medidas a Balizas

    figure(1);
    
    plot(bal(:,1:1),bal(:,2:2),'g*');
    hold on
    plot(XF(:,1:1),XF(:,2:2),'r--',XFreal(:,1:1),XFreal(:,2:2),'g--');
   
    title('Posicion x-y');
    legend('Posición Balizas','Estimación','Real');
    xlabel('x');
    ylabel('y');
    hold off
    figure(2);
    plot(1:Npasos,XF(:,3:3),'b.-',1:Npasos,XFreal(:,3:3),'g.-');
    title('Angulo');
    legend('Estimación','Real');
end
    


