from pyscreeze import Point, Box
from shapes.square import Square

class SoftwareBase:
    """Base class for each drawing application. Create new class for each application"""
    def __init__(self) -> None:
        self.software_name = None
        self.scr_directories = {}

    def start_new_drawing(self, width: int, height: int):
        raise NotImplemented
    
    def get_drawing_boundaries(self) -> Box:
        raise NotImplemented
    
    def draw_square_square_tool(self, square: Square):
        raise NotImplemented
    
    def draw_square_freehand(self, square: Square):
        raise NotImplemented
    
    def draw_line_freehand(self, start: Point, end: Point):
        raise NotImplemented
    
    def draw_continues_lines(self, start: Point, points: list[Point]):
        raise NotImplemented
    
    def draw_continues_lines_freehand(self, points: list[Point]):
        raise NotImplemented
    
    def close_application(self, save: bool = False):
        raise NotImplemented
    
    #
    #   DRAWING MODES
    #
    def set_brush_draw_mode_freehand(self):
        raise NotImplemented

    def set_brush_draw_mode_rectangle(self):
        raise NotImplemented
    
    #
    #   BRUSH
    #
    def get_brush_size(self) -> int:
        raise NotImplemented

    def brush_size_increase(self):
        raise NotImplemented
    
    def brush_size_decrease(self):
        raise NotImplemented
