from . import Display,debug
from .utils import python,engine,asyncio

from time import perf_counter as time
from typing import Any

import pygame

class SceneManager:
    """The Main Manager of the Scenes."""
    scene: tuple[str, "Scene"] = (None, None)
    """The current scene (name and scene object)."""

    # --- Scene Control ---
    @classmethod
    async def start(cls) -> None:
        """
        Start the main game loop.
        """
        scene_object = cls.scene[1]
        if not scene_object:
            raise Exception("No scene selected")
        
        # Main game loop
        while True:
            await scene_object.run()
            await asyncio.sleep(0)
    '''
    @classmethod
    def create(cls, name: type, **kwargs: Any) -> None:
        scenes = Assets.data.get("scenes")
        scene_object = scenes.get(name, None)
        if not scene_object:
            engine.error(RuntimeError(f"Scene: {name}, not found in Assets/scenes"))
            engine.quit() 

        scene_class = getattr(scene_object, name.capitalize(), None)
        if not scene_class:
            engine.error(RuntimeError(f"Scene: {name} has not class with name {name.capitalize()}"))
            engine.quit()

        scene_instance = scene_class(**kwargs)
        cls._set_scene(name, scene_instance)
    '''

    @classmethod
    def create(cls, scene_class: type, **kwargs: Any) -> None:
        """
        Create a new scene instance.

        Args:
            scene_class (type): The class of the scene.
            kwargs: Additional arguments passed to the scene's constructor.
        """

        scene_instance = scene_class(**kwargs)
        scene_name = scene_instance.__class__.__name__
        cls._set_scene(scene_name, scene_instance)

    @classmethod
    def __exit(cls) -> None:
        """Exit the current scene."""
        scene_obj = cls.scene[1]
        if scene_obj:
            scene_obj.exit()

    '''
    @classmethod
    def change_to(cls, name: str) -> None:
        """
        Exit and change to a different scene.

        Args:
            name (str): The name of the scene to switch to.
        """
        cls.__exit()
        cls.create(name)

    @classmethod
    def restart(cls) -> None:
        """
        Restart the current scene.
        """
        cls.__exit()
        scene_name = cls.scene[0]
        if scene_obj:
            cls.create(scene_name)

    @classmethod
    def reset(cls) -> None:
        """
        Reset the current scene by re-creating it.
        """
        scene_name = cls.scene[0]
        if not scene_name:
            return

        cls.__exit()
        cls.change_to(scene_name)

    '''

    @classmethod
    def pause(cls) -> None:
        """
        Pause the current scene.
        """
        scene_obj = cls.scene[1]
        if scene_obj:
            scene_obj.pause()

    @classmethod
    def resume(cls) -> None:
        """Resumes the current scene."""
        scene_obj = cls.scene[1]
        if scene_obj:
            scene_obj.resume()

    @classmethod
    def quit(cls) -> None:
        """
        Quit the application through the current scene.
        """
        scene_obj = cls.scene[1]
        if scene_obj:
            scene_obj.quit()

    @classmethod
    def _set_scene(cls, name: str, scene: "Scene") -> None:
        """
        Set the current scene.

        Args:
            name (str): The name of the scene.
            scene (Scene): The scene object.

        Returns:
            Tuple[str, Scene]: A tuple containing the scene name and the scene instance.
        """
        cls.scene = (name, scene)

