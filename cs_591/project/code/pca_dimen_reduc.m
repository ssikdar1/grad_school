% Use PCARES function to do that:
% 
% [residuals,reconstructed] = pcares(X,ndim)
% 
% The 'reconstructed' will have the reduced dimensions data based on the ndims input. Note that 'reconstructed' will still be the original dimension. You can choose the first ndims if you'd like.
% 
% If you want the reduced dimensions in the new basis then just take the first ndims of the SCORE variable
% 
% SCORE(:,1:ndims)
% 
% [COEFF,SCORE] = princomp(X)

%data = csvread('C:\Users\Shan\Documents\GitHub\grad_school\cs_591\project\superdataset.csv');
%[COEFF, SCORE, LATENT] = princomp(X)
%Coeff contains the first princp components.
%Latent contains the variances: PLOT this to get a cool looking graph
%Score is the new data we want I think
%Choose the first ndimensions
%dimension_reduced = SCORE(:,1:ndims)
% ndims = 10
% [COEFF, SCORE, LATENT] = princomp(zscore(X))
% dimension_reduced = SCORE(:,1:ndims)
