import pygame

class Display:
    """Handles the main game display surface and rendering."""

    window = None
    """The main display window"""

    @classmethod
    def init(cls, title: str, resolution:tuple[int, int] , stretch=False,
             fullscreen=False, resizable=False, vsync=False) -> None:
        """
        Initializes the main display window used by all scenes.

        Args:
            title (str): The title of the window.
            resolution (tuple[int, int]): The resolution of the window (width, height).
            stretch (bool): Whether to stretch the internal surface to fit the screen. Defaults to False.
            fullscreen (bool): Start in fullscreen mode. Defaults to False.
            resizable (bool): Allows the window to be resizable. Defaults to False.
            vsync (bool): Enables vertical sync. Defaults to False.
        """
        cls._title = title
        cls._res = resolution
        cls._width, cls._height = resolution

        cls._vsync = vsync
        cls._fullscreen = fullscreen
        cls._resizable = resizable

        cls._stretch = stretch
        # no camera yet
        # cls._dynamic_zoom = dynamic_zoom

        cls._new_res = None
        cls._last_res = resolution # We also keep last_res so we know what resolution to revert to if needed.

        cls._surf = pygame.Surface(resolution)
        cls._clock = pygame.time.Clock()

        cls.__set_title()
        cls.__set_mode()

    # Note: The classmethod-properties need to be change as they are not going to work for python>=3.13
    # Maybe get_property() is going to be the best replacement.
    # Keeping it this way for now, as i like them. :(

    # Link: https://docs.python.org/3.13/library/functions.html#classmethod

    @classmethod
    @property
    def surf(cls) -> pygame.Surface:
        """pygame.Surface: The main rendering surface."""
        return cls._surf

    @classmethod
    @property
    def clock(cls) -> pygame.time.Clock:
        """pygame.time.Clock: The main clock."""
        return cls._clock

    @classmethod
    @property
    def center(cls) -> tuple:
        """center: tuple[float, float]"""
        return (cls._res[0] / 2, cls._res[1] / 2)

    @classmethod
    def is_resized(cls) -> bool:
        """
        Check if the display has been resized.

        Returns:
            bool: True if a new resolution has been set, otherwise False.
        """
        return bool(cls._new_res)

    @classmethod
    def resize(cls, new_res) -> None:
        """
        Resize the display window.

        Args:
            new_res (tuple[int, int]): The new resolution.
        """
        if not cls._fullscreen:
            cls._last_res = new_res
        cls._new_res = new_res
        cls.__set_mode()

    @classmethod
    def get_stretch_surf(cls) -> pygame.Surface:
        """
        Get a stretched version of the internal surface to the new resolution.

        Returns:
            pygame.Surface: The scaled surface.
        """
        return pygame.transform.scale(cls._surf, cls._new_res)

    @classmethod
    def toggle_fullscreen(cls) -> None:
        """Toggle fullscreen mode on or off."""
        cls._fullscreen = not cls._fullscreen
        cls._fullscreen and pygame.display.toggle_fullscreen()

        not cls._fullscreen and cls.resize(cls._last_res) # If we're exiting fullscreen, we need to resize back to the previous resolution.

    @classmethod
    def draw_shape(cls, Shape, fill=0) -> None:
        """
        Draw a shape on the screen.

        Args:
            Shape: The shape object with a `.draw()` method.
            fill (int, optional): Fill mode or color. Defaults to 0.
        """

        # Just calls the abstracted shape.draw method, so we only need one method to draw any future shape :)
        Shape.draw(cls.surf, fill=fill, scale=1)

    # not ready
    '''
    @classmethod
    def draw_text(cls, Txt) -> None:
        """
        Draw text on the screen.

        Args:
            Txt: A text object with a `.draw()` method.
        """
        Txt.draw(cls.surf, scale=1)

    @classmethod
    def draw_image(cls, Image) -> None:
        """
        Draw an image on the screen.

        Args:
            Image: An image object with a `.draw()` method.
        """
        Image.draw(cls.surf, scale=1)

    '''

    # Note: I planned to use the new pygame.Window for more features,
    # but it caused issues with pybgag (web builds), so set_mode for now.
    @classmethod
    def __set_mode(cls) -> None:
        """Private method to set the display mode based on flags and resolution."""
        res = cls._res if not cls._new_res else cls._new_res
        vsync = int(cls._vsync)

        # apply the flags
        flags = 0
        if cls._resizable:
            flags |= pygame.RESIZABLE 
        if cls._fullscreen:
            flags |= pygame.FULLSCREEN 
            flags |= pygame.HWSURFACE

        cls.window = pygame.display.set_mode(res, flags=flags, vsync=vsync)

    @classmethod
    def __set_title(cls):
        pygame.display.set_caption(cls._title)