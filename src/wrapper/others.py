__all__ = ["vector"]

import pygame

def vector(x: int | float, y: int | float, z: int | float | None = None) -> pygame.math.Vector2 | pygame.math.Vector3:
    """
    Creates a 2D or 3D pygame vector based on the input arguments.

    Parameters:
        x (int | float): X value of the vector.
        y (int | float): Y value of the vector.
        z (int | float | None): Optional Z value; if provided, returns a 3D vector.

    Returns:
        pygame.math.Vector2 or pygame.math.Vector3: A 2D or 3D vector.

    Examples:
        vector(1, 2) -> pygame.math.Vector2(1, 2)\n
        vector(1, 2, 3) -> pygame.math.Vector3(1, 2, 3)
    """
    if z is not None:
        return pygame.math.Vector3(x, y, z)
    return pygame.math.Vector2(x, y)
