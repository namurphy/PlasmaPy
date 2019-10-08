from abc import ABC, abstractmethod

__all__ = ["AbstractParticle"]


class AbstractParticle(ABC):

    @abstractmethod
    @property
    def mass(self):
        raise NotImplemented
