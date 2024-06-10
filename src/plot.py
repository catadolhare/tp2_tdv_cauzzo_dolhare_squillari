import matplotlib.pyplot as plt
import numpy as np

cant_viajes = [140, 15, 21, 17]
vagones = [48, 15, 15, 5]

coefficients = np.polyfit(cant_viajes, vagones, 1)  # 1 means linear fit (degree 1)
slope = coefficients[0]
intercept = coefficients[1]
best_fit_line = np.polyval(coefficients, cant_viajes)

plt.plot(cant_viajes, best_fit_line, color='red')

plt.scatter(cant_viajes, vagones)
plt.xlabel('Cantidad de viajes')
plt.ylabel('Cantidad de vagones')
plt.title('Cantidad de vagones necesarios para cada cantidad de viajes')

plt.show()