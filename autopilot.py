import krpc
import time
import math

conn = krpc.connect(name='Восток-1')
vessel = conn.space_center.active_vessel

mass = vessel.mass
print(f"Масса ракеты: {mass:.2f} кг")

bounding_box = vessel.bounding_box(vessel.reference_frame)
width = bounding_box[1][0] - bounding_box[0][0]
radius = width / 2
area = math.pi * radius**2

print(f"Ширина ракеты: {width:.2f} м")
print(f"Площадь основания: {area:.2f} м²")

vessel.auto_pilot.engage()
vessel.auto_pilot.target_pitch_and_heading(90, 90)

vessel.control.activate_next_stage()
print("Старт!")

while vessel.resources.amount('SolidFuel') > 0.1:
    time.sleep(0.1)

print("Твердое топливо израсходовано. Следующая ступень...")
vessel.control.activate_next_stage()  # Нажатие пробела для отделения ТТ

# Поворот на 45 градусов на восток
print("Поворот на 45 градусов на восток.")
vessel.auto_pilot.target_pitch_and_heading(45, 90)

vessel.control.throttle = 1.0  # Продолжаем работу двигателя

print("Подъем до апоапсиса на 94 км.")
orbit = vessel.orbit
while orbit.apoapsis_altitude < 94000:
    time.sleep(0.1)

print("Апоапсис достигнут. Отключение двигателя.")
vessel.control.throttle = 0

print("Планирование маневра для круговой орбиты.")
mu = vessel.orbit.body.gravitational_parameter
r_target = vessel.orbit.body.equatorial_radius
v_circular = (mu / r_target) ** 0.5
current_speed = vessel.flight(vessel.orbital_reference_frame).speed

delta_v = v_circular - current_speed
apoapsis_time = conn.space_center.ut + vessel.orbit.time_to_apoapsis

node = vessel.control.add_node(apoapsis_time, prograde=delta_v)
print(f"Маневр создан с Δv = {delta_v:.2f} м/с.")

available_thrust = vessel.available_thrust
isp = vessel.specific_impulse * 9.82  # Ускорение тяги
fuel_flow = available_thrust / isp
burn_time = vessel.mass * delta_v / available_thrust

print(f"Расчетное время сжигания: {burn_time:.2f} секунд")

time.sleep(22)

print("Наведение на узел маневра.")
vessel.auto_pilot.engage()
vessel.auto_pilot.reference_frame = node.reference_frame
vessel.auto_pilot.target_direction = (0, 1, 0)
time.sleep(2)

vessel.control.throttle = 1.0

time.sleep(20)

vessel.control.throttle = 0.0

time.sleep(10)

print("Отделение ступени и завершение орбитальной фазы.")
vessel.control.activate_next_stage()
vessel.control.activate_next_stage()

node.remove()
