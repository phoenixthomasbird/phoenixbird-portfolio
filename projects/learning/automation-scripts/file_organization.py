
import os
import shutil
def organize_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            shutil.move(os.path.join(folder_path, filename), os.path.join(folder_path, "Images"))
        elif filename.endswith(".pdf") or filename.endswitch(".docx"):
            shutil.move(os.path.join(folder_path, filename), os.path.join(folder_path, "Documents"))

organize_files(os.path.expanduser("~/Documents")) 