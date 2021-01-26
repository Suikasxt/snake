import numpy as np
counter = 0
for n in [[20,20,100]]:
    for j in range(10):
        f = open('%02d.in'%counter, 'w')
        f.write('%d %d %d\n'%(n[0], n[1], n[2]))
        for i in range(n[2]):
            f.write('%d %d\n'%(np.random.randint(n[0]), np.random.randint(n[1])))
        f.close()
        counter+=1
