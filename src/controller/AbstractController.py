from abc import ABC, abstractmethod
from view.AbstractTab import AbstractTab


class AbstractController(ABC):
    @abstractmethod
    def bind(self, view: AbstractTab):
        raise NotImplementedError
