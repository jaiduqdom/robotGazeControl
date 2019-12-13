function [Zk] = observaBalizas(Xk,bal,i)
   
    Zk=sqrt((Xk(1)-bal(i,1))^2+(Xk(2)-bal(i,2))^2);
   

