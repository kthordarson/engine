import subprocess
import os

base_argv = [
    "pdoc", "--docformat=google",
    "--logo", "http://localhost:8000/logo.png",
    "--favicon", "http://localhost:8000/icon.png",
    "pyxora", "!pyxora.examples"
]

def run():
    # create a http server to host the images
    server = subprocess.Popen(
        ["python", "-m", "http.server","8000","--directory","docs/data"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    try:
        subprocess.run(base_argv)
    finally:
        server.terminate()

def build():
    import shutil
    base_argv[3] ="/data/logo.png" # logo
    base_argv[5] ="/data/icon.png" # favicon
    output = os.path.abspath(input("Output path (folder): ") + "/build")
    argv = base_argv + ["-o", output]
    subprocess.run(argv)
    shutil.copytree("docs/data", os.path.abspath(os.path.join(output, "data")), dirs_exist_ok=True)

    print("Done")
