import utime
from machine import Pin


echo = Pin(8, Pin.IN)
trigger = Pin(9, Pin.OUT)

motor1a = Pin(14, Pin.OUT)
motor1b = Pin(15, Pin.OUT)

motor2a = Pin(17, Pin.OUT)
motor2b = Pin(16, Pin.OUT)


def measure_distance():
    trigger.low()  # отключаем датчик расстояния
    utime.sleep_us(2)
    trigger.high()  # посылаем сигнал в пространство
    utime.sleep_us(5)
    trigger.low()  # прекращаем слать сигнал, ждем ответа
    signal_off = 0
    signal_on = 0
    while echo.value() == 0:
        signal_off = utime.ticks_us()
    while echo.value() == 1:
        signal_on = utime.ticks_us()
    time_passed = signal_on - signal_off
    distance_to_object = (time_passed * 0.0343) / 2
    print("Дистанция до объекта: ", distance_to_object, "см")
    return distance_to_object


def forward():
    motor1a.high()
    motor1b.low()
    motor2a.high()
    motor2b.low()


def backward():
    motor1a.low()
    motor1b.high()
    motor2a.low()
    motor2b.high()


def left():
    motor1a.high()
    motor1b.low()
    motor2a.low()
    motor2b.high()


def right():
    motor1a.low()
    motor1b.high()
    motor2a.high()
    motor2b.low()


def stop():
    # на все 4 боковых контактных зажима перестаем подавать ток
    motor1a.low()
    motor1b.low()
    motor2a.low()
    motor2b.low()


while True:
    stop()
    n_measures = 100
    distance = 0.0
    for i in range(n_measures):
        distance += measure_distance()
    distance /= n_measures
    if distance < 20:
        stop()
        backward()
        utime.sleep(1)
        continue
    if distance < 40:
        stop()
        right()
        utime.sleep(1)
        continue
    stop()
    forward()
    utime.sleep(1)
