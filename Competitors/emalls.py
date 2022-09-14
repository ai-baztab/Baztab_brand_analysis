import numpy as np

# a = ["1","2","3","4","5","6","7","8","9"]
# a = np.reshape(a,(3,3))
# l = ["new","new","new"]
# new = np.concatenate((a,l), axis =1)
# print(new[0,:])

a = np.reshape([None, None, None, None], (2, 2))
a[0,0] = 'None'
a[1,1] = 2
a[0,1] = 'sad'
print(a)
