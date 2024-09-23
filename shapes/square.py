import pyautogui as pya
from pyscreeze import Point, Box
from PIL.Image import Image

from typing import Union, Optional

from shapes.common import Size, create_random_point_within_boundaries
from shapes.shape import Shape

#
#   CLASSES
#
class SquareSizeNotAllowed(Exception):
    """Exception raised for invalid square sizes.

    This exception is raised when an attempt is made to set a square's size 
    that does not meet the required constraints, such as being too small.

    Args:
        message (str): A description of the size issue.
        size (Size): The size that caused the exception.
    
    Examples:
        Raise an exception for a square that is too small:
            >>> raise SquareSizeNotAllowed("Square is too small", Size(0,0))
            Traceback (most recent call last):
                ...
            square.SquareSizeNotAllowed: Square is too small: Size(width=0, height=0)
    
        Raise an exception for a square that is not wide enough:
            >>> raise SquareSizeNotAllowed("Square is not wide enough", Size(0,100))
            Traceback (most recent call last):
                ...
            square.SquareSizeNotAllowed: Square is not wide enough: Size(width=0, height=100)
        
        Raise an exception for a square that is not tall enough:
            >>> raise SquareSizeNotAllowed("Square is not tall enough", Size(100,0))
            Traceback (most recent call last):
                ...
            square.SquareSizeNotAllowed: Square is not tall enough: Size(width=100, height=0)
        
        
    """
    def __init__(self, message, size: Size):
        self.message = message
        self.size = size
        super().__init__(f"{message}: {size}")
    
    def __str__(self) -> str:
        return f"{self.message}: {self.size}"

