function [Xk_, Pk_]= propaga(Xk, Uk, Pk, T, Q)
    A=[1,0,-Uk(1)*T*sin(Xk(3));0,1,Uk(1)*T*cos(Xk(3));0,0,1];
    W=[T*cos(Xk(3)),0;T*sin(Xk(3)),0;0,T];
    
    Xk_(1) = Xk(1)+(Uk(1)*T*cos(Xk(3)));
    Xk_(2) = Xk(2)+(Uk(1)*T*sin(Xk(3)));
    Xk_(3) = Xk(3)+Uk(2)*T;
    
    Xk_ = Xk_';
    Pk_ = A*Pk*A' + W*Q*W';
end
    