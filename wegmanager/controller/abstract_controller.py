# pylint: disable=missing-module-docstring
from abc import ABC, abstractmethod
from wegmanager.view.AbstractTab import AbstractTab


class AbstractController(ABC):
    @abstractmethod
    def bind(self, view: AbstractTab):
        raise NotImplementedError
