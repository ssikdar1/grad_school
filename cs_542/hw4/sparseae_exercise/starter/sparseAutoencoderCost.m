function [cost,grad] = sparseAutoencoderCost(theta, visibleSize, hiddenSize, ...
                                             lambda, sparsityParam, beta, data)

% visibleSize: the number of input units (probably 64) 
% hiddenSize: the number of hidden units (probably 25) 
% lambda: weight decay parameter
% sparsityParam: The desired average activation for the hidden units (denoted in the lecture
%                           notes by the greek alphabet rho, which looks like a lower-case "p").
% beta: weight of sparsity penalty term
% data: Our 64x10000 matrix containing the training data.  So, data(:,i) is the i-th training example. 
  
% The input theta is a vector (because minFunc expects the parameters to be a vector). 
% We first convert theta to the (W1, W2, b1, b2) matrix/vector format, so that this 
% follows the notation convention of the lecture notes. 

W1 = reshape(theta(1:hiddenSize*visibleSize), hiddenSize, visibleSize);
W2 = reshape(theta(hiddenSize*visibleSize+1:2*hiddenSize*visibleSize), visibleSize, hiddenSize);
b1 = theta(2*hiddenSize*visibleSize+1:2*hiddenSize*visibleSize+hiddenSize);
b2 = theta(2*hiddenSize*visibleSize+hiddenSize+1:end);

% Cost and gradient variables (your code needs to compute these values). 
% Here, we initialize them to zeros. 
cost = 0;
W1grad = zeros(size(W1)); 
W2grad = zeros(size(W2));
b1grad = zeros(size(b1)); 
b2grad = zeros(size(b2));

%% ---------- YOUR CODE HERE --------------------------------------
%  Instructions: Compute the cost/optimization objective J_sparse(W,b) for the Sparse Autoencoder,
%                and the corresponding gradients W1grad, W2grad, b1grad, b2grad.
%
% W1grad, W2grad, b1grad and b2grad should be computed using backpropagation.
% Note that W1grad has the same dimensions as W1, b1grad has the same dimensions
% as b1, etc.  Your code should set W1grad to be the partial derivative of J_sparse(W,b) with
% respect to W1.  I.e., W1grad(i,j) should be the partial derivative of J_sparse(W,b) 
% with respect to the input parameter W1(i,j).  Thus, W1grad should be equal to the term 
% [(1/m) \Delta W^{(1)} + \lambda W^{(1)}] in the last block of pseudo-code in Section 2.2 
% of the lecture notes (and similarly for W2grad, b1grad, b2grad).
% 
% Stated differently, if we were using batch gradient descent to optimize the parameters,
% the gradient descent update to W1 would be W1 := W1 - alpha * W1grad, and similarly for W2, b1, b2. 
% 

[rows,columns] = size(data);
% m = columns; % number of traning examples
m=10000; %using this to test faster
s2 = hiddenSize; % number of nodes in layer2

rho1 = zeros(hiddenSize,1);
for i = 1:m
    x = data(:,i);
    a2 = sigmoid(W1*x + b1);
    rho1 = rho1 + a2;
end
rho1 = rho1/m;

%
% Backward propogation pg 9
%
for i = 1:m

    % Feedforward pass
    x = data(:,i);
    a2 = sigmoid(W1*x + b1);     % (25 x 64) (64 x 1) + (25x1) = 25 x 1
    a3 = sigmoid(W2*a2+b2);     % (64 x 25) x (25 x 1) + (64 x 1) = (64 x 1)

    cost = cost + 1/2 * (norm((a3 - x)))^2;  %1st term of the cost function on page 6
    %cost = cost/2;
    delta3 = -(x-a3).*(a3.*(1-a3));     %2. Calculate the output layer


    %3. For l= nl-1, nl-2, nl-3,....2
     % With the sparsity param pg 16
   delta2 = ((W2'*delta3) + (beta*((-sparsityParam./rho1)+(1-sparsityParam)./(1-rho1)))).*(a2.*(1-a2));
%    delta2 = (W2'*delta3).*(a2.*(1-a2)); %Without the sparsity param
    
    %4. Compute the desired partial derivatives add to the running total or W1grab a
    W1grad = W1grad + delta2*x';
    W2grad = W2grad+ delta3*a2';
    b1grad = b1grad+ delta2;
    b2grad = b2grad+ delta3;
end

W1grad = W1grad/m + lambda * W1;
W2grad = W2grad/m + lambda * W2;
b1grad = b1grad/m;
b2grad = b2grad/m;

%divide J by number of samples
cost = cost/m;
%add the regularization term to cost (pg 6)
cost = cost + (lambda/2)*(sum(sum(W1.^2))+sum(sum(W2.^2)));


% Calculate the third term in order to implement J_Sparse
 
penalty = 0;
for j=1:s2    
    rho_hat_j = rho1(j);
    % Kullback - Leibler Divergence
     KL = sparsityParam*log(sparsityParam/rho_hat_j) + (1-sparsityParam)*log((1-sparsityParam)/(1-rho_hat_j));
     penalty = penalty + KL;  
end
% %J_sparse(W,b) = J(W,b,data) + beta * penalty; 
cost = cost + beta * penalty; 



%-------------------------------------------------------------------
% After computing the cost and gradient, we will convert the gradients back
% to a vector format (suitable for minFunc).  Specifically, we will unroll
% your gradient matrices into a vector.

grad = [W1grad(:) ; W2grad(:) ; b1grad(:) ; b2grad(:)];

end

%-------------------------------------------------------------------
% Here's an implementation of the sigmoid function, which you may find useful
% in your computation of the costs and the gradients.  This inputs a (row or
% column) vector (say (z1, z2, z3)) and returns (f(z1), f(z2), f(z3)). 

function sigm = sigmoid(x)
    sigm = 1 ./ (1 + exp(-x));
end

