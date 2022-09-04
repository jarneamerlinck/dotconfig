from pathlib import Path

INPUT_DIR = Path.cwd() / "/home/eragon/repos/fluves/files"
for file in list(INPUT_DIR.rglob("*.*")):
    f = open(file, "r")