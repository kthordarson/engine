# Change the directory to the example's base directory
# This ensures relative paths are working correctly.

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

os.chdir(BASE_DIR)

print('Example Test: ')