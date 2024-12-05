import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from scipy import constants

# Данные с Кербина
m0 = 10000
M = m0 + 24000
Ft = 1609220
Cf = 0.2
ro = 1.225
S = 18.4
g = 1.00034 * constants.g
k = (M - m0) / (3 * 60 + 90)

def A(t):
    return (Ft / (M - k * t))


def B(t):
    return ((Cf * ro * S) / (2 * (M - k * t)))


def dv_dt(t, v):
    return (A(t) - B(t) * v ** 2 - g)


# Начальная скорость
v0 = 0

# Время интеграции
t = np.linspace(0, 45, 50)

# Решение уравнения
solve = integrate.solve_ivp(dv_dt, t_span=(0, max(t)), y0=[v0], t_eval=t)

# Данные для построения графика
x = solve.t
y = solve.y[0]

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(x, y, color="royalblue", linestyle="--", linewidth=2, label="Скорость ракеты v(t)")
plt.title("Зависимость скорости от времени (Данные с Кербина)", fontsize=14, fontweight="bold")
plt.xlabel("Время, с", fontsize=12)
plt.ylabel("Скорость, м/с", fontsize=12)
plt.legend(loc="best", fontsize=10)
plt.grid(True, linestyle="--", alpha=0.7)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.show()
