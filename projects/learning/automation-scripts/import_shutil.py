import os
import shutil
from pathlib import Path

def organize_files(directory):
    #convert directory to Path object for easier handling.
    dir_path = Path(directory)

    #check if the directory exists
    if not dir_path.exists():
        print(f"Error: Directory '{directory}' does not exist.")
        return
    
    #get all files in the directory
    files = [f for f in dir_path.iterdir() if f.is_file()]

    if not files:
        print("No files found in the directory.")
        return
    
    #process each file
    for file_path in files:
        #get the file extension (converted to lowercase)
        extension = file_path.suffix.lower()

        #skip files without an extension
        if not extension:
            print(f"Skipping '{file_path.name}' (no extension)")
            continue

        #remove the dot from the extension
        extension = extension[1:]

        #create a new folder name based on the extension
        new_folder = dir_path / extension

        #create the folder if it doesn't exist
        try:
            new_folder.mkdir(exist_ok=True)
        except Exception as e:
            print(f"Error creating folder '{new_folder}': {e}")
            continue

        #define the new file path
        new_file_path = new_folder / file_path.name

        #move the file
        try:
            shutil.move(str(file_path), str(new_file_path))
            print(f"Moved '{file_path.name}' to '{extension}' folder")
        except Exception as e:
            print(f"Error moving '{file_path.name}': {e}")


def main():
    #specify your directory.
    directory = os.path.expanduser("~/Downloads")

    #print opening message, organize files, and print completion message
    print(f"Organizing files in: {directory}")
    organize_files(directory)
    print("File organization complete!")


if __name__ == "__main__":
    main()