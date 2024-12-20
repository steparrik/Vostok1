import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Константы
m0 = 10000
M = m0 + 24000
Ft = 1609220  # тяга
Cf = 0.2  # коэффициент лобового сопротивления
ro = 1.225  # плотность воздуха (кг/м^3)
S = 18.4  # площадь поперечного сечения (м^2)
g = 9.80665  # ускорение свободного падения (м/с^2)
k = (M - m0) / (3 * 60 + 90)  # скорость изменения массы

# Функции для расчета массы и ускорения
def mass(t):
    return M - k * t

def acceleration(v, m):
    drag = 0.5 * Cf * ro * v**2 * S
    return (Ft - m * g - drag) / m

# Система дифференциальных уравнений
def equations(t, y):
    v, h = y
    m = mass(t)
    a = acceleration(v, m)
    return [a, v]  # [dv/dt, dh/dt]

# Начальные условия
y0 = [0, 0]  # начальная скорость и начальная высота
t_span = (0, 45)  # интервал времени
t_eval = np.arange(0, 45, 0.1)  # моменты времени для вывода решения

# Решение задачи с помощью
# solve_ivp
solution = solve_ivp(equations, t_span, y0, t_eval=t_eval)

# Извлечение результатов
times = solution.t
velocities = solution.y[0]
heights = solution.y[1]
masses = mass(times)

# Построение графиков
plt.figure(figsize=(12, 8))

# График скорости
plt.subplot(3, 1, 1)
plt.plot(times, velocities, label="Скорость", color="blue")
plt.xlabel("Время (с)")
plt.ylabel("Скорость (м/с)")
plt.title("Скорость от времени")
plt.grid()
plt.legend()

# График высоты
plt.subplot(3, 1, 2)
plt.plot(times, heights, label="Высота", color="green")
plt.xlabel("Время (с)")
plt.ylabel("Высота (м)")
plt.title("Высота от времени")
plt.grid()
plt.legend()

# График массы
plt.subplot(3, 1, 3)
plt.plot(times, masses, label="Масса", color="red")
plt.xlabel("Время (с)")
plt.ylabel("Масса (кг)")
plt.title("Масса от времени")
plt.grid()
plt.legend()

plt.tight_layout()
plt.show()