class SceneEvent:
    """
    A helper class to create custom events for the Scenes.
    """
    def __init__(self,scene: "Scene") -> None:
        """
        @private
        (Not include in the docs as it should be call only inside scene itself)
        Updates all the custom events and it's properties at the scene state.

        Initializes a Scene Event.

        Args:
            scene (SceneManager): The reference to the current Scene.
        """
        self.__data = {}
        self.__scene = scene

    def create(self,name: str,state: int = 0,**kwargs: Any) -> int:
        """
        Create and store a new custom event.

        Args:
            name (str): The name of the event.
            state (int): The event state, where:
                - 1: Runtime
                - -1: Pause time
                - 0: Both (default = 0)
            **kwargs: Additional arguments passed to the event's info. Can be any extra data needed for the event.

        Returns:
            int: The ID of the new event.
        """
        event_id = pygame.event.custom_type()
        create_time = self._now(state)
        last_time = create_time
        basic_argv = {
            "name":name,"custom":True,
            "create_time":create_time,"calls":0,
            "last_time":last_time,"timer":None,
            "loops":None,"state":state
        }

        kwargs.update(basic_argv)
        event = pygame.event.Event(
            event_id,
            kwargs
        )

        self.__data[name] = event
        return event_id

    def get(self,name: str) -> pygame.event.Event:
        """
        Get a custom event by its name.

        Args:
            name (str): The name of the event.

        Returns:
            pygame.event.Event or None: The event with the specified name, or None if not found.
        """
        return self.__data.get(name,None)

    def remove(self,name: str) -> "SceneEvent":
        """
        Remove a custom event by its name.

        Args:
            name (str): The name of the event.

        Returns:
            SceneEvent: The event that was removed
        """
        return self.__data.pop(event_name)

    def post(self,name: str) -> bool:
        """
        Post a custom event by its name.

        Args:
            name (str): The name of the event.

        Returns:
            bool: returns a boolean on whether the event was posted or not
        """
        event = self.get(name)
        return pygame.event.post(event)

    def match(self,name: str,other_event: "SceneEvent") -> bool:
        """
        Check if a custom event matches by its name.

        Args:
            name (str): The name of the event.
            other_event (SceneEvent): The event to compare against.

        Returns:
            bool: True if the events match, False otherwise.
        """
        event = self.get(name)
        return event.type == other_event.type

    # Handling events manually seems more flexible and easier for this use case.
    def schedule(self,name: str,timer: int,loops: int = -1) -> None:
        """
        Shedule a custom event by it's name, for ms timer and loop times.

        Args:
            name (str): The name of the event.
            timer (int): The time of the shedule in ms.
            loops (int): The amount of loop times (default = -1, forever).
        """
        event = self.get(name)
        event.timer = timer
        event.loops = loops

    # Update all the scene events and it properties
    def update(self,state: int):
        """
        @private
        
        (Not include in the doc as it should be call only inside scene itself)
        Updates all the custom events and it's properties at the scene state.

        Args:
            state (int): The scene state. (default = -1, forever).
        """
        for event_name in self.__data:
            event = self.get(event_name)

            if not(self._is_state(state,event.state)):
                continue

            if not event.timer:
                continue

            if event.calls == event.loops:
                continue

            self._update_time(event)

    def _now(self, state: int) -> float:
        """Returns the current time based on the state.

        Args:
            state (int): Determines which time value to return.
                - If 0: Returns runtime + pausetime.
                - If >0: Returns runtime.
                - If <0: Returns pausetime.

        Returns:
            float: The calculated current time value.
        """
        runtime = self.__scene.runtime
        pausetime = self.__scene.pausetime
        if state == 0:
            return runtime + pausetime

        now = runtime if state > 0 else pausetime
        return now


    def _update_time(self, event:"Event") -> None:
        """Checks if an event should be triggered based on elapsed time.

        If the time since the last event trigger exceeds the timer threshold,
        the event is posted and its last_time is updated.

        Args:
            event (object): An object with the following attributes:
                - state (int): State used to determine which time value to use.
                - last_time (float): Timestamp of the last event trigger.
                - timer (float): Timer threshold in milliseconds.
                - name (str): Name of the event to post.

        Side Effects:
            Posts the event via self.post() if the condition is met.
            Updates event.last_time.
        """
        now = self._now(event.state)
        diff = (now - event.last_time) * 1000
        is_time = diff >= event.timer
        if not is_time:
            return

        self.post(event.name)
        event.last_time = now
        event.calls += 1


    @staticmethod
    def _is_state(state: int, event_state: int)-> bool:
        """Checks if the event state matches the given state or is neutral (0).

        Args:
            state (int): Target state to compare against.
            event_state (int): Current state of the event.

        Returns:
            bool: True if the event_state equals the state or is 0, False otherwise.
        """
        same = event_state == state
        is_zero = event_state == 0
        return (same or is_zero)

