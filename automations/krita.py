import pyautogui as pya
from pyscreeze import ImageNotFoundException, Point

from automations.software_base import SoftwareBase
from shapes.square import Square
from shapes.common import Size

class Krita(SoftwareBase):
    # Freehand moves too fast with 0.1 duration with pyautogui.dragTo()
    freehand_draw_speed = 0.2
    def __init__(self, screenshots_directory: str) -> None:
        self.scr_directories = {
            "base": screenshots_directory,
            "new_document_window": f"{screenshots_directory}/new_document_window",
            "drawing_window": f"{screenshots_directory}/drawing_window",
            "shapes": f"{screenshots_directory}/shapes"
        }

        self.software_name = "Krita"
        self.brush_size = 40

    #
    #   BASICS
    #
    def start_new_drawing(self, size: Size):
        """
        Software needs to be already open and active. Does not check for it!
        Presses "ctrl + n" for new document window
        Checks if the currently selected format is A4 (300ppi) in landscape. If not, changes to it
            - Checks if heihg width is wanted
        Presses create button
        Waits for the new document to be created
        """
        scr_folder = self.scr_directories['new_document_window']

        pya.hotkey("ctrl", "n")
        try:
            pya.locateOnScreen(f"{scr_folder}/window_title.png", 5, confidence=0.8) # TODO - Cleanup - Nicer file path
        except:
            print(f"Did not find active new document window title")
            # TODO change back
            title_pos = pya.locateCenterOnScreen(f"{scr_folder}/window_title_unactive.png", minSearchTime=5, confidence=0.9)
            pya.click(title_pos)

        pya.hotkey("alt", "i")
        pya.write(str(size.width))
        pya.hotkey("alt", "h")
        pya.write(str(size.height))
        pya.hotkey("alt", "c")
        pya.locateOnScreen(f"{scr_folder}/document_empty_2k_landscape.png", 5, confidence=0.9)

    
    def get_drawing_boundaries(self):
        return pya.locateOnScreen(f"{self.scr_directories['base']}/empty_2k_paper.png", confidence=0.9)
    
    #
    #   DRAWING
    #
    def draw_square_rectangle_tool(self, square: Square):
        # TODO - Does not work as thought. If drawn with same parameters as freehand, the square is ~20pixels wider on the drawing
        self.set_brush_draw_mode_rectangle()
        pya.moveTo(square.top_left)
        pya.dragTo(square.bottom_right)
    
    def draw_square_freehand(self, square: Square):
        points = [square.top_left, square.top_right, square.bottom_right, square.bottom_left, square.top_left]
        self.draw_continues_lines_freehand(points)

    def draw_line_freehand(self, start: Point, end: Point):
        self.set_brush_draw_mode_freehand()
        pya.moveTo(start)
        pya.dragTo(end, duration = Krita.freehand_draw_speed, button='left')
    
    def draw_continues_lines_freehand(self, points: list[Point]):
        self.set_brush_draw_mode_freehand()
        pya.moveTo(points[0])
        for point in points[1:]:
            pya.dragTo(point, duration = Krita.freehand_draw_speed, button='left')
    
    def close_application(self, save: bool = False):
        pya.hotkey("ctrl", "q")
        if not save:
            pya.hotkey("alt", "n")
            return

    #
    #   DRAWING MODES
    #
    def set_brush_draw_mode_freehand(self):
        pya.press("b")

    def set_brush_draw_mode_rectangle(self):
        pya.hotkey("shift", "r")

    #
    #   BRUSH
    #
    def get_brush_size(self) -> int:
        # TODO - Add functionality to actually getting the brush size, now only returns the starting size
        # Brush size is needed for calculting the allowed drawing zone and the clearance for other drawings
        # so the drawn objects (squares) do not touch
        return self.brush_size
        
    def brush_size_increase(self):
        pya.press("]")
    
    def brush_size_decrease(self):
        pya.press["["]

