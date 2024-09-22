import pyautogui as pya
from pyscreeze import Point, Box


from typing import Union, Optional

from shapes.common import Size, create_random_point_within_boundaries
from shapes.shape import Shape

#
#   CLASSES
#
class SquareSizeNotAllowed(Exception):
    pass

class Square(Shape):
    def __init__(self, top_left: Point, size: Size, brush_size: int):
        """
        
        Args:
            top_left (Point): test
            size (Size): test
            brush_size (int): test

        Examples:
            Create a square with top left at (0,0), size (100,100) and brush size of 40:
                >>> test_square = Square(Point(0,0), Size(100,100), 40)
                >>> print(f"{test_square.top_left}, {test_square.top_right}, {test_square.bottom_left}, {test_square.bottom_right}")
                Point(x=0, y=0), Point(x=100, y=0), Point(x=0, y=100), Point(x=100, y=100)
                >>> print(f"{test_square.size.width}, {test_square.size.height}")
                100, 100
                >>> print(f"{test_square.brush_size}, {test_square.brush_width}")
                40, 20

            Create a square with top left at (0,0), size (100,100) and brush size of 40:
                >>> test_square = Square(Point(0,0), Size(100,100), 40)
                >>> print(f"{test_square.top_left}, {test_square.top_right}, {test_square.bottom_left}, {test_square.bottom_right}")
                Point(x=0, y=0), Point(x=100, y=0), Point(x=0, y=100), Point(x=100, y=100)
                >>> print(f"{test_square.size.width}, {test_square.size.height}")
                100, 100
                >>> print(f"{test_square.brush_size}, {test_square.brush_width}")
                40, 20
        """
        self.set_size(size)
        self.calculate_corners(top_left)
        self.set_brush_size(brush_size, brush_size // 2)

    def __str__(self) -> str:
        return f"Square:\n\t{self.size=}\n\t{self.brush_size=}, {self.brush_width=}\n\tCorners:\n\t\t{self.top_left}\t{self.top_right}\n\t\t{self.bottom_left}\t{self.bottom_right}"

    
    def set_size(self, size: Size):
        """

        Args:
            size (Size): 
        
        raises:
            SquareSizeNotAllowed: When the square size is smaller than 1x1

        Examples:
            Set size to 100x100:
                >>> test_square = Square(Point(0,0), Size(250,250), 40)
                >>> test_square.set_size(Size(100,100))
                >>> print(f"{test_square.size}")
                Size(width=100, height=100)

            Set size to zero:
                >>> test_square = Square(Point(0,0), Size(250,250), 40)
                >>> test_square.set_size(Size(0,0))
                Traceback (most recent call last):
                    ...
                square.SquareSizeNotAllowed: Minimum square size is Size(1,1). Given Size(width=0, height=0)
                >>> print(f"{test_square.size}")
                Size(width=250, height=250)
            
            Set size to negative:
                >>> test_square = Square(Point(0,0), Size(250,250), 40)
                >>> test_square.set_size(Size(-100, -100))
                Traceback (most recent call last):
                    ...
                square.SquareSizeNotAllowed: Minimum square size is Size(1,1). Given Size(width=-100, height=-100)
                >>> print(f"{test_square.size}")
                Size(width=250, height=250)
            
            Set height to negative:
                >>> test_square = Square(Point(0,0), Size(250,250), 40)
                >>> test_square.set_size(Size(100,-100))
                Traceback (most recent call last):
                    ...
                square.SquareSizeNotAllowed: Minimum square size is Size(1,1). Given Size(width=100, height=-100)
                >>> print(f"{test_square.size}")
                Size(width=250, height=250)

            Set width to negative:
                >>> test_square = Square(Point(0,0), Size(250,250), 40)
                >>> test_square.set_size(Size(-100,100))
                Traceback (most recent call last):
                    ...
                square.SquareSizeNotAllowed: Minimum square size is Size(1,1). Given Size(width=-100, height=100)
                >>> print(f"{test_square.size}")
                Size(width=250, height=250)
        """
        if size.height <= 0 or size.width <= 0:
            raise SquareSizeNotAllowed(f"Minimum square size is Size(1,1). Given {size}")
        self.size = size

    def set_brush_size(self, new_brush_size: int, new_brush_width: int):
        """Sets the brush size for the object

        Args:
            new_brush_size (int):   The diameter of the brush
            new_brush_width (int):   The radius of the brush

        Examples:
            Set brush size to even number:
                >>> test_square = Square(Point(1000,1000), Size(100,100), 40)
                >>> test_square.set_brush_size(10, 5)
                >>> print(f"{test_square.brush_size}, {test_square.brush_width}")
                10, 5
        """

        self.brush_size = new_brush_size
        self.brush_width = new_brush_width
        


    def calculate_corners(self, top_left: Point) -> list[Point]:
        """ Generates the corners for the object from the given top left corner

        Does not care about drawing boundaries and will happily point outside of the screen if wanted.
        Requires the self.size parameter to be present and a type of Point

        Args:
            top_left (Point): Represents the squares top left corner
        
        Returns:
            list[Point]: The newly created corners [top left, top right, bottom right, bottom left]
        
        Examples:
            Calculate corners at origin for 100x100 square:
                >>> test_square = Square(Point(1000,1000), Size(100,100), 40)
                >>> print(test_square.calculate_corners(Point(0,0)))
                [Point(x=0, y=0), Point(x=100, y=0), Point(x=100, y=100), Point(x=0, y=100)]
            
            Calculate corners at negative position for 100x100 square:
                >>> test_square = Square(Point(1000,1000), Size(100,100), 40)
                >>> print(test_square.calculate_corners(Point(-1000,-1000)))
                [Point(x=-1000, y=-1000), Point(x=-900, y=-1000), Point(x=-900, y=-900), Point(x=-1000, y=-900)]
            
            Calculate corners at large positive position for 10000x10000 square:
                >>> test_square = Square(Point(1000,1000), Size(10000, 10000), 40)
                >>> print(test_square.calculate_corners(Point(100_000,100_000)))
                [Point(x=100000, y=100000), Point(x=110000, y=100000), Point(x=110000, y=110000), Point(x=100000, y=110000)]
            
            
        """
        self.top_left = top_left
        self.top_right = Point(top_left.x + self.size.width, top_left.y)
        self.bottom_left = Point(top_left.x, top_left.y + self.size.height)
        self.bottom_right = Point(top_left.x + self.size.width, top_left.y + self.size.height)

        return [self.top_left, self.top_right, self.bottom_right, self.bottom_left]
    
    def get_points_for_continuous_drawing(self) -> list[Point]:
        """Returns a list of all drawing points for continuos drawing
        
        Examples:
            Get all conmtinuous drawing points for square at top left with size of 100:
                >>> test_square = Square(Point(0,0), Size(100,100), 40)
                >>> test_square.get_points_for_continuous_drawing()
                [Point(x=0, y=0), Point(x=100, y=0), Point(x=100, y=100), Point(x=0, y=100), Point(x=0, y=0)]
        """
        # The list should start and end in the same spot
        return [self.top_left, self.top_right, self.bottom_right, self.bottom_left, self.top_left]

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

        Examples:
            Squares do not touch
            Squares are identical
            Squares one side of brushes overlap
            Squares one side overlap
            Squares share a corner
            Squares corner inside of each other
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
    
    
    def get_screenshot(self):
        shape_box = (self.get_left_edge(), self.get_top_edge(), self.size.width, self.size.height)
        return pya.screenshot(region=shape_box)
        

#
#   HELPER FUNCTIONS
#
def create_random_square_within_boundaries(boundaries: Box, size: Size, brush_size: int) -> Square:
    top_left = create_random_point_within_boundaries(boundaries, modifier_bottom=-size.height, modifier_right=-size.width)
    return Square(top_left, size, brush_size)


def create_squares(square_count: int, boundaries: Box, square_size: Size, brush_size: int, max_retries: int = 100) -> list[Square]:
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