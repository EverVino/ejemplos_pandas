import numpy as np
import matplotlib.pyplot as plt 

from matplotlib.animation import FuncAnimation

dx = dy = 10
dt = 10 # dt/2 = 5
x = np.linspace(0,40,20)
y = np.linspace(0,40,20)
t = np.arange(0, 5000 + dt, dt)

nx, ny = len(x), len(y)
nt  = len(t)

k = 0.835
lmbd = k*dt/dx/dt 
T_sup = 100
T_der = 50
T_izq = 75
T_inf = 0

Txyt = np.zeros((nx, ny))
Txy = np.zeros((ny, nx))

Txy[:,0] = T_izq
Txy[:,-1] = T_der 
Txy[0] =  T_sup 
Txy[-1] = T_inf

M = 2*(1+lmbd)*np.eye(nx-2)
#print(M)
R = np.zeros(nx-2)
for i in range(1, nx-2):
    M[i-1, i] = -lmbd 
    M[i, i-1] = -lmbd 
#print(M)
Txy0 = np.copy(Txy)
Txy05 = np.copy(Txy)
M_inv = np.linalg.inv(M)
ans = []
ans.append(Txy)
for t in range(nt):
    Txy0 = np.copy(Txy)
    Txy05 = np.copy(Txy)
    for i in range(1,ny-1):
        
        for j in range(nx-2,0,-1):
            if j == 1:
                R[j-1] = lmbd*Txy05[j-1,i]+lmbd*Txy0[j,i-1]+2*(1-lmbd)*Txy0[j,i]+lmbd*Txy0[j,i+1]
                
            elif j == nx-2:
                R[j-1] = lmbd*Txy0[j,i-1]+2*(1-lmbd)*Txy0[j,i]+lmbd*Txy0[j,i+1]+lmbd*Txy05[j+1,i]
            else:
                R[j-1] = lmbd*Txy0[j,i-1]+2*(1-lmbd)*Txy0[j,i]+lmbd*Txy0[j,i+1]
        
        X = M_inv@R.T
        Txy05[1:ny-1,i] = X

    for j in range(1,ny-1):
        for i in range(1, nx-1):
            if i == 1:
                R[i-1] = lmbd*Txy[j,i-1]+lmbd*Txy05[j-1,i]+2*(1-lmbd)*Txy05[j,i]+lmbd*Txy05[j+1,i]
            elif i == nx-2:
                R[i-1] = lmbd*Txy05[j-1,i]+2*(1-lmbd)*Txy05[j,i]+lmbd*Txy05[j+1,i]+ lmbd*Txy[j,i+1]
            else:
                R[i-1] = lmbd*Txy05[j-1,i]+2*(1-lmbd)*Txy05[j,i]+lmbd*Txy05[j+1,i]
        #print(R)
        X = M_inv@R.T
        Txy[j,1:ny-1] = X
    
    ans.append(np.copy(Txy))

levels = np.linspace(-1, 101, 50)
#plt.contourf(x,y,z, levels = levels, cmap = "YlOrRd")

#plt.show()
#print("done")

fig, ax = plt.subplots()
xdata, ydata, Tdata = [], [], []
ln = plt.contourf(x, y, ans[0], levels = levels, cmap = "coolwarm")
#ln.contourf.set(xlim=(0,1), ylim=(0,1))
print(ans[nt-1])
def init():
    ax.set_xlim(0, 40)
    ax.set_ylim(0, 40)
    ax.set_title('Temp XY', fontsize = 20)
    return ln

def animate(i):
    zdata = ans[i]
    ax.set_title(f"Temp XY {i}")
    ln = plt.contourf(x, y, zdata, levels = levels, cmap = "coolwarm")
    return ln

time = 0
ani = FuncAnimation(fig, animate, interval = 200, frames=nt, init_func=init, blit=False)
plt.show()

