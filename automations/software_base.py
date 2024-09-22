from pyscreeze import Point, Box
from shapes.square import Square

class SoftwareBase:
    """Base class for each drawing application. Create new class for each application"""
    def __init__(self) -> None:
        self.software_name = None
        self.scr_directories = {}

    def start_new_drawing(self, width: int, height: int):
        raise NotImplementedError
    
    def get_drawing_boundaries(self) -> Box:
        raise NotImplementedError
    
    def draw_square_square_tool(self, square: Square):
        raise NotImplementedError
    
    def draw_square_freehand(self, square: Square):
        raise NotImplementedError
    
    def draw_line_freehand(self, start: Point, end: Point):
        raise NotImplementedError
    
    def draw_continues_lines(self, start: Point, points: list[Point]):
        raise NotImplementedError
    
    def draw_continues_lines_freehand(self, points: list[Point]):
        raise NotImplementedError
    
    def close_application(self, save: bool = False):
        raise NotImplementedError
    
    #
    #   DRAWING MODES
    #
    def set_brush_draw_mode_freehand(self):
        raise NotImplementedError

    def set_brush_draw_mode_rectangle(self):
        raise NotImplementedError
    
    #
    #   BRUSH
    #
    def get_brush_size(self) -> int:
        raise NotImplementedError

    def brush_size_increase(self):
        raise NotImplementedError
    
    def brush_size_decrease(self):
        raise NotImplementedError