class Square(Shape):
    """Represents a square shape in a 2D space.

    The Square class inherits from the Shape class and encapsulates properties and behaviors
    specific to a square. It includes information about the square's position, size, and 
    brush attributes, and provides methods to manipulate and interact with the square.

    Attributes:
        top_left (Point): The top-left corner of the square.
        top_right (Point): The top-right corner of the square, calculated from top_left and size.
        bottom_left (Point): The bottom-left corner of the square, calculated from top_left and size.
        bottom_right (Point): The bottom-right corner of the square, calculated from top_left and size.
        size (Size): The width and height of the square.
        brush_size (int): The width of the brush used to draw the square.
        brush_width (int): The effective width of the brush, typically half of the brush size.

    Methods:
        set_size(size: Size): Adjusts the size of the square, ensuring it meets size requirements.
        set_brush_size(new_brush_size: int, new_brush_width: int): Sets the brush size
        calculate_corners(top_left: Point) -> list[Point]: Generates the corners of the square based on the given top-left corner.
        get_right_edge() -> int: Returns the x-coordinate of the square's right edge.
        get_left_edge() -> int: Returns the x-coordinate of the square's left edge.
        get_top_edge() -> int: Returns the y-coordinate of the square's top edge.
        get_bottom_edge() -> int: Returns the y-coordinate of the square's bottom edge.
        is_colliding_with(square: Square) -> bool: Checks if this square overlaps with another square.
        get_screenshot() -> Image: Takes a screenshot of the square's area.
        __str__() -> str: Returns a string representation of the square.

    Examples:
        Create a square and display its properties:
            >>> test_square = Square(Point(0, 0), Size(100, 100), 10)
            >>> print(test_square.size)
            Size(width=100, height=100)
            >>> print(test_square)
            Square: self.size=Size(width=100, height=100), self.brush_size=10, self.brush_width=5, self.top_left=Point(x=0, y=0), self.top_right=Point(x=100, y=0), self.bottom_left=Point(x=0, y=100), self.bottom_right=Point(x=100, y=100)

        Adjust the size of the square:
            >>> test_square = Square(Point(0, 0), Size(100, 100), 10)
            >>> test_square.set_size(Size(150, 150))
            >>> print(test_square.size)
            Size(width=150, height=150)
    """
    def __init__(self, top_left: Point, size: Size, brush_size: int):
        """
        Initializes a Square object, which represents a square shape on the screen.

        Args:
            top_left (Point): The coordinates of the top-left corner of the square.
            size (Size): The dimensions of the square, defined by width and height.
            brush_size (int): The width of the brush used to draw the square.
                             This affects the total size of the square.

        Attributes:
            top_left (Point): The top-left corner of the square.
            top_right (Point): The top-right corner, calculated based on the size.
            bottom_left (Point): The bottom-left corner, calculated based on the size.
            bottom_right (Point): The bottom-right corner, calculated based on the size.
            size (Size): Stores the width and height of the square.
            brush_size (int): The thickness of the brush used for the square's outline.
            brush_width (int): Half the brush size, used for inner stroke calculations.

        Raises:
            SquareSizeNotAllowed: If the size is invalid (e.g., width or height <= 0).

        Examples:
            Create a square with a top-left corner at (0,0), size of (100,100), and a brush size of 40:
                >>> test_square = Square(Point(0,0), Size(100,100), 40)
                >>> print(f"{test_square.top_left}, {test_square.top_right}, {test_square.bottom_left}, {test_square.bottom_right}")
                Point(x=0, y=0), Point(x=100, y=0), Point(x=0, y=100), Point(x=100, y=100)
                >>> print(f"{test_square.size.width}, {test_square.size.height}")
                100, 100
                >>> print(f"{test_square.brush_size}, {test_square.brush_width}")
                40, 20

            Create a square with a larger brush size of 60:
                >>> test_square = Square(Point(0,0), Size(100,100), 60)
                >>> print(f"{test_square.top_left}, {test_square.top_right}, {test_square.bottom_left}, {test_square.bottom_right}")
                Point(x=0, y=0), Point(x=100, y=0), Point(x=0, y=100), Point(x=100, y=100)
                >>> print(f"{test_square.size.width}, {test_square.size.height}")
                100, 100
                >>> print(f"{test_square.brush_size}, {test_square.brush_width}")
                60, 30
        """
        self.set_size(size)
        self.calculate_corners(top_left)
        self.set_brush_size(brush_size, brush_size // 2)

    def __str__(self) -> str:
        """Return a concise string representation of the Square object.

        This method provides a formatted string that includes key properties of the 
        square, such as its size, brush size, brush width, and the coordinates of its 
        corners. It is useful for debugging and quickly inspecting the square's attributes.

        Returns:
            str: A formatted string representation of the Square object.

        Examples:
            Create a square and print its string representation:
                >>> square = Square(Point(0, 0), Size(100, 100), 10)
                >>> print(square)
                Square: self.size=Size(width=100, height=100), self.brush_size=10, self.brush_width=5, self.top_left=Point(x=0, y=0), self.top_right=Point(x=100, y=0), self.bottom_left=Point(x=0, y=100), self.bottom_right=Point(x=100, y=100)
        """
        return (f"Square: {self.size=}, {self.brush_size=}, "
                f"{self.brush_width=}, {self.top_left=}, "
                f"{self.top_right=}, {self.bottom_left=}, "
                f"{self.bottom_right=}")
    
    def set_size(self, size: Size):
        """Ensure the square size is large enough.

        Args:
            size (Size): The new size of the square.

        Raises:
            SquareSizeNotAllowed: If the size is smaller than 1x1 or has negative dimensions.

        Examples:
            Set size to 100x100:
                >>> test_square = Square(Point(0, 0), Size(250, 250), 40)
                >>> test_square.set_size(Size(100, 100))
                >>> print(f"{test_square.size}")
                Size(width=100, height=100)

            Set size to zero:
                >>> test_square = Square(Point(0, 0), Size(250, 250), 40)
                >>> test_square.set_size(Size(0, 0))
                Traceback (most recent call last):
                    ...
                square.SquareSizeNotAllowed: Square is too small: Size(width=0, height=0)
                >>> print(f"{test_square.size}")
                Size(width=250, height=250)
            
            Set size to negative:
                >>> test_square = Square(Point(0, 0), Size(250, 250), 40)
                >>> test_square.set_size(Size(-100, -100))
                Traceback (most recent call last):
                    ...
                square.SquareSizeNotAllowed: Square is too small: Size(width=-100, height=-100)
                >>> print(f"{test_square.size}")
                Size(width=250, height=250)
            
            Set height to negative:
                >>> test_square = Square(Point(0, 0), Size(250, 250), 40)
                >>> test_square.set_size(Size(100, -100))
                Traceback (most recent call last):
                    ...
                square.SquareSizeNotAllowed: Square is not tall enough: Size(width=100, height=-100)
                >>> print(f"{test_square.size}")
                Size(width=250, height=250)

            Set width to negative:
                >>> test_square = Square(Point(0, 0), Size(250, 250), 40)
                >>> test_square.set_size(Size(-100, 100))
                Traceback (most recent call last):
                    ...
                square.SquareSizeNotAllowed: Square is not wide enough: Size(width=-100, height=100)
                >>> print(f"{test_square.size}")
                Size(width=250, height=250)
        """
        if size.height <= 0 or size.width <= 0:
            if size.height <= 0 and size.width <= 0:
                raise SquareSizeNotAllowed("Square is too small", size)
            elif size.height <= 0:
                raise SquareSizeNotAllowed("Square is not tall enough", size)
            else:
                raise SquareSizeNotAllowed("Square is not wide enough", size)
        
        self.size = size

    def set_brush_size(self, new_brush_size: int, new_brush_width: int):
        """Set the brush size and width for the square.

        This method updates the brush size and width used for drawing the square. 
        The brush size is typically the diameter, while the brush width is the effective 
        radius. 

        Args:
            new_brush_size (int): The diameter of the brush. This value must be a positive integer.
            new_brush_width (int): The effective width of the brush. This value must be a positive integer.

        Examples:
            Set brush size and width to valid values:
                >>> test_square = Square(Point(1000, 1000), Size(100, 100), 40)
                >>> test_square.set_brush_size(10, 5)
                >>> print(f"{test_square.brush_size}, {test_square.brush_width}")
                10, 5

            Change brush size and width to new values:
                >>> test_square.set_brush_size(20, 10)
                >>> print(f"{test_square.brush_size}, {test_square.brush_width}")
                20, 10
        """

        self.brush_size = new_brush_size
        self.brush_width = new_brush_width
        
    def calculate_corners(self, top_left: Point) -> list[Point]:
        """Generate the corners of the square from the given top-left corner.

        This method calculates the positions of the square's corners based on the 
        provided top-left corner and the square's size. It does not consider drawing 
        boundaries and can produce corners outside the visible area if desired. 
        The `self.size` attribute must be set prior to calling this method.

        Args:
            top_left (Point): The top-left corner of the square.

        Returns:
            list[Point]: A list of Points representing the corners of the square in 
                        the order [top left, top right, bottom right, bottom left].

        Examples:
            Calculate corners at origin for a 100x100 square:
                >>> test_square = Square(Point(1000, 1000), Size(100, 100), 40)
                >>> print(test_square.calculate_corners(Point(0, 0)))
                [Point(x=0, y=0), Point(x=100, y=0), Point(x=100, y=100), Point(x=0, y=100)]

            Calculate corners at a negative position for a 100x100 square:
                >>> test_square = Square(Point(1000, 1000), Size(100, 100), 40)
                >>> print(test_square.calculate_corners(Point(-1000, -1000)))
                [Point(x=-1000, y=-1000), Point(x=-900, y=-1000), Point(x=-900, y=-900), Point(x=-1000, y=-900)]

            Calculate corners at a large positive position for a 10000x10000 square:
                >>> test_square = Square(Point(1000, 1000), Size(10000, 10000), 40)
                >>> print(test_square.calculate_corners(Point(100_000, 100_000)))
                [Point(x=100000, y=100000), Point(x=110000, y=100000), Point(x=110000, y=110000), Point(x=100000, y=110000)]
        """
        self.top_left = top_left
        self.top_right = Point(top_left.x + self.size.width, top_left.y)
        self.bottom_left = Point(top_left.x, top_left.y + self.size.height)
        self.bottom_right = Point(top_left.x + self.size.width, top_left.y + self.size.height)

        return [self.top_left, self.top_right, self.bottom_right, self.bottom_left]
    
    def get_points_for_continuous_drawing(self) -> list[Point]:
        """Return a list of all drawing points for continuous drawing.

        This method generates the sequence of points that outline the square, 
        allowing for continuous drawing. The list begins and ends at the same 
        point to create a closed shape.

        Returns:
            list[Point]: A list of Points representing the corners of the square 
                        in order, including the starting point at the end for 
                        continuous drawing.

        Examples:
            Get all continuous drawing points for a square at top left with size of 100:
                >>> test_square = Square(Point(0, 0), Size(100, 100), 40)
                >>> test_square.get_points_for_continuous_drawing()
                [Point(x=0, y=0), Point(x=100, y=0), Point(x=100, y=100), Point(x=0, y=100), Point(x=0, y=0)]
        """
        # The list should start and end in the same spot
        return [self.top_left, self.top_right, self.bottom_right, self.bottom_left, self.top_left]

    def get_right_edge(self) -> int:
        """Get the x coordinate of the square's rightmost edge.

        This method calculates the rightmost x coordinate of the square, taking into account
        the brush width used when drawing the square.

        Returns:
            int: The x-coordinate of the square's rightmost edge, including the brush width.

        Examples:
            Get the square's rightmost edge:
                >>> square = Square(Point(100, 100), Size(100, 100), 40)
                >>> print(square.get_right_edge())
                220
            
            Get the square's rightmost edge without brush:
                >>> square = Square(Point(100, 100), Size(100, 100), 0)
                >>> print(square.get_right_edge())
                200
        """
        return self.top_right.x + self.brush_width

    def get_left_edge(self) -> int:
        """Get the x-coordinate of the square's leftmost edge.

        This method calculates the leftmost x-coordinate of the square, taking into account
        the brush width used when drawing the square.

        Returns:
            int: The x-coordinate of the square's leftmost edge, adjusted for the brush width.

        Examples:
            Get the square's leftmost edge:
                >>> square = Square(Point(100, 100), Size(100, 100), 40)
                >>> print(square.get_left_edge())
                80
            
            Get the square's leftmost edge without brush:
                >>> square = Square(Point(100, 100), Size(100, 100), 0)
                >>> print(square.get_left_edge())
                100
        """
        return self.top_left.x - self.brush_width
    
    def get_top_edge(self) -> int:
        """Get the y-coordinate of the square's topmost edge.

        This method calculates the topmost y-coordinate of the square, taking into account
        the brush width used when drawing the square.

        Returns:
            int: The y-coordinate of the square's topmost edge, adjusted for the brush width.

        Examples:
            Get the square's topmost edge:
                >>> square = Square(Point(100, 100), Size(100, 100), 40)
                >>> print(square.get_top_edge())
                80
            
            Get the square's topmost edge without brush:
                >>> square = Square(Point(100, 100), Size(100, 100), 0)
                >>> print(square.get_top_edge())
                100
        """
        return self.top_left.y - self.brush_width
    
    def get_bottom_edge(self) -> int:
        """Get the y-coordinate of the square's bottommost edge.

        This method calculates the bottommost y-coordinate of the square, taking into account
        the brush width used when drawing the square.

        Returns:
            int: The y-coordinate of the square's bottommost edge, adjusted for the brush width.

        Examples:
            Get the square's bottommost edge:
                >>> square = Square(Point(100, 100), Size(100, 100), 40)
                >>> print(square.get_bottom_edge())
                220
            
            Get the square's bottommost edge without brush:
                >>> square = Square(Point(100, 100), Size(100, 100), 0)
                >>> print(square.get_bottom_edge())
                200
        """
        return self.bottom_left.y + self.brush_width
    
    def is_colliding_with(self, square: "Square") -> bool:
        """Checks whether this square overlaps (collides) with another square.

        This method determines if two squares are colliding by comparing their edges.
        It checks whether any of the following conditions hold:
        - The left side of this square is further to the right than the other square's right side.
        - The right side of this square is further to the left than the other square's left side.
        - The bottom of this square is higher than the other square's top.
        - The top of this square is lower than the other square's bottom.

        The brush size of each square is taken into account when calculating the edges.

        Args:
            square (Square): The other square to check collision with.

        Returns:
            bool: `True` if the squares overlap, `False` otherwise.

        Examples:
            Squares do not touch:
                >>> square1 = Square(Point(0, 0), Size(100, 100), 40)
                >>> square2 = Square(Point(200, 200), Size(100, 100), 40)
                >>> print(square1.is_colliding_with(square2))
                False

            Squares are identical:
                >>> square1 = Square(Point(0, 0), Size(100, 100), 40)
                >>> square2 = Square(Point(0, 0), Size(100, 100), 40)
                >>> print(square1.is_colliding_with(square2))
                True

            Squares with one side of brushes overlapping:
                >>> square1 = Square(Point(0, 0), Size(100, 100), 40)
                >>> square2 = Square(Point(100, 0), Size(100, 100), 40)
                >>> print(square1.is_colliding_with(square2))
                True
            
            Squares with one side of brushes overlapping by one:
                >>> square1 = Square(Point(0, 0), Size(100, 100), 40)
                >>> square2 = Square(Point(140, 0), Size(100, 100), 40)
                >>> print(square1.is_colliding_with(square2))
                True

            Squares with one side overlapping (without brush overlap):
                >>> square1 = Square(Point(0, 0), Size(100, 100), 0)
                >>> square2 = Square(Point(100, 0), Size(100, 100), 0)
                >>> print(square1.is_colliding_with(square2))
                True

            Squares share a corner:
                >>> square1 = Square(Point(0, 0), Size(100, 100), 40)
                >>> square2 = Square(Point(100, 100), Size(100, 100), 40)
                >>> print(square1.is_colliding_with(square2))
                True
            
            Squares brushes share a corner:
                >>> square1 = Square(Point(0, 0), Size(100, 100), 40)
                >>> square2 = Square(Point(140, 140), Size(100, 100), 40)
                >>> print(square1.is_colliding_with(square2))
                True

            One square's corner inside the other:
                >>> square1 = Square(Point(0, 0), Size(100, 100), 40)
                >>> square2 = Square(Point(50, 50), Size(100, 100), 40)
                >>> print(square1.is_colliding_with(square2))
                True
        """
        # self left side is more to the right than other square's right side
        if self.get_left_edge() > square.get_right_edge():
            return False
        # other square's left side is more to the right than self's right side
        if square.get_left_edge() > self.get_right_edge():
            return False
        
        # self bottom is higher than the other square's top
        if self.get_bottom_edge() < square.get_top_edge():
            return False
        # other square's bottom is higher than self's top
        if square.get_bottom_edge() < self.get_top_edge():
            return False
        
        return True
    
    def get_screenshot(self):
        """Capture a screenshot of the square's area.

        This method uses the position and size of the square to take a screenshot 
        of the area it occupies on the screen. The screenshot is captured as an image object.
        Usefull for more accurate counting of the shapes on the screen.

        Returns:
            Image: An image of the square's current area.

        Examples:
            Take a screenshot of the square:
                >>> test_square = Square(Point(0, 0), Size(100, 100), 40)
                >>> image = test_square.get_screenshot()
                >>> print(type(image) is Image)
                True

            Take a screenshot of a square at a different position:
                >>> test_square = Square(Point(50, 50), Size(200, 200), 40)
                >>> image = test_square.get_screenshot()
                >>> print(image.size)  # Ensure the size matches the square dimensions
                (200, 200)
        """
        shape_box = (self.get_left_edge(), self.get_top_edge(), self.size.width, self.size.height)
        return pya.screenshot(region=shape_box)
        

#
#   HELPER FUNCTIONS
#
def create_random_square_within_boundaries(boundaries: Box, size: Size, brush_size: int) -> Square:
    """Create a random square within specified boundaries.

    This function generates a random top-left corner point for a square, ensuring
    that the square fits within the provided boundaries. The size and brush width
    of the square are specified as parameters.

    Args:
        boundaries (Box): The bounding box within which the square can be created.
        size (Size): The size of the square.
        brush_size (int): The width of the brush used to draw the square.

    Returns:
        Square: A new square instance with a random position within the boundaries.

    Examples:
        Create a random square within given boundaries:
            >>> import random
            >>> random.seed(0)
            >>> boundaries = Box(0,0,500,500)
            >>> size = Size(100, 100)
            >>> brush_size = 10
            >>> random_square = create_random_square_within_boundaries(boundaries, size, brush_size)
            >>> print(random_square.top_left)  # Should be within boundaries
            Point(x=197, y=388)
            >>> print(random_square.size)  # Should match the specified size
            Size(width=100, height=100)
    """
    top_left = create_random_point_within_boundaries(
        boundaries,
        modifier_bottom = -size.height,
        modifier_right = -size.width
    )
    return Square(top_left, size, brush_size)


def create_squares(square_count: int, boundaries: Box, square_size: Size, brush_size: int, max_retries: int = 100) -> list[Square]:
    """Create a specified number of non-overlapping squares within given boundaries.

    This function generates a list of squares with specified size and brush width.
    Each square is positioned randomly within the provided boundaries, and overlaps
    with previously created squares are checked to ensure they do not collide.
    If a square cannot be placed after a certain number of retries, an error is raised.

    Args:
        square_count (int): The number of squares to create.
        boundaries (Box): The bounding box within which the squares can be created.
        square_size (Size): The size of each square.
        brush_size (int): The width of the brush used to draw each square.
        max_retries (int, optional): The maximum number of attempts to place a square 
            before raising an error. Defaults to 100.

    Returns:
        list[Square]: A list of created squares that do not overlap.

    Raises:
        RuntimeError: If unable to place a square within the maximum number of retries.

    Examples:
        Create 5 non-overlapping squares within specified boundaries:
            >>> import random
            >>> random.seed(0)
            >>> boundaries = Box(0,0,500,500)
            >>> square_size = Size(50, 50)
            >>> brush_size = 5
            >>> squares = create_squares(5, boundaries, square_size, brush_size)
            >>> print(len(squares))
            5
            >>> for square in squares:
            ...     print(square.top_left)  # Should be within boundaries
            Point(x=432, y=197)
            Point(x=20, y=132)
            Point(x=261, y=248)
            Point(x=207, y=401)
            Point(x=244, y=183)
    """
    def is_new_square_overlapping_with_others(square: Square, squares: list[Square]) -> bool:
        """Check if a new square overlaps with any existing squares.

        This function iterates through a list of existing squares to determine
        if the specified new square collides with any of them. It returns `True`
        if there is an overlap and `False` otherwise.

        Args:
            square (Square): The new square to check for overlap.
            squares (list[Square]): A list of existing squares to check against.

        Returns:
            bool: `True` if the new square overlaps with any existing square, 
                `False` otherwise.

        Examples:
            New square overlaps with others:
                >>> existing_squares = [
                ...     Square(Point(0, 0), Size(100, 100), 10),
                ...     Square(Point(150, 150), Size(100, 100), 10)
                ... ]
                >>> new_square = Square(Point(50, 50), Size(100, 100), 10)
                >>> print(is_new_square_overlapping_with_others(new_square, existing_squares))
                True  # Overlaps with the first square
            
            New Square does not overlap with others:
                >>> existing_squares = [
                ...     Square(Point(0, 0), Size(100, 100), 10),
                ...     Square(Point(150, 150), Size(100, 100), 10)
                ... ]
                >>> new_square = Square(Point(300, 300), Size(100, 100), 10)
                >>> print(is_new_square_overlapping_with_others(new_square, existing_squares))
                False  # No overlap with either square
        """
        for test_square in squares:
            if square.is_colliding_with(test_square):
                return True
        return False

    squares = []
    retries = 0
    for _ in range(square_count):
        this_square = create_random_square_within_boundaries(boundaries, square_size, brush_size)

        if len(squares) == 0:
            # First square created, no need to check for overlap
            squares.append(this_square)
            continue

        while is_new_square_overlapping_with_others(this_square, squares):
            this_square = create_random_square_within_boundaries(boundaries, square_size, brush_size)
            retries += 1
        
            if retries > max_retries:
                raise RuntimeError("Unable to create legal square in 100 tries")
        retries = 0
        squares.append(this_square)

    return squares