from math import ceil, exp, tanh
from random import random

# sigmoid activation function
def sigmoid(x):
    return tanh(x)

def dsigmoid(x):
    return 1.0 - x ** 2

# returns a network trained with the specified dataset, number of iterations,
# learning rate and momentum
def nn(ds, n, r, m):
    # derive number of neurons in input, hidden and output layers
    ni = len(ds[0][0]) + 1
    nh = int(ceil((len(ds[0][0]) + len(ds[0][1])) / 2.0))
    no = len(ds[0][1])
    # input weights
    wi = []
    for i in range(ni):
        w = []
        for j in range(nh):
            w.append(random())
        wi.append(w)
    # output weights
    wo = []
    for i in range(nh):
        w = []
        for j in range(no):
            w.append(random())
        wo.append(w);
    # input weights change
    ci = []
    for i in range(ni):
        ci.append([0.0] * nh)
    # output weights change
    co = []
    for i in range(nh):
        co.append([0.0] * no)
    # hidden activations
    ah = [1.0] * nh
    # output activations
    ao = [1.0] * no
    # hidden deltas
    dh = [0.0] * nh
    # output deltas
    do = [0.0] * no
    # train
    for i in range(n):
        e = 0.0
        for d in ds:
            # forward-propagate
            ai = d[0] + [1.0]
            fp(wi, wo, ai, ah, ao)
            # back-propagate
            for j in range(no):
                d = d[1][j] - ao[j]
                do[j] = dsigmoid(ao[j]) * d
                e += 0.5 * d ** 2
            for j in range(nh):
                d = 0.0
                for k in range(no):
                    d += do[k] * wo[j][k]
                dh[j] = dsigmoid(ah[j]) * d
            for j in range(nh):
                for k in range(no):
                    c = do[k] * ah[j]
                    wo[j][k] += r * c + m * co[j][k]
                    co[j][k] = c
            for j in range(ni):
                for k in range(nh):
                    c = dh[k] * ai[j]
                    wi[j][k] += r * c + m * ci[j][k]
                    ci[j][k] = c
        print(e)
    return wi, wo, ai, ah, ao

def fp(wi, wo, ai, ah, ao):
    #print('wi', wi)
    #print('wo', wo)
    ni = len(wi)
    nh = len(wi[0])
    no = len(wo[0])
    for i in range(nh):
        x = 0.0
        for j in range(ni):
            x += ai[j] * wi[j][i]
        ah[i] = sigmoid(x)
    for i in range(no):
        x = 0.0
        for j in range(nh):
            x += ah[j] * wo[j][i]
        ao[i] = sigmoid(x)
    print(ai, ao)
    return ao

# validates the specified network with the specified dataset
def v(nn, ds):
    return

# returns test dataset
def tds():
    return [
        [[0,0], [0]],
        [[0,1], [1]],
        [[1,0], [1]],
        [[1,1], [0]]
    ]

# returns validation dataset
def vds():
    return [
        [[0,0], [0]],
        [[0,1], [1]],
        [[1,0], [1]],
        [[1,1], [0]]
    ]

# train and validate
v(nn(tds(), 1000, 0.5, 0.1), vds())
