from abc import ABC, abstractmethod
from CSP.Variable import Variable


class Constraint(ABC):

    def __init__(self, variables: list[Variable]):
        self.variables = variables

    def is_satisfied(self) -> bool:
        return True
