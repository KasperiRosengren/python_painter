from collections import namedtuple
from pyscreeze import Point, Box

import random
from typing import Union, Optional

Size = namedtuple("Size", ["width", "height"])

def create_random_point_within_boundaries(
        boundaries: Box,
        modifier_top: int = 0,
        modifier_bottom: int = 0,
        modifier_left: int = 0,
        modifier_right: int = 0
        ) -> Point:
    """Creates a random point in the given boundaries square
    

    """
    x = random.randint(boundaries.left + modifier_left, boundaries.left + boundaries.width + modifier_right)
    y = random.randint(boundaries.top + modifier_top, boundaries.top + boundaries.height + modifier_bottom)
    return Point(x, y)