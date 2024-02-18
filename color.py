from enum import Enum


class Color(Enum):
    RED = [1, 0, 0]
    GREEN = [0, 1, 0]
    BLUE = [0, 0, 1]

    YELLOW = [1, 1, 0]
    CYAN = [0, 1, 1]
    MAGENTA = [1, 0, 1]

    BLACK = [0, 0, 0]
    WHITE = [1, 1, 1]
    GRAY = [0.5, 0.5, 0.5]

    PINK = [1, 0.7529411764705882, 0.796078431372549]
    PURPLE = [0.5019607843137255, 0, 0.5019607843137255]

    def rgb(self):
        return self.value
