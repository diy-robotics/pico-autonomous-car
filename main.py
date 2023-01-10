import utime
from machine import Pin


echo = Pin(8, Pin.IN)
trigger = Pin(9, Pin.OUT)

motor1a = Pin(14, Pin.OUT)
motor1b = Pin(15, Pin.OUT)

motor2a = Pin(17, Pin.OUT)
motor2b = Pin(16, Pin.OUT)


def measure_distance():
    """Функция измерения дистанции"""

    # отключаем датчик расстояния
    trigger.low()

    # делаем паузу на 2 микросекунды
    utime.sleep_us(2)

    # посылаем сигнал в пространство
    trigger.high()

    # делаем паузу на 5 микросекунд
    utime.sleep_us(5)

    # прекращаем слать сигнал, ждем ответа
    trigger.low()

    # задаем стартовое время отправления сигнала датчика - 0
    signal_off = 0
    # задаем время время получения ответа датчика - 0
    signal_on = 0

    # обновляем время отправки сигнала ультразвукового датчика
    # и время его ответа
    while echo.value() == 0:
        signal_off = utime.ticks_us()
    while echo.value() == 1:
        signal_on = utime.ticks_us()

    # считаем время между отправкой сигнала и получением ответа
    time_passed = signal_on - signal_off

    # высчитываем дистанцию до объекта,
    # зная что скорость звука - 343 м/секунду или 0.0343 см/микросекунду.
    # формула расчета: (время путешествия сигнала * скорость звука) / 2.
    distance_to_object = (time_passed * 0.0343) / 2
    print("Дистанция до объекта: ", distance_to_object, "см")
    return distance_to_object


def forward():
    """
    Функция движения вперед

    Моторы 1 и 2 запускаем вперед
    """
    motor1a.high()
    motor1b.low()
    motor2a.high()
    motor2b.low()


def backward():
    """
    Функция движения назад

    Моторы 1 и 2 запускаем назад
    """
    motor1a.low()
    motor1b.high()
    motor2a.low()
    motor2b.high()


def left():
    """
    Функция движения налево

    Мотор 1 (левый) запускаем вперед, мотор 2 (правый) - назад.
    """
    motor1a.high()
    motor1b.low()
    motor2a.low()
    motor2b.high()


def right():
    """
    Функция движения направо

    Мотор 1 запускаем назад, мотор 2 - вперед.
    """
    motor1a.low()
    motor1b.high()
    motor2a.high()
    motor2b.low()


def stop():
    """
    Функция остановки

    Прекращаем подавать ток на все контакты, связанные с моторами.
    """
    motor1a.low()
    motor1b.low()
    motor2a.low()
    motor2b.low()


def test():
    """Функция для тестирования сборки"""
    stop()
    forward()
    utime.sleep(5)
    backward()
    utime.sleep(5)
    stop()


test()  # запуск функции "тест"

# основный цикл работы робота
while True:
    # сначала останавливаем подачу тока на все моторы
    stop()

    # указываем, сколько измерений нужно,
    # чтобы посчитать расстояние до объекта впереди
    n_measures = 100

    # задаем первоначальную дистанцию - 0
    distance = 0.0

    # запускаем измерение дистанции "n_measures" раз, складываем все измерения
    for i in range(n_measures):
        distance += measure_distance()
    # делим дистанцию, собранную за "n_measures" запусков, на количество запусков
    distance /= n_measures

    # создаем условие: если дистанция меньше 20 см до предмета впереди,
    # то останавливаем робота, двигаемся назад, запускаем весь цикл заново
    if distance < 20:
        stop()
        backward()
        utime.sleep(1)
        continue
    # создаем условие: если дистанция меньше 40 см до предмета впереди,
    # то останавливаемся, поворачиваем направо, запускаем весь цикл заново
    if distance < 40:
        stop()
        right()
        utime.sleep(1)
        continue
    # если дистанции впереди достаточно,
    # то двигаемся вперед на протяжении 1 секунды
    forward()
    utime.sleep(1)
