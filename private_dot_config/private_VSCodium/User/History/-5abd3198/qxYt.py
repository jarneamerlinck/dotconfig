from pathlib import Path
INPUT_DIR = Path.cwd() / "Your_Folder_Name"
for file in list(INPUT_DIR.rglob("*.xls*")):