"""
This program implements a fitness tracker software module
that processes data for three types of training: running, walking and swimming.
"""

# Type is used to annotate the dictionary type
# in the read_package function

from typing import Type


class InfoMessage:
    """Training Information Message."""

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
        """Get training information."""

        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Basic training class."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
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
        """Get the distance in km."""

        action: int = self.action
        m_in_km: int = self.M_IN_KM
        len_step: float = self.LEN_STEP

        distance_km: float = action * len_step / m_in_km

        return distance_km

    def get_mean_speed(self) -> float:
        """Get the mean speed in km/h."""

        distance: float = self.get_distance()
        duration: float = self.duration

        mean_speed_kmh: float = distance / duration

        return mean_speed_kmh

    def get_spent_calories(self) -> float:
        """Get the number of calories consumed."""

        return 0.0

    def show_training_info(self) -> InfoMessage:
        """Get an informational message about the completed workout."""

        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Training: Running."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Get the number of calories consumed while running.."""

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
    """Training: sports walking."""

    WALK_COEFFICIENT_1: float = 0.035
    WALK_COEFFICIENT_2: float = 0.029
    KMH_in_MS: float = 0.278
    SM_in_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Get the number of calories consumed while walking."""

        weight: float = self.weight

        walk_coef_1: float = self.WALK_COEFFICIENT_1
        walk_coef_2: float = self.WALK_COEFFICIENT_2

        kmh_in_ms: float = self.KMH_in_MS
        mean_speed_kmh: float = self.get_mean_speed()
        mean_speed_ms: float = mean_speed_kmh * kmh_in_ms

        sm_in_m: int = self.SM_in_M
        height_s: float = self.height
        height_m: float = height_s / sm_in_m

        duration_h: float = self.duration
        h_in_min: int = self.HOUR_IN_MINUTES
        duration_m: float = duration_h * h_in_min
        return ((walk_coef_1 * weight + (mean_speed_ms ** 2
                 / height_m) * walk_coef_2 * weight) * duration_m)


class Swimming(Training):
    """Training: Swimming."""
    LEN_STEP: float = 1.38
    SWIM_COEFFICIENT_1: float = 1.1
    SWIM_COEFFICIENT_2: int = 2

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
        """Get the average speed while swimming in km/h."""

        length_pool: float = self.length_pool
        count_pool: float = self.count_pool
        m_in_km: int = self.M_IN_KM
        distance: float = length_pool * count_pool / m_in_km

        duration: float = self.duration

        mean_speed_kmh: float = distance / duration

        return mean_speed_kmh

    def get_spent_calories(self) -> float:
        """Get the number of calories consumed while swimming."""

        mean_speed: float = self.get_mean_speed()

        swim_coef_1: float = self.SWIM_COEFFICIENT_1
        swim_coef_2: int = self.SWIM_COEFFICIENT_2

        weigth: float = self.weight
        duration: float = self.duration

        calories: float = ((mean_speed + swim_coef_1)
                           * swim_coef_2 * weigth * duration)

        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Read data from sensors."""

    sport_types: dict[str, Type[Training]] = {'SWM': Swimming,
                                              'RUN': Running,
                                              'WLK': SportsWalking}

    return sport_types[workout_type](*data)


def main(training: Training) -> None:
    """Main function."""

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
