from typing import Union


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:

        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Получить информацию о тренировке."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}. ')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: int = 0.65
    HOUR_IN_MINUTES: int = 60

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
        action = self.action
        m_in_km: int = self.M_IN_KM
        len_step: float = self.LEN_STEP
        return (action * len_step / m_in_km)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в км/ч."""
        distance = self.get_distance()
        duration = self.duration
        return (distance / duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.duration,
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: int = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий во время бега."""
        calories_multiplier: int = self.CALORIES_MEAN_SPEED_MULTIPLIER
        calories_shift: float = self.CALORIES_MEAN_SPEED_SHIFT
        mean_speed: float = self.get_mean_speed()
        weight: float = self.weight
        m_in_km: int = self.M_IN_KM
        h_in_min: int = self.HOUR_IN_MINUTES
        duration: float = self.duration
        return ((calories_multiplier * mean_speed + calories_shift)
                * weight / m_in_km * duration * h_in_min)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WALK_COEFFICIENT_1: float = 0.035
    WALK_COEFFICIENT_2: float = 0.029
    KMH_in_MS: float = 3.6

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий во время ходьбы."""
        walk_coef_1: float = self.WALK_COEFFICIENT_1
        walk_coef_2: float = self.WALK_COEFFICIENT_2
        kmh_in_ms: float = self.KMH_in_MS
        weight: float = self.weight
        mean_speed_kmh: float = self.get_mean_speed()
        mean_speed_ms: float = mean_speed_kmh / kmh_in_ms
        height: float = self.height
        duration: float = self.duration
        h_in_min = self.HOUR_IN_MINUTES
        return ((walk_coef_1 * weight + (mean_speed_ms ** 2 / height)
                 * walk_coef_2 * weight) * duration * h_in_min)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SWIM_COEFFICIENT_1: float = 1.1
    SWIM_COEFFICIENT_2: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость во время плавания."""
        length_pool: float = self.length_pool
        count_pool: float = self.count_pool
        m_in_km: int = self.M_IN_KM
        duration: float = self.duration
        return (length_pool * count_pool / m_in_km / duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий во время плавания."""
        mean_speed: float = self.get_mean_speed()
        swim_coef_1: float = self.SWIM_COEFFICIENT_1
        swim_coef_2: int = self.SWIM_COEFFICIENT_2
        weigth: float = self.weight
        duration: float = self.duration
        return ((mean_speed + swim_coef_1) * swim_coef_2 * weigth * duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    sport_types: dict[str, Union[Swimming,
                                 Running,
                                 SportsWalking]] = {'SWM': Swimming,
                                                    'RUN': Running,
                                                    'WLK': SportsWalking}
    if workout_type in sport_types:
        return sport_types[workout_type](*data)
    return None


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    message: str = info.get_message()
    print(message)


if __name__ == '__main__':
    packages: list[tuple[str, list[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
