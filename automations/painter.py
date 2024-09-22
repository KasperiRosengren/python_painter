from pyscreeze import Box, Point
from PIL.Image import Image

from typing import Optional, Union
from time import time

from automations.software_base import SoftwareBase
from automations.machine import Machine
from shapes.square import create_squares
from shapes.common import Size, create_random_point_within_boundaries
from shapes.shape import Shape

class Painter:
    def __init__(self, machine: Machine, software: SoftwareBase) -> None:
        self.machine = machine
        self.software = software
    
    def start_new_drawing(self, drawing_size: Size):
        self.software.start_new_drawing(drawing_size)
    
    def get_current_brush_size(self) -> int:
        return self.software.get_brush_size()

    def get_painting_borders(self) -> Box:
        drawing_boundaries = self.software.get_drawing_boundaries()
        brush_size = self.software.get_brush_size()
        draw_area = create_painting_border_for_brush(drawing_boundaries, brush_size)
        return draw_area

    def open_used_software(self):
        self.machine.open_software(self.software)
    
    def close_used_software(self):
        self.machine.close_software(self.software)
    
    def draw_shapes_on_canvas(self, shapes: list[Shape]):
        for shape in shapes:
            self.software.draw_continues_lines_freehand(shape.get_points_for_continuous_drawing())
    
    def draw_line_on_canvas(self, start_point: Point, end_point: Point):
        self.software.draw_line_freehand(start_point, end_point)

    def draw_random_lines_on_canvas_until_image_not_found(self, boundaries: Box, image: Union[str, Image], timeout: int = 240, **kwargs):
        if (images_found := self.machine.count_all_image_occurances(image, **kwargs)) <= 0:
            return
        
        start_time = time()
        end_time = start_time + timeout
        draw_counter = 0
        # Keeps looping untill no images are found, or the timer runs out
        while (img_found := self.machine.count_all_image_occurances(image, **kwargs)) > 0:
            if time() > end_time:
                raise RuntimeError("Images still found")
            if images_found != img_found:
                images_found = img_found
                print(f"One image skrippled over, {img_found} left")
            
            draw_counter += 1
            start_point = create_random_point_within_boundaries(boundaries)
            end_point = create_random_point_within_boundaries(boundaries)
            self.software.draw_line_freehand(start_point, end_point)
        
        finish_time = time()

        elapsed = finish_time - start_time
        
        print(f"No images found any more. Took {draw_counter} lines and {elapsed:.2f} seconds")
    
    def count_shapes_in_screen(self, shape: Shape):
        scr = shape.get_screenshot()
        return self.machine.count_all_image_occurances(scr, confidence = 0.99)


def create_painting_border_for_brush(draw_area: Box, brush_size: int) -> Box:
    brush_width = brush_size // 2 # Not the most accurate way of doing thing, but works for now
    # Drawing boundaries need to take in to account the brush width. Drawing outside of the paper is not wanted behaviour
    left = draw_area.left + brush_width
    top = draw_area.top + brush_width
    width = draw_area.width - brush_width
    height = draw_area.height - brush_width
    return Box(left, top, width, height)