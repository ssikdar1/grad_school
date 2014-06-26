%CS: 542
% Shan Sikdar
%
% Linear Regression Implementation:
% This started out as a Least Squares Implementation
% and then later I extended it out to a Regularized Least Squares 
%
% Basis functions are at the bottom
% to run type test(data); into the console
%
function test(data)
    % These are the different variables we want to test and see what the
    % error is
    base = [2,3,4,5,6,7,8];
    value = zeros(1,7);
    for i = base
        value(i-1) = test1(data,i);
    end
    plot(base,value);
end


function ED = test1(data,k)
    % data 13 * 10
    numData = 13;
    numFeature = 10;
    M = 7;
    %k = 2;   % 3rd colum is HW
    % target t is a colum vector
    target = zeros(13,1);
    
    % make PHI, phi_j_bar
    %Initialize the PHI Matrix, since we know the dimensions just hard code
    %them.
    PHI = zeros(13,7);
    phi0_bar = 0;phi1_bar = 0;phi2_bar = 0;phi3_bar = 0;phi4_bar = 0;
    phi5_bar = 0;phi6_bar = 0;
    t_bar = 0;
    X = zeros(13,3);

    %Fill the PHI matrix, using the basis functions, and all the vectors in
    %out data set
    for i = 1:numData
        x = zeros(1,3);
        x(1) = data(i,1);
        x(2) = data(i,9);
        x(3) = data(i,k);
        X(i,1:3) = [x(1),x(2),x(3)];
        PHI(i,1:7) = [phi0(x),phi1(x),phi2(x),phi3(x),phi4(x),phi5(x),phi6(x)];
        target(i) = data(i,10);
        phi0_bar = phi0_bar + phi0(x);
        phi1_bar = phi1_bar + phi1(x);
        phi2_bar = phi2_bar + phi2(x);
        phi3_bar = phi3_bar + phi3(x);
        phi4_bar = phi4_bar + phi4(x);
        phi5_bar = phi5_bar + phi5(x);
        phi6_bar = phi6_bar + phi6(x);
        t_bar = t_bar + target(i);
    end
    
    % This is my regularization parameter lambda
    % I tested using values of .5 ,1 , 100, 1000, 2000
    lambda = .01;
    disp(lambda);
    t_bar = t_bar / numData;
    phi0_bar = phi0_bar / numData;
    phi1_bar = phi1_bar / numData;
    phi2_bar = phi2_bar / numData;
    phi3_bar = phi3_bar / numData;
    phi4_bar = phi4_bar / numData;
    phi5_bar = phi5_bar / numData;
    phi6_bar = phi6_bar / numData;
    phi_bar = [phi0_bar,phi1_bar,phi2_bar,phi3_bar,phi4_bar,phi5_bar,phi6_bar];
%    
%     % Least Square error for Simple Gaussian: pg 142
%    PHIt = inv(transpose(PHI)*PHI)*transpose(PHI);
%    wML = PHIt * target;
%    w0 = phi_bar * wML;
   
   %Regularized Least Squares, pg 145
  % disp(transpose(PHI)*PHI);
   PHIt = inv(transpose(PHI)*PHI + lambda*eye(7))*transpose(PHI);
   wML = PHIt * target;
   w0 = phi_bar * wML; % Equation 3.19
 
    %Calculate the errors, when using regularized least squares i need to
    %additonal error term
    EDw = 0;
    for i = 1:numData
        EDw = EDw + (target(i)-w0-(wML(1)*phi1(X)+wML(2)*phi2(X)+wML(3)*phi3(X)+wML(4)*phi4(X)+wML(5)*phi5(X)+wML(6)*phi6(X)))^2;
    end
    EDw = EDw/2;
    %Regularized Least Squares Error Term, Assuming the L1 norm in this
    %case
    EDw = EDw + (lambda/2)*(wML(1) + wML(2) + wML(3) + wML(4) + wML(5) + wML(6));
   % disp(EDw)
    ED = EDw;
end

%
% These are my Polynomial Basis fun
%
function result = phi0(x)
    result = 1;
end
function result = phi1(x)
    result = x(1);
end
function result = phi2(x)
    result = x(2)^2;
end
function result = phi3(x)
    result = x(3)^3;
end
function result = phi4(x)
    result = x(1)*x(2);
end
function result = phi5(x)
    result = x(1)*x(3);
end
function result = phi6(x)
    result = x(2)*x(3);
end
