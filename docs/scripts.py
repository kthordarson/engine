import subprocess

logo_url = "https://github.com/ToniDevStuff/pyxora/blob/b1952e81ce8543ef66cf1fabd4ea7dc9ea93f3fe/pyxora/images/icon.png?raw=true"

argv = [
    "pdoc", "--docformat=google",
    "--logo",logo_url,
    "--favicon",logo_url,
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