class Scene:
    Manager = SceneManager
    """Manager: Reference to the scene manager (SceneManager)."""

    Display = Display
    """ Display: Reference to the scene's display handler (pyxora.Display)."""

    global_runtime = 0
    """ global_pausetime: The global runtime for all the scenes."""    
    global_pausetime = 0
    """ global_runtime: The global pause time for all the scenes."""    
    _global_start_time = time()

    def __init__(self,**kwargs: Any) -> None:
        """
        Initializes a Scene object.
        
        Args:
            **kwargs: Additional arguments passed to the scene. Can be any extra data needed for the scene.

        Raises:
            RuntimeError: If the Display has not been initialized. Call Display.init() first.
        """
        if not self.Display.window:
            engine.error(RuntimeError("Display has not been initialized! Call Display.init first."),debug)
            self.quit()

        self.__initialize(kwargs)

    # Lifecycle Methods
    def _start(self) -> None:
        """
        @public
        Called once at the start of the scene. You must Override this func in your subclass.

        Raises:
            NotImplementedError: If not overridden.
        """
        raise NotImplementedError("start() must be overridden in subclass.")

    def _update(self) -> None:
        """
        @public
        Called every frame to update scene logic. You must Override this func in your subclass.

        Raises:
            NotImplementedError: If not overridden.
        """
        raise NotImplementedError("update() must be overridden in subclass.")

    def _draw(self) -> None:
        """
        @public
        Called every frame to draw elements to the screen. You must Override this func in your subclass.

        Raises:
            NotImplementedError: If not overridden.
        """
        raise NotImplementedError("draw() must be overridden in subclass.")

    # Paused Lifecycle Methods
    def _paused_update(self) -> None:
        """@public Called every paused frame to update scene logic. Override this func in your subclass."""
        pass
    def _paused_draw(self) -> None:
        """@public Called every paused frame to draw elements to the screen. Override this func in your subclass."""        
        pass

    # Scene State Change Methods
    def _on_create(self) -> None:
        """@public Called once at the scene creation "SceneManager.create()". Override this func in your subclass to add code."""
        pass
    def _on_quit(self) -> None:
        """@public Called once at the scene quit "Scene.quit()". Override this func in your subclass to add code."""
        pass
    def _on_resume(self) -> None:
        """@public Called once at the scene resume "Scene.resume()". Override this func in your subclass to add code."""
        pass
    def _on_pause(self) -> None:
        """@public Called once at the scene pause "Scene.pause()". Override this func in your subclass to add code."""
        pass
    def _on_error(self,error: BaseException) -> None:
        """
        @public
        Called once at engine error "Scene.__handle_error()". Override this func in your subclass to add code.

        Args:
            error (BaseException): The engine error that occurred.
        """
        pass

    # Scene Event/Input Methods
    def _on_event(self, event: pygame.Event) -> None:
        """
        @public
        Called every pygame event. Override this func in your subclass to add code.

        Args:
            event (pygame.Event): The pygame event that occurred.
        """
        pass
    def _on_keydown(self,key: str) -> None:
        """
        @public
        Called every keyboard keydown. Override this func in your subclass to add code.

        Args:
            key (str): The keyboard key.
        """
        pass
    def _on_keyup(self,key: str) -> None:
        """
        @public
        Called every keyboard keyup. Override this func in your subclass to add code.

        Args:
            key (str): The keyboard key.
        """
        pass
    def _on_keypressed(self,key: str) -> None:
        """
        @public
        Called every keypressed. Override this func in your subclass to add code.

        Args:
            key (str): The keyboard key.
        """
        pass
    def _on_mousewheel(self,wheel: int) -> None:
        """
        @public
        Called every mousewheel change. Override this func in your subclass to add code.

        Args:
            wheel (int): The wheel position, wheel>0 = up, wheel<1 = down.
        """
        pass

    # Paused Event/Input Methods
    def _on_paused_event(self, event: pygame.event.Event) -> None:
        """
        @public
        Called every paused pygame event. Override this func in your subclass to add code.

        Args:
            event (pygame.Event): The pygame event that occurred.
        """
        pass
    def _on_paused_keydown(self,key: str) -> None:
        """
        @public
        Called every paused keyboard keydown. Override this func in your subclass to add code.

        Args:
            key (str): The keyboard key.
        """
    def _on_paused_keyup(self,key: str) -> None:
        """
        @public
        Called every paused keyboard keypressed. Override this func in your subclass to add code.

        Args:
            key (str): The keyboard key.
        """
        pass
    def _on_paused_keypressed(self,key: str) -> None:
        """
        @public
        Called every paused keypressed. Override this func in your subclass to add code.

        Args:
            key (str): The keyboard key.
        """
        pass
    def _on_paused_mousewheel(self,wheel: int) -> None:
        """
        @public
        Called every paused mousewheel change. Override this func in your subclass to add code.

        Args:
            wheel (int): The wheel position, wheel>0 = up, wheel<1 = down.
        """
        pass

    # Main Loop
    # Async to support pygbag export
    async def run(self) -> None:
        """
        Starts the scene.

        Raises:
            Exception: If there is any error in the scene.
        """
        try:
            self.__initialize_runtime()
            self._start()

            while self.__running:
                self.__handle_events()
                self.__update()
                self.__render()
                self.__flip()

                await asyncio.sleep(0)

        except Exception as e:
            self.__handle_error(e)

    # Scene Management
    def pause(self) -> None:
        """Pauses the scene."""
        self.__paused = True
        self.__pause_last_time = time()
        self._on_pause()

    def resume(self):
        """Resumes the scene."""
        self.__paused = False
        # reset the dt for one frame after the pause
        # that reduces any potensial spikes from the high pause fps
        # I might need to find a better solution in the future
        self.dt = 0
        self._on_resume()

    def exit(self):
        """Exits the game loop."""
        self.__running = False

    def quit(self):
        """Quits the game entirely."""
        self._on_quit()
        engine.quit()

    # Scene-Utils
    def is_time(self,ms):
        """Checks if a specified time interval has elapsed since the last frame."""
        multiplier = 1/ms*1000
        return int(self.runtime * multiplier) != int((self.runtime - self.dt) * multiplier)

    def is_event(self,event_id):
        """Checks if an event is happening during the frame. """
        return event_id in self.events

    def is_custom_event(self,event_name):
        """Checks if a custom event is happening during the frame. """
        return event_name in self.custom_events    

    def is_paused(self):
        """Returns if the scene is paused."""
        return self.__paused

    def get_mouse_pos(self):
        """Gets the current mouse pos."""
        return pygame.mouse.get_pos()

    # Private Methods
    def __initialize(self,kwargs):
        try:
            self.max_fps = 60
            self.background_color = (0, 0, 0)

            self.__running = True
            self.__paused = False

            self.__event_handlers = {
                True:  (self._on_paused_keydown, self._on_paused_keyup, self._on_paused_keypressed, self._on_paused_mousewheel, self._on_paused_event),
                False: (self._on_keydown,        self._on_keyup,        self._on_keypressed,        self._on_mousewheel,        self._on_event)
            }

            # set manual the scene kwargs to the scene
            for k, v in kwargs.items(): 
                setattr(self, k, v)
            self._on_create()
        except Exception as e:
            # expect on_create error as is not in the main loop
            self.__handle_error(e)

    def __initialize_runtime(self):
        """Sets up initial basic runtime values."""
        self.dt = self.fps = self.runtime = self.pausetime = 0
        self.keys_pressed = set() # we manually keep track with the key_pressed every frame, set so no duplicates
        self.events = set() # log events every frame
        self.custom_events = set() # log custom events every frame

        # Create custom Scene events
        self.Event = SceneEvent(self)
        # self.Camera = pyxora.Camera()

        self._start_time = time()
        self.__running = True

    def __handle_error(self,e):
        """ Handles every possible error with a nice message."""
        self._on_error(e)
        engine.error(e,debug)
        self.quit()

    def __handle_events(self):
        """Handles events during runtime or when paused."""
        self.events.clear()
        self.custom_events.clear()
        self.Event.update(-1 if self.__paused else 1)

        on_keydown, on_keyup, on_keypressed, on_wheel, on_event = self.__event_handlers[self.__paused]
        for event in pygame.event.get():
            self.events.add(event.type)

            if hasattr(event, "custom"):
                self.custom_events.add(event.name)
                continue

            if event.type == pygame.QUIT:
                self.quit()

            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                self.keys_pressed.add(key)
                on_keydown(key)

            elif event.type == pygame.KEYUP:
                key = pygame.key.name(event.key)
                self.keys_pressed.discard(key)
                on_keyup(key)

            elif event.type == pygame.MOUSEWHEEL:
                wheel = "up" if event.y >= 1 else "down"
                on_wheel(wheel)

            elif event.type == pygame.VIDEORESIZE:
                self.Display.resize((event.w, event.h))
                # self.Camera.dynamic_zoom()
            on_event(event)

        if self.keys_pressed:
            on_keypressed(self.keys_pressed)


    def __update(self):
        """Update the scene and timers, depending on whether it's paused or active."""
        update = self._paused_update if self.__paused else self._update
        update_timers = self.__update_paused_timers if self.__paused else self.__update_timers
        update()
        update_timers()

    def __update_timers(self):
        """Updates global and local runtime timers."""
        delta = time() - self._start_time
        global_delta = time() - self._global_start_time

        self.runtime = delta - self.pausetime
        self.global_runtime = global_delta - self.global_pausetime

    def __update_paused_timers(self):
        """Tracks time spent in pause mode."""

        # That was the easiest way to track the duration during the pause
        # but not the best :D
        delta = time() - self.__pause_last_time

        self.pausetime += delta
        self.global_pausetime += delta

        self.__pause_last_time = time()

    # no point to update the fps every frame as is hard to tell with the eye
    # maybe i should change it to average instead?
    def __update_fps(self): 
        """Updates the current scene fps every 250ms."""
        if self.is_time(250):
            self.fps = self.Display.clock.get_fps()

    def __render(self):
        """Renders the scene."""
        if not self.__paused: # skip background if paused to keep the last frame render
            self.__draw_background()
        (self._paused_draw if self.__paused else self._draw)()

    def __draw_background(self):
        """Clears the screen with the background color."""
        self.Display.surf.fill(self.background_color)

    def __draw_display(self):
        """Draws the display."""
        surf = self.Display.get_stretch_surf() if self.Display.is_resized() else self.Display.surf
        self.Display.window.blit(surf,(0,0))

    def __flip(self):
        """Updates the display with the latest frame."""
        self.__update_fps() # I think updating the fps before the flip is the best place?
        self.dt = self.Display.clock.tick(self.max_fps) / 1000 # Also take the dt
        self.__draw_display()
        pygame.display.flip()