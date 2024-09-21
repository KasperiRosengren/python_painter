from .datatypes import Size
from pyscreeze import Point

class Square:
    def __init__(self, top_left: Point, size: Size, brush_size: int):
        self.size: Size = size
        self.calculate_corners(top_left)
        self.set_brush_size(brush_size)

    def set_brush_size(self, new_brush_size: int):
        self.brush_size = new_brush_size
        self.brush_width = new_brush_size // 2

    def calculate_corners(self, top_left: Point):
        self.top_left = top_left
        self.top_right = Point(top_left.x + self.size.width, top_left.y)
        self.bottom_left = Point(top_left.x, top_left.y + self.size.height)
        self.bottom_right = Point(top_left.x + self.size.width, top_left.y + self.size.height)

    def get_right_edge(self) -> int:
        return self.top_right.x

    def get_left_edge(self) -> int:
        return self.top_left.x
    
    def get_top_edge(self) -> int:
        return self.top_left.y
    
    def get_bottom_edge(self) -> int:
        return self.bottom_left.y
    
    def is_colliding_with(self, square: "Square") -> bool:
        """Checks that given square does not collide with self
        
        Check if self bottom is higher than other top, or other way around
        Check if self left is further to the right than other right, or other way around
        Takes into account the brush size included with each square
        """
        # self left side is more to the right than other squares right side
        if self.get_left_edge() - self.brush_width > square.get_right_edge() + square.brush_width:
            return False
        # other squares left side is more to the right than self right side
        if square.get_left_edge() - square.brush_width > self.get_right_edge() + self.brush_width:
            return False
        
        # self bottom is higher than the other squares top
        if self.get_bottom_edge() + self.brush_width < square.get_top_edge() - square.brush_width:
            return False
        # other squares bottom is higher than self top
        if square.get_bottom_edge() - square.brush_width < self.get_top_edge() - self.brush_width:
            return False
        
        return True
    
    def __str__(self) -> str:
        return f"Square:\n\t{self.size=}\n\t{self.brush_size=}, {self.brush_width=}\n\tCorners:\n\t\t{self.top_left}\t{self.top_right}\n\t\t{self.bottom_left}\t{self.bottom_right}"
 