import subprocess

logo_url = "https://github.com/ToniDevStuff/pyxora/blob/main/pyxora/data/images/logo.png?raw=true"
icon_url = "https://github.com/ToniDevStuff/pyxora/blob/main/pyxora/data/images/icon.png?raw=true"

argv = [
    "pdoc", "--docformat=google",
    "--logo",logo_url,
    "--favicon",icon_url,
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
