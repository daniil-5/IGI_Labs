import math

from matplotlib import patches

from Task4.base import GeometricFigure
from Task4.color import FigureColor

class Triangle(GeometricFigure):
    def __init__(self, radius, color):
        self.name = "Triangle"
        self.radius = radius
        self.color_obj = FigureColor(color)

    @property
    def color(self):
        return self.color_obj.color

    def area(self):
        side = 2 * math.sqrt(3) * self.radius
        area = (math.sqrt(3) / 4) * side ** 2
        return area

    def description(self):
        return "Figure: {0}, Radius: {1:.2f}, Color: {2}, Area: {3:.2f}".format(
            self.get_name(), self.radius, self.color, self.area()
        )

    def draw(self, text):
        import matplotlib.pyplot as plt
        from matplotlib.patches import Polygon

        side = 2 * math.sqrt(3) * self.radius
        height = math.sqrt(3) / 2 * side

        # 3 Points of the triangle
        points = [
            (0, 0),
            (side, 0),
            (side / 2, height)
        ]

        triangle = Polygon(points, closed=True, edgecolor='black', facecolor=self.color)
        fig, ax = plt.subplots()
        ax.add_patch(triangle)
        ax.set_xlim(-1, side + 1)
        ax.set_ylim(-1, height + 1)
        ax.set_aspect('equal')

        circle = patches.Circle((side / 2, height / 3), self.radius, fill=False, linestyle='--', edgecolor='black', linewidth=1.5)
        ax.add_patch(circle)

        ax.set_title(text)
        plt.grid(True)
        plt.savefig("Task4/triangle_output.png")
        plt.show()
