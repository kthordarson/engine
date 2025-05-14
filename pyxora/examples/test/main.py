# /// script
# dependencies = [
#   "pyxora",
#   "pygame-ce"
# ]
# ///

import pyxora
from pyxora.utils import python

async def main():
    """initializing the engine and starting the main scene."""

    pyxora.debug = False

    # Initialize the display (window size, title, etc.)
    pyxora.Display.init(
        title="Test", 
        resolution=(500,500),
        fullscreen = False,
        resizable = True,
        stretch=True
    )

    '''
    # Load game assets (e.g., images, sounds, etc.)
    pyxora.Assets.init(
        path_data="/data",
        path_scenes="/scenes",
        path_scripts="/scripts",
        pre_load = True
    )

    # Create and configure the initial scene (scene name,**kwargs)
    pyxora.Scene.Manager.create("platformer", max_fps=-1)
    '''

    # This line is going to change.
    # Now load the scene here because the Asset Manager is not ready.
    scene_class = python.get_class(
        module = python.load_module("/scenes/test.py"),
        class_name = "Test"
    )
    pyxora.Scene.Manager.create(scene_class,max_fps=-1)

    # Start the async scene
    await pyxora.Scene.Manager.start()

if __name__ == "__main__":
    pyxora.asyncio.run(main)