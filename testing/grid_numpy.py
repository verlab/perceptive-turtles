import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 4*np.pi, 100)
x = np.cos(3 * t)
y = np.sin(t)

gridx = np.linspace(-1, 1, 5)
gridy = np.linspace(-1, 1, 5)

grid, _, _ = np.histogram2d(x, y, bins=[gridx, gridy])

plt.figure()
plt.plot(x, y, 'ro')
plt.grid(True)

plt.figure()
plt.pcolormesh(gridx, gridy, grid)
plt.plot(x, y, 'ro')
plt.colorbar()

plt.show()