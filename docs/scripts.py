import subprocess

argv = [
    "pdoc", "--docformat=google",
    "pyxora", "!pyxora.examples"
]

def run():
    subprocess.run(argv)

def build():
    import os
    output = os.path.abspath(input("output-path: ")+"/build")
    argv.append("-o")
    argv.append(output)
    subprocess.run(argv)
    print("Done")