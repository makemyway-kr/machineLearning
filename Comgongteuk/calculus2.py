import numpy as np
def mi_bun(f,W):
    results = np.zeros_like(W)
    delta_x = 1e-4
    it = np.nditer(W,flags = ['multi_index'] , op_flags = ['readwrite'])
    while not it.finished:
            idx = it.multi_index
            temp_val = W[idx]
            W[idx] = float(temp_val) + delta_x 
            fx1 = f(W)
            W[idx] = float(temp_val) - delta_x
            fx2 = f(W)
            results[idx] = (fx1 - fx2) / (2*delta_x)
            W[idx] = temp_val
            it.iternext()
    return results

def function1(w):
    return (w[0]**2) + (2*w[0]*w[1]) + (w[1]**2)

f = lambda w : function1(w)

w = np.array([9.0 , 7.0])

print(mi_bun(f,w))