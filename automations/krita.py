import pyautogui as pya
from pyscreeze import ImageNotFoundException
from automations.software_base import SoftwareBase
from helpers.square import Square
from pyscreeze import Point

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

    def get_brush_size(self) -> int:
        # TODO - Add functionality to actually getting the brush size, now only returns the starting size
        # Beush size is needed for calculting the allowed drawing zone and the clearance for other drawings
        # so the drawn objects (squares) do not touch
        return self.brush_size


    def increase_brush_size(self):
        pya.press("]")
    
    def decrease_brush_size(self):
        pya.press["["]


    def start_new_drawing(self, width: int, height: int):
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
            title_pos = pya.locateCenterOnScreen(f"{scr_folder}/window_title_unactive.png", 5, confidence=0.9)
            pya.click(title_pos)

        pya.hotkey("alt", "i")
        pya.write(str(width))
        pya.hotkey("alt", "h")
        pya.write(str(height))
        pya.hotkey("alt", "c")
        pya.locateOnScreen(f"{scr_folder}/document_empty_2k_landscape.png", 5, confidence=0.9)

    
    def get_drawing_boundaries(self):
        return pya.locateOnScreen(f"{self.scr_directories['base']}/empty_2k_paper.png", confidence=0.9)
    
    def draw_square_square_tool(self, square: Square):
        # TODO - Does not work as thought. If drawn with same parameters as freehand, the square is ~20pixels wider on the drawing
        pya.moveTo(square.top_left)
        pya.hotkey("shift", "r")
        pya.dragTo(square.bottom_right)
    
    def draw_square_freehand(self, square: Square):
        pya.press("b")
        pya.moveTo(square.top_left)
        pya.dragTo(square.top_right, duration = Krita.freehand_draw_speed, button='left')
        pya.dragTo(square.bottom_right, duration = Krita.freehand_draw_speed, button='left')
        pya.dragTo(square.bottom_left, duration = Krita.freehand_draw_speed, button='left')
        pya.dragTo(square.top_left, duration = Krita.freehand_draw_speed, button='left')

    def count_base_image_squares(self, img_name: str) -> int:
        #try:
        squares = pya.locateAllOnScreen(f"{self.scr_directories['shapes']}/{img_name}", confidence=0.985)
        #except pya.ImageNotFoundException as IE: # TODO - Why not working? Does not catch? Not a fan of catching all Exceptions
        #    return 0
        #except ImageNotFoundException as IE:
        #    return 0
        
        counter = 0
        try:
            for square in squares:
                counter += 1
        except pya.ImageNotFoundException as IE: # TODO - Why not working? Does not catch? Not a fan of catching all Exceptions
            return 0
        except ImageNotFoundException as IE:
            return 0
        
        return counter
    
    def draw_line_freehand(self, start: Point, end: Point):
        pya.press("b")
        pya.moveTo(start)
        pya.dragTo(end, duration = Krita.freehand_draw_speed, button='left')
    
    def close_application(self, save: bool = False):
        pya.hotkey("ctrl", "q")
        if not save:
            pya.hotkey("alt", "n")
            return

