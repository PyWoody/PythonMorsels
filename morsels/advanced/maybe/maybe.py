import random


class _Maybe:

    def __init__(self, truthiness=0.5):
        self._truthiness = float(truthiness)
        self.choices = iter(
            random.choices(
                [True, False],
                weights=[self.truthiness, 1.0 - self.truthiness],
                k=100
            )
        )

    @property
    def truthiness(self):
        return self._truthiness

    @truthiness.setter
    def truthiness(self, value):
        self._truthiness = float(value)
        self.choices = iter(
            random.choices(
                [True, False],
                weights=[self.truthiness, 1.0 - self.truthiness],
                k=100
            )
        )

    def __repr__(self):
        return str(next(self))

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return next(self.choices)
        except StopIteration:
            self.choices = iter(
                random.choices(
                    [True, False],
                    weights=[self.truthiness, 1.0 - self.truthiness],
                    k=100
                )
            )
            return next(self.choices)

    def __call__(self):
        return next(self)

    def __bool__(self):
        return next(self)

    def __eq__(self, other):
        return next(self) == bool(other) if other else False


Maybe = _Maybe()
