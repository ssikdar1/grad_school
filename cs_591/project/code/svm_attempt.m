clear
label_column_num =30;
TrainingSet = csvread('train.csv');
GroupTrain = TrainingSet(:,label_column_num);
TrainingSet(:,label_column_num) = [];

TestSet = csvread('test.csv');
Test_Classes = TestSet(:,label_column_num);
TestSet(:,label_column_num) = [];


% %
% % Normalize to z-scores
% %
% %
% TrainingSet = zscore(TrainingSet);
% TestSet = zscore(TestSet);

results = multisvm(TrainingSet, GroupTrain, TestSet); 
[numAnswers, foo] =size(results); 
numCorrect = 0;
for i=1:numAnswers
    if(results(i) == Test_Classes(i))
         numCorrect = numCorrect + 1;
    end
end
disp(numCorrect)
disp(numAnswers)
accuracy = numCorrect/numAnswers;
disp(accuracy);


