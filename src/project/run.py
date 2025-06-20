from .path import get_path, valid_project
from pyxora.utils import asyncio,python
import os

def run(args):
    """Run a project."""
    path = get_path(args.name)
    if not valid_project(path):
        print(f"No project found with name '{args.name}'")
        return

    # move to run path
    os.chdir(path)
    # load the main class
    main = python.load_class(os.path.join(path,"main.py"), "main")
    # run the main class
    asyncio.run(main)
    return path
