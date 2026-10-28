import os
import platform
from pathlib import Path



#function definition
def walk_directory(directory_path):
    #convert string path to Path object
    root_dir = Path(directory_path.strip())

    #check if the root directory exists
    if not root_dir.exists():
        print(f"Error: Directory '{directory_path}' does not exist.")
        return
    
    #show files in the root directory
    print(f"\n{root_dir.name}:")
    for item in root_dir.iterdir():
        if item.is_file():
            print(f"    {item.name}")

    #walk through subdirectories
    for folder in root_dir.rglob("*"):
        if folder.is_dir() and folder != root_dir: #skip root directory
            print(f"\n{folder.name}")

            #get all the files in the current folder
            for file in folder.rglob("*"):
                if file.is_file():
                    #print the file name indented
                    print(f"    {file.name}")


def main():
    #set the directory path
    #directory = input("Enter the directory path to walk.").strip()
    directory = os.path.expanduser("~/Downloads")

    #if no input, use the current directory
    if not directory:
        directory = "."

    #show the operating system name
    os_name = platform.system()
    print(f"\nOperating System: {os_name}")
    print(f"Scanning directory: {directory}")
    walk_directory(directory)

    print("Done. \n")


if __name__ == "__main__":
    #call the main function
    main()
