from .others import vector
from abc import ABC, abstractmethod
from math import ceil
from typing import Iterable
import pygame

class Shape(ABC):
    """Abstract base class for all drawable shapes."""
    
    def __init__(self, pos: Iterable[int | float] | pygame.math.Vector2 | pygame.math.Vector3, color: str | tuple):
        """
        Initializes the shape with a position and color.
        
        Args:
            pos (list | tuple | pygame.math.Vector2 | pygame.math.Vector3): The position of the shape.
            color (str | tuple): The color of the shape, either as a string (e.g., "red") or a tuple (R, G, B).
        """
        self.pos = vector(*pos)
        """ The position of the shape"""
        self.color = color
        """ The color of the shape"""

    @property
    @abstractmethod
    def rect(self) -> pygame.Rect | pygame.FRect:
        """Abstract method to get the bounding rectangle of the shape."""
        pass

    @abstractmethod
    def draw(self, surf: pygame.Surface, fill: int, scale: int | float) -> None:
        """
        Abstract method to draw the shape on a surface with a given fill and scale.
        
        Args:
            surf (pygame.Surface): The surface to draw on.
            fill (int): The fill value for the shape (positive values for outline else is solid).
            scale (int | float): The scale factor for the shape size.
        """
        pass


class Rect(Shape):
    """Represents a rectangle shape."""
    
    def __init__(self, pos: Iterable[int | float] | pygame.math.Vector2 | pygame.math.Vector3, size: tuple | list, color: str | tuple):
        """
        Initializes the rectangle with position, size, and color.
        
        Args:
            pos (pygame.math.Vector2 | pygame.math.Vector3): The position of the rectangle.
            size (tuple | list): The size of the rectangle, either as a tuple or list (width, height).
            color (str | tuple): The color of the rectangle, either as a string (e.g., "red") or a tuple (R, G, B).
        """
        super().__init__(pos, color)
        self.size = size
        """ The size of the Rect"""

    @property
    def rect(self) -> pygame.Rect | pygame.FRect:
        """
        Returns the bounding rectangle (pygame.Rect or pygame.FRect) based on coordinate types.
        
        Returns:
            pygame.Rect | pygame.FRect: The bounding rectangle of the shape.
        """
        if all(isinstance(i, int) for i in (self.pos[0], self.pos[1], self.size[0], self.size[1])):
            return pygame.Rect(self.pos, self.size)  # Use pygame.Rect if all values are integers
        return pygame.FRect(self.pos, self.size)  # Use pygame.FRect otherwise

    def draw(self, surf: pygame.Surface, fill: int, scale: int | float) -> None:
        """
        Draws the rectangle on the surface with a given fill and scale.
        
        Args:
            surf (pygame.Surface): The surface to draw on.
            fill (int): The fill value for the shape (positive values for outline else is solid).
            scale (int | float): The scale factor for the rectangle size.
        """
        # Scale the rectangle and fill value
        rect = self.rect
        fill *= scale
        rect.width *= scale
        rect.height *= scale
        fill = ceil(fill)  # Ensure fill is an integer
        
        # Draw the rectangle
        pygame.draw.rect(surf, self.color, rect, width=fill if fill > 0 else 0)


class Circle(Shape):
    """Represents a circle shape."""
    
    def __init__(self, pos: Iterable[int | float] | pygame.math.Vector2 | pygame.math.Vector3, radius: int | float, color: str | tuple):
        """
        Initializes the circle with position, radius, and color.
        
        Args:
            pos (pygame.math.Vector2 | pygame.math.Vector3): The position of the circle.
            radius (int | float): The radius of the circle.
            color (str | tuple): The color of the circle, either as a string (e.g., "red") or a tuple (R, G, B).
        """
        super().__init__(pos, color)
        self.radius = radius
        """ The radius of the Circle"""

    @property
    def rect(self) -> pygame.Rect:
        """
        Returns the bounding rectangle for the circle.
        
        Returns:
            pygame.Rect: The bounding rectangle that encloses the circle.
        """
        pos = (self.pos[0] - self.radius, self.pos[1] - self.radius)  # Top-left corner of the bounding rect
        size = (self.radius * 2, self.radius * 2)  # Size of the bounding rectangle
        return pygame.Rect(pos, size)

    def draw(self, surf: pygame.Surface, fill: int, scale: int | float) -> None:
        """
        Draws the circle on the surface with a given fill and scale.
        
        Args:
            surf (pygame.Surface): The surface to draw on.
            fill (int): The fill value for the circle outline (negative for outline, positive for solid).
            scale (int | float): The scale factor for the circle size.
        """
        # Scale the circle and fill value
        pos = self.pos
        fill *= scale
        radius = self.radius * scale  # Scale the radius
        fill = ceil(fill)  # Ensure fill is an integer
        
        # Draw the circle
        pygame.draw.circle(surf, self.color, pos, radius, width=fill if fill > 0 else 0)