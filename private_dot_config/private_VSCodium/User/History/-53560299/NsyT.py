from pathlib import Path


original_path= "/nas/homes/jarnea-1000035/lanxess/fiber_dts_bandweaver_firelaser_0003"
destination_path = "/nas/homes/jarnea-1000035/lanxess/fiber_dts_bandweaver_firelaser_0003_New"
INPUT_DIR = Path.cwd() / "/home/eragon/repos/fluves/files"
for file_org in list(INPUT_DIR.rglob("*.*")):
    file_des = str(file_org).replace(original_path, destination_path)
    
    path_to_make = file_des
    print(path_to_make)
    # fo =  open(file_org,"r")
    # fd = open(file_des,"w")
    # fd.write(fo.read())
    # fo.close()
    # fd.close()
    # print(file_org, "is done")
    