library(autoencoder)

#training data rows are examples and columns are input channels
training.matrix	<- as.matrix(read.csv(file="C:\\Users\\Shan\\Documents\\GitHub\\grad_school\\research\\datasets\\sparseAuto_train.csv", sep=",", header=FALSE)) 
# a matrix used for testing the trained autoencoder
testing.matrix	<- as.matrix(read.csv(file="C:\\Users\\Shan\\Documents\\GitHub\\grad_school\\research\\datasets\\sparseAuto_test.csv", sep=",", header=FALSE))					
nl = 3						# number of layers 
N.hidden = 1				#vector for number of nodes in each hidden layer
unit.type = "tanh"			#activation function
lambda = 0.0002				#weight decay
beta = 6					#sparsity penalty term
rho = 0.01					#desired sparsity
epsilon <- 0.001			#small parameter for initialization of wieghts
max.iterations = 3000		#number of iterations in optimizer
# optim.method 
# rescaling.offset

autoencoder.object <- autoencode(X.train=training.matrix, nl=nl,N.hidden=N.hidden,
unit.type=unit.type,lambda=lambda,beta=beta,rho=rho,epsilon=epsilon,
optim.method="BFGS",max.iterations=max.iterations,
rescale.flag=TRUE,rescaling.offset=0.001)



## Extract weights W and biases b from autoencoder.object:
W <- autoencoder.object$W
b <- autoencoder.object$b
mean.error.training.set <- autoencoder.object$mean.error.training.set
mean.error.test.set <- autoencoder.object$b

print(W)
print(b)
print("ERRORS")
print(mean.error.training.set)
print(mean.error.test.set)