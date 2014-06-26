nu = 10;
beta = 10; %changing Beta from 1 to 1000 same accuracy why?
h = 1;

%
% TODO- Should I switch to using the binary images that were provided or
% keep this?
%
%

img = imread('Bayes-noise.png'); % The original noisy image
gray = rgb2gray(img); %grayscale
binary = im2bw(gray); % 0 and 1's
Y = binary.*2-1; % Changing 1,0 to 1,-1

%
% Coordinate Descent Algorithm
% 1. Initialize {x_i}. x_i = y_i
% 2. Loop over {X_i}. For each x_i fix the nieghborhood and see whether
% -x_i would decrease the energy. If so then flip x_i otherwise continue
%3. Stop when no changes can be made for X.

X = Y; % Initializing {x_i}
final_energy = 0; %initialize final energy function

[rows,cols] = size(X);

iterate = 1;
ctr = 0;
while(iterate)
    ctr = ctr + 1;
    %set it to false
    iterate = 0;
    
    for i = 1:rows
       for j= 1:cols
           x_i = X(i,j);
           y_i = Y(i,j);
           flip = -1*x_i;

           top_neighbor = 0;
           bottom_neighbor = 0;
           left_neighbor = 0;
           right_neighbor = 0;
           %Use if conditions to grab the pixels 2-4 neighbors?
           if(i > 1)
                top_neighbor = X(i-1,j);
           end

           if(i < rows)
               bottom_neighbor = X(i+1,j);
           end

           if(j > 1)
              left_neighbor = X(i,j-1); 
           end

           if(j < cols)
               right_neighbor = X(i, j+1);
           end

           %Energy Term for the neighbor cliques
           E1 = -beta*(x_i* top_neighbor + x_i*bottom_neighbor + x_i*left_neighbor + x_i*right_neighbor);
           E2 = -beta*(flip* top_neighbor +flip*bottom_neighbor +flip*left_neighbor + flip*right_neighbor);

           %Energy Term for the x_i y_i clique
           E1 = E1 + -nu * x_i * y_i;
           E2 = E2 + -nu*flip*y_i;

           %Energy Term as to bias the model towards one sign.
           E1 = E1 + h * x_i;
           E2 = E2 + h * flip;

           %Does fliping the sign of x_i result in lower energy? If so flip the
           %sign Homes.
           if(E2 < E1)
                X(i,j) = flip;
                %we stop only when no more changes can be made to X.
                %since I set iterate to false above set it to true if a
                %change has been made
                iterate = 1;
           end
       end
    end
end
disp(ctr);
%Upload the Good picture, convert to grayscale, then binary
img = imread('Bayes.png'); % The original noisy image
gray = rgb2gray(img); %grayscale
binary = im2bw(gray); % 0 and 1's
answer = binary.*2-1; % Changing 1,0 to 1,-1

%Now loop through the answer and my X matrix and see how many are correct
numCorrect = 0;
for i = 1:rows
   for j= 1:cols
       if(X(i,j) == answer(i,j))
           numCorrect = numCorrect + 1;
       end
   end
end

%divide the number correct by the number of pixels (aka the number of
%indexes)
accuracy = numCorrect/(rows*cols);
disp(accuracy);
imwrite(X,'Output.png');