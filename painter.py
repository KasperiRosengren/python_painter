import pyautogui as pya
from pyscreeze import Box, Point

import argparse
import random

from automations.krita import Krita
from automations.machine import Machine
from helpers.square import Square
from helpers.datatypes import Size

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
        '--min_squares', 
        type=int, 
        default=2, 
        help='Minimum number of squares (default: 2)'
    )
    
    parser.add_argument(
        '--max_squares', 
        type=int, 
        default=5, 
        help='Maximum number of squares (default: 5)'
    )
    
    parser.add_argument(
        '--square_width', 
        type=int, 
        default=100, 
        help='Width of each square (default: 100)'
    )
    
    parser.add_argument(
        '--square_height', 
        type=int, 
        default=100, 
        help='Height of each square (default: 100)'
    )

    return parser.parse_args()

        
def create_random_point_within_boundaries(boundaries: Square) -> Point:
    return Point(
        random.randint(boundaries.get_left_edge(), boundaries.get_right_edge()),
        random.randint(boundaries.get_top_edge(), boundaries.get_bottom_edge())
    )

def create_random_square_within_boundaries(boundaries: Square, size: Size, brush_size: int) -> Square:
    top_left = Point(
        random.randint(boundaries.get_left_edge(), boundaries.get_right_edge() - size.width),
        random.randint(boundaries.get_top_edge(), boundaries.get_bottom_edge() - size.height)
    )
    return Square(top_left, size, brush_size)

def draw_random_lines_untill_no_square_found(krita: Krita, boundaries: Square):
    img = "square_freehand_40_100_100_black_on_white.png"
    counter = 0
    while krita.count_base_image_squares(img) > 0 or counter > 1_000:
        start_point = create_random_point_within_boundaries(boundaries)
        end_point = create_random_point_within_boundaries(boundaries)
        krita.draw_line_freehand(start_point, end_point)
        counter += 1
    
    print(f"{krita.count_base_image_squares(img)} squares found, {counter} lines drawn")

def create_squares(square_count: int, boundaries: Square, brush_size: int, max_retries: int = 100) -> list[Square]:
    def is_new_square_overlapping_with_others(square: Square, squares: list[Square]) -> bool:
        for test_square in squares:
            if square.is_colliding_with(test_square):
                return True
        return False

    squares = []
    retries = 0
    for _ in range(square_count):
        this_square = create_random_square_within_boundaries(boundaries, square_size, brush_size)
        print(this_square)

        if len(squares) == 0:
            # First square created, no need to check for overlap
            squares.append(this_square)
            continue

        while is_new_square_overlapping_with_others(this_square, squares):
            print("Illegal position")
            this_square = create_random_square_within_boundaries(boundaries, square_size, brush_size)
            print(this_square)
            retries += 1
        
            if retries > max_retries:
                raise RuntimeError("Unable to create legal square in 100 tries")
        retries = 0
        squares.append(this_square)

    return squares

def main(screenshots: str, squrare_min_max: tuple[int], square_size: Size):
    krita = Krita(f"{screenshots}/krita")
    machine = Machine(screenshots)

    machine.open_software(krita)
    krita.start_new_drawing(2560, 1440)

    square_count = random.randint(*squrare_min_max)
    squares = []
    
    drawing_boundaries = krita.get_drawing_boundaries()
    
    brush_size = krita.get_brush_size()
    brush_width = brush_size // 2 # Not the most accurate way of doing thing, but works for now

    if square_size.width < brush_size or square_size.height < brush_size:
        raise RuntimeError(f"Trying to use too small square size for the current brush {brush_size=} {square_size=}")


    boundary_top_left = Point(drawing_boundaries.left + brush_width, drawing_boundaries.top + brush_width)
    boundary_size = Size(drawing_boundaries.width - brush_width, drawing_boundaries.height - brush_width)
    square_boundaries = Square(boundary_top_left, boundary_size, 0)

    squares = create_squares(square_count, square_boundaries, brush_size)

    print(f"{square_count=}")
    print(f"{drawing_boundaries=}")
    print(f"{square_boundaries=}")

    
    
    print("Squares created successfully!".center(70, "-"))
    for square in squares:
        print(square)
        krita.draw_square_freehand(square)
    print("Squares drawn!".center(70, "-"))
    
    found_squares = krita.count_base_image_squares("square_freehand_40_100_100_black_on_white.png")
    print(f"Found: {found_squares}, Drawed: {square_count}")

    draw_random_lines_untill_no_square_found(krita, square_boundaries)
    machine.close_software(krita)

                


if __name__=="__main__":
    args = parse_args()
    screenshots = args.screenshots_dir
    squrare_min_max = (args.min_squares, args.max_squares)
    square_size = Size(args.square_width, args.square_height)
    main(screenshots, squrare_min_max, square_size)
