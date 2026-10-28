
import shutil

def backup_files(source_folder, backup_folder):
    shutil.copytree(source_folder, backup_folder)
    print("Backup completed.")

backup_files("path/to/source", "path/to/backup")

