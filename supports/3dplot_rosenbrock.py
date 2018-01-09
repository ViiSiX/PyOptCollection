import numpy as np
from matplotlib import cm, pyplot as plt
from matplotlib.ticker import LinearLocator
from mpl_toolkits.mplot3d import Axes3D
from py_opt_collection.test_functions import ROSENBROCK as OptTarget


fig = plt.figure()
ax = fig.gca(projection='3d')

# Make data.
X, Y = np.meshgrid(
    np.linspace(
        OptTarget['optimization'].boundaries[0][0],
        OptTarget['optimization'].boundaries[0][1],
        100
    ),
    np.linspace(
        OptTarget['optimization'].boundaries[1][0],
        OptTarget['optimization'].boundaries[1][1],
        100
    ),
)
Z = (lambda x, y: OptTarget['optimization'].func([x, y]))(X, Y)

# Gradient color
Gx, Gy = np.gradient(Z)
G = (Gx**2+Gy**2)**.15
N = G/G.max()

surf = ax.plot_surface(X, Y, Z,
                       facecolors=cm.jet(N),
                       linewidth=0, antialiased=False)

# Customize the axises.
ax.zaxis.set_major_locator(LinearLocator(10))

plt.xlabel('X axis (-3, 3)')
plt.ylabel('Y axis (-3, 3)')
plt.title('Plot of Rosenbrock function.', y=-0.1)
plt.show()
