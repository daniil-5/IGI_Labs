class FigureColor:
    def __init__(self, color: str):
        self._color = color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if not isinstance(value, str):
            raise ValueError("Color must be a string")
        self._color = value
