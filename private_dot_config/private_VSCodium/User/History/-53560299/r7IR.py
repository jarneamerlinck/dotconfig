from pathlib import Path
original_path= "/nas/homes/jarnea-1000035/lanxess/fiber_dts_bandweaver_firelaser_0003"
destination_path = "/nas/homes/jarnea-1000035/lanxess/fiber_dts_bandweaver_firelaser_0003_New"

INPUT_DIR = Path.cwd() / "/home/eragon/repos/fluves/files"
for file in list(INPUT_DIR.rglob("*.*")):
    file.replace(original_path, destination_path)
    print(file_des)