from unicodedata import ucd_3_2_0
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation

import csv
L = 1
u0t = 1
ult = 0
ux0 = 0
x = np.linspace(0, L, 500)
dx = x[1]-x[0]
t = np.linspace(0, 1, 500)
dt = t[1]-t[0]

nx = len(x)
nt = len(t)
u = np.zeros((nt,nx))
u[0,:] = ux0

u[:,-1] = ult
u[:,0] = u0t
alfa, beta = dt/2/dx**2, 0.005
with open("ini_u.csv", "w") as csvfile:
    writer = csv = csv.writer(csvfile)
    for line in u:
        writer.writerow(line)

M = (1+2*alfa)*np.eye(nx-2)
#print(M)

for i in range(1,nx-2):
    M[i-1, i] = -alfa 
    M[i, i-1] = -alfa 


R = np.zeros(nx-2)  # To review

for l in range(1, nt):
    for i in range(1,nx-1):
        if i == 1:
            R[i-1] = alfa*u[l-1,i+1]+ (1-2*alfa-beta**2)*u[l-1,i]+alfa*u[l-1,i-1]+alfa*u[l,i-1]
            #print("ini")
        elif i == nx-2: # Rev
            R[i-1] = alfa*u[l-1,i+1]+ (1-2*alfa-beta**2)*u[l-1,i]+alfa*u[l-1,i-1]+alfa*u[l,i-1]
            #print("final")
        else:
            R[i-1] = alfa*u[l-1,i+1]+ (1-2*alfa-beta**2)*u[l-1,i]+alfa*u[l-1,i-1]
            #print("medio")
    
    X = np.linalg.inv(M)@R.T
    #print(len(X))
    u[l,1:nx-1] = X
    #print(X)

y = np.linspace(0,1,4)

z = np.array([u[0,:], u[0,:], u[0,:], u[0,:]])

levels = np.linspace(z.min(), z.max(), 50)
#plt.contourf(x,y,z, levels = levels, cmap = "YlOrRd")

#plt.show()
#print("done")

fig, ax = plt.subplots()
xdata, ydata, zdata = [], [], []
ln = plt.contourf(x, y, z, levels = levels, cmap = "YlOrRd")
#ln.contourf.set(xlim=(0,1), ylim=(0,1))

def init():
    ax.set_xlim(0, 1)
    ax.set_ylim(-1, 1)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(r'$\frac{\partial u}{\partial t}=\frac{\partial^2 u}{\partial x^2}-\beta u $', fontsize = 20)
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    return ln

def animate(i):
    zdata = np.array([u[i,:], u[i,:], u[i,:], u[i,:]])
    tiempo = i
    #ax.set_title(f"Tiempo{i}")
    ln = plt.contourf(x, y, zdata, levels = levels, cmap = "YlOrRd")
    
    
    return ln

time = 0
ani = FuncAnimation(fig, animate, interval = 50, frames=len(u), init_func=init, blit=False)
plt.show()







