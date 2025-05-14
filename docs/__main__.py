from .scripts import run,build

import sys

def main():
	argv = sys.argv
	need_build = "--build" in argv or "-b" in argv

	build() if need_build else run()

if __name__ == "__main__":
	main()