import numpy as np
#Xk = np.arange(10)
Xk = [10]
Xk[0] = np.transpose(np.matrix([5, 6]))
print(Xk[0][0].item())
