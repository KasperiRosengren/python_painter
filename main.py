import pyautogui as pya
from pyscreeze import Box, Point

import argparse
import random

from automations.painter import Painter
from automations.krita import Krita
from automations.machine import Machine
from automations.software_base import SoftwareBase
from shapes.square import Square, create_squares
from shapes.common import Size

def parse_args():
    desciption = """
        This script automates the process of drawing squares in a drawing application (Krita) using PyAutoGUI.
        The script performs the following steps:
        
        1. **Open Drawing Application**: It launches a drawing application (Krita) and waits for the application to load.
          
        2. **Draw Squares**: The program will randomly select a number of squares (between 2 and 5, inclusive) to draw on the canvas.
           Each square will have the same specified width and height. The position of each square is chosen randomly, ensuring that
           no squares overlap.
        
        3. **Count Squares**: After drawing the squares, the script uses image recognition to count the number of squares on the canvas.
           The counting is based on the known appearance and size of the squares. The program verifies that the number of squares on
           the canvas matches the number originally selected to draw.
        
        4. **Modify the Canvas**: The script randomly "messes up" the canvas by drawing over the squares so that they can no longer be recognized.
           This step ensures that the image recognition can no longer identify any squares on the canvas.
        
        5. **Close the Application**: Finally, the script closes the drawing application.
        """
    parser = argparse.ArgumentParser(description=desciption, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        '-d', '--screenshots-dir', 
        type=str,
        default="./screenshots",
        help='Directory where screenshots are stored. Default is ./screenshots'
    )
    
    parser.add_argument(
        '--min-squares', 
        type=int,
        default=2,
        help='Minimum number of squares (default: 2)'
    )
    
    parser.add_argument(
        '--max-squares', 
        type=int,
        default=5,
        help='Maximum number of squares (default: 5)'
    )
    
    parser.add_argument(
        '--square-width', 
        type=int,
        default=100,
        help='Width of each square (default: 100)'
    )
    
    parser.add_argument(
        '--square-height', 
        type=int,
        default=100,
        help='Height of each square (default: 100)'
    )
    args = parser.parse_args()
    screenshots = args.screenshots_dir
    if args.max_squares < args.min_squares:
        print("Max squares can not be lower than min squares. Setting both to min squares")
        squrare_min_max = (args.min_squares, args.min_squares)
    else:
        squrare_min_max = (args.min_squares, args.max_squares)

    square_size = Size(args.square_width, args.square_height)

    return screenshots, squrare_min_max, square_size

def main(screenshots: str, squrare_min_max: tuple[int], square_size: Size):
    print("STARTING".center(70, "-"))
    machine = Machine(screenshots) # move to args -> windows11, debian12 and ubuntu21.04 do things differently
    software = Krita(f"{screenshots}/krita") # move to args -> krita, paint and gimp have completely different UI and hotkeys
    painter = Painter(machine, software)
    painter.open_used_software()
    painter.start_new_drawing(Size(2560, 1440)) # TODO - create a way for not hard coding this. Requires support for finding correct draw are

    draw_area = painter.get_painting_borders()

    square_count = random.randint(*squrare_min_max) # Randomise the square count for each run

    squares = create_squares(square_count, draw_area, square_size, painter.get_current_brush_size())
    print(f"{draw_area=}")
    print("Squares created")

    painter.draw_shapes_on_canvas(squares)
    print("Squares drawn")


    # Using the screenshot
    preset_img = f"{software.scr_directories['shapes']}/square_freehand_40_100_100_black_on_white.png"
    preset_found = machine.count_all_image_occurances(preset_img, confidence=0.98)
    print(f"Found {preset_found}/{square_count} squares drawn, with presaved screenshot")

    # Using one of the drawn shapes as benchmark, this time the first one drawn
    shape_scr = squares[0].get_screenshot()
    found_scr = machine.count_all_image_occurances(shape_scr, confidence=0.99)
    print(f"Found {found_scr}/{square_count} squares drawn, with new screenshot")

    painter.draw_random_lines_on_canvas_until_image_not_found(draw_area, preset_img, confidence = 0.98)


    painter.close_used_software()



    

if __name__=="__main__":
    args = parse_args()
    main(*args)
