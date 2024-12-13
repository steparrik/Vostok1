import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.constants import g

# Данные с Кербина
m0 = 10000
M = m0 + 24000
Ft = 1609220  # тяга
Cf = 0.2  # коэффициент лобового сопротивления
ro = 1.225  # плотность воздуха (кг/м^3)
S = 18.4  # площадь поперечного сечения (м^2)
g = 1.00034 * g  # ускорение свободного падения (м/с^2)
k = (M - m0) / (3 * 60 + 90)  # скорость изменения массы

def mass(t):
    return M - k * t

def du_dt(t, u):
    m_t = mass(t)
    return (
        -g
        - (Cf * (ro * u**2) * S) / (2 * m_t)
        + Ft / m_t
    )

time_span = (0, 45)
time_eval = np.linspace(time_span[0], time_span[1], 500)

# Начальные условия
u0 = 0  # начальная скорость

# Решение задачи
solution = solve_ivp(du_dt, time_span, [u0], t_eval=time_eval, method="RK45")

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(solution.t, solution.y[0], label="Скорость", color="blue")
plt.title("График скорости от времени")
plt.xlabel("Время (с)")
plt.ylabel("Скорость (м/с)")
plt.grid()
plt.legend()
plt.show()
