from pathlib import Path
original_path= "/home/eragon/repos/fluves/files"
destination_path = "/home/eragon/repos/fluves/files_New"

original_path= "/nas/homes/jarnea-1000035/lanxess/fiber_dts_bandweaver_firelaser_0003"
destination_path = "/nas/homes/jarnea-1000035/lanxess/fiber_dts_bandweaver_firelaser_0003_New"
INPUT_DIR = Path.cwd() / "/home/eragon/repos/fluves/files"
for file_org in list(INPUT_DIR.rglob("*.*")):
    file_des = str(file_org).replace(original_path, destination_path)
    print(file_des)
    fo =  open(file_org,"r")
    fd = open(file_des,"w")
    