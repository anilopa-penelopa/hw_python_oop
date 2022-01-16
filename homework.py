from dataclasses import dataclass
from typing import Dict, List, Union, Type


def format_for_template(template_string: str,
                        parameters: Dict[str, float]) -> str:
    return (template_string.format(**parameters))


@dataclass(init=True)
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        parameters: Dict[str, str] = {
            'training_type': self.training_type,
            'duration': format(self.duration, '.3f'),
            'distance': format(self.distance, '.3f'),
            'speed': format(self.speed, '.3f'),
            'calories': format(self.calories, '.3f')
        }
        template_string = (
            'Тип тренировки: {training_type}; '
            'Длительность: {duration} ч.; '
            'Дистанция: {distance} км; '
            'Ср. скорость: {speed} км/ч; '
            'Потрачено ккал: {calories}.'
        )
        return format_for_template(template_string, parameters)


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MINUTES_PER_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = self.__class__.__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(training_type=training_type, duration=duration,
                           distance=distance, speed=speed, calories=calories)


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_RUN_1: float = 18
    COEFF_CALORIE_RUN_2: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий на тренеровке "Бег"."""
        duration_minutes = self.duration * self.MINUTES_PER_HOUR
        calories: float = ((self.COEFF_CALORIE_RUN_1 * self.get_mean_speed()
                            - self.COEFF_CALORIE_RUN_2)
                           * self.weight / self.M_IN_KM
                           * duration_minutes
                           )
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_WALK_1: float = 0.035
    COEFF_CALORIE_WALK_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий на тренеровке "Ходьба"."""
        duration_minutes = self.duration * self.MINUTES_PER_HOUR
        calories = ((self.COEFF_CALORIE_WALK_1 * self.weight
                     + (self.get_mean_speed() ** 2 // self.height)
                     * self.COEFF_CALORIE_WALK_2 * self.weight)
                    * duration_minutes)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFF_CALORIE_SWIM_1: float = 1.1
    COEFF_CALORIE_SWIM_2: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в тренировке "Плавание"."""
        distance_meters = self.length_pool * self.count_pool
        distance_km = distance_meters / self.M_IN_KM
        mean_speed = distance_km / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий на тренеровке "Плавание"."""
        calories = ((self.get_mean_speed() + self.COEFF_CALORIE_SWIM_1)
                    * self.COEFF_CALORIE_SWIM_2 * self.weight)
        return calories


def read_package(workout_type: str, data: List[float]) -> Training:
    """Чтение данных, полученных с датчиков."""
    dict_trainings: Dict[str,  Type[Union[Swimming, Running, SportsWalking]]] = \
        {'SWM': Swimming,
         'RUN': Running,
         'WLK': SportsWalking}
    training_name = dict_trainings[workout_type]
    return training_name(*data)


def main(training: Training) -> None:
    """Вывод сообщений после тренировки."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
