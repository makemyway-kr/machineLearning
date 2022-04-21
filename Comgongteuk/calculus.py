import numpy as np
def numerical_derivative(f,x):
    delta_x = 1e-4
    grad = np.zeros_like(x)
    print("debug 1. initial input variable = ",x)
    print("debug 2. initial input variable = ",grad)
    print("==========================================")
    it = np.nditer(x,flags=['multi_index'], op_flags = ['readwrite'] )
    
    while not it.finished:
        idx = it.multi_index
        print("debug3. idx = ",idx,",x[idx] = ", x[idx])
        tmp_val = x[idx]
        x[idx] = float(tmp_val) + delta_x
        fx1 = f(x)
        
        x[idx] = float(tmp_val) - delta_x
        fx2 = f(x)
        grad[idx] = (fx1 - fx2) / (2*delta_x)
        print("debug4. grad[idx] = ", grad[idx])
        print("debug5. grad[idx] =",grad)
        print("===================================")
        x[idx] = tmp_val
        it.iternext()
    return grad
#2번문제
def func1(W):
    x = W[0]
    y = W[1]
    return (x*2) + (3*x*y) + y**3
f = lambda W : func1(W)
W = np.array([1.0,2.0])
ret = numerical_derivative(f,W)
print('type(ret) = ',type(ret),',ret_val = ',ret)

#3번문제
def func2(W):
    w = W[0][0]
    x = W[0][1]
    y = W[1][0]
    z = W[1][1]
    return w*x + x*y*z + 3*w + z*(y**2)

Z = np.array([[1.0,2.0],[3.0,4.0]])
f2 = lambda Z : func2(Z)
ret2 = numerical_derivative(f2,Z)
print('type(ret) = ', type(ret2) , ',ret_val = ',ret2 )
