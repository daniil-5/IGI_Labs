from abc import ABC, abstractmethod

class GeometricFigure(ABC):
    name = "Abstract Figure"

    @abstractmethod
    def area(self):
        pass

    def get_name(self):
        return self.name
