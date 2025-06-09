import subprocess

logo_url = "https://github.com/ToniDevStuff/pyxora/blob/gh-pages/data/logo.png?raw=true"
favicon_url = "https://github.com/ToniDevStuff/pyxora/blob/gh-pages/data/favicon.png?raw=true"

argv = [
    "pdoc", "--docformat=google",
    "--logo",logo_url,
    "--favicon",favicon_url,
    "pyxora", "!pyxora.examples"
]

def run():
    subprocess.run(argv)

def build():
    import os
    output = os.path.abspath(os.getcwd()+"/build")
    argv.append("-o")
    argv.append(output)
    subprocess.run(argv)
    print("Done")
