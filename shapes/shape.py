from pyscreeze import Point

from typing import Union, Optional

from shapes.common import Size


class Shape:
    """Base class for all shapes"""
    def __init__(self) -> None:
        self.brush_size: int = None
        self.brush_width: int = None

    def set_size(self, size: Size):
        raise NotImplementedError

    def set_brush_size(self, new_brush_size: int, new_brush_width: int):
        raise NotImplementedError
    
    def get_points_for_continuous_drawing(self) -> list[Point]:
        raise NotImplementedError
    
    def get_right_edge(self) -> int:
        raise NotImplementedError

    def get_left_edge(self) -> int:
        raise NotImplementedError
    
    def get_top_edge(self) -> int:
        raise NotImplementedError
    
    def get_bottom_edge(self) -> int:
        raise NotImplementedError
    
    def is_colliding_with(self, square: "Shape") -> bool:
        raise NotImplementedError     

    def get_screenshot(self):
        raise NotImplementedError
