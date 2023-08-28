"""
This program implements a fitness tracker software module
that processes data for three types of training: running, walking and swimming.
"""

from dataclasses import asdict, dataclass
from typing import ClassVar, TypeVar


@dataclass
class InfoMessage:
    """Training Information Message."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE_TEMPLATE: ClassVar[str] = ('Тип тренировки: {training_type}; '
                                       'Длительность: {duration:.3f} ч.; '
                                       'Дистанция: {distance:.3f} км; '
                                       'Ср. скорость: {speed:.3f} км/ч; '
                                       'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Get training information."""

        return self.MESSAGE_TEMPLATE.format(**asdict(self))


class Training:
    """Basic training class."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    HOUR_IN_MINUTES: int = 60

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Get the distance in km."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Get the mean speed in km/h."""

        distance: float = self.get_distance()

        return distance / self.duration

    def get_spent_calories(self) -> float:
        """Get the number of calories consumed."""

        raise NotImplementedError()

    def show_training_info(self) -> InfoMessage:
        """Get an informational message about the completed workout."""

        return InfoMessage(
            type(self).__name__,
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

        mean_speed: float = self.get_mean_speed()

        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * mean_speed
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * self.duration
                * self.HOUR_IN_MINUTES)


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

        mean_speed_kmh: float = self.get_mean_speed()
        mean_speed_ms: float = mean_speed_kmh * self.KMH_in_MS

        height_m: float = self.height / self.SM_in_M

        duration_m: float = self.duration * self.HOUR_IN_MINUTES

        return ((self.WALK_COEFFICIENT_1 * self.weight + (mean_speed_ms ** 2
                / height_m) * self.WALK_COEFFICIENT_2 * self.weight)
                * duration_m)


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

        distance: float = (self.length_pool * self.count_pool) / self.M_IN_KM

        return distance / self.duration

    def get_spent_calories(self) -> float:
        """Get the number of calories consumed while swimming."""

        mean_speed: float = self.get_mean_speed()

        return ((mean_speed + self.SWIM_COEFFICIENT_1)
                * self.SWIM_COEFFICIENT_2 * self.weight * self.duration)


T = TypeVar('T', int, float)


def read_package(workout_type: str, data: list[T]) -> Training:
    """ Read data from sensors."""

    sport_types: dict[str, type[Training]] = {'SWM': Swimming,
                                              'RUN': Running,
                                              'WLK': SportsWalking}

    try:
        return sport_types[workout_type](*data)

    except ValueError:
        raise ValueError('А здесь понятный текст, что пошло нет так') from None


def main(training: Training) -> None:
    """Main function."""

    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages: list[tuple[str, list[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
