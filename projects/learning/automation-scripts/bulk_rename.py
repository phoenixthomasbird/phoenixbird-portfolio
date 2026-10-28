#IMPORT STATEMENTS
from pathlib import Path


#FUNCTION DEFINITIONS

def rename_files(root_dir, pattern, recursive, preferred_name):

    #try block 
    try:
        root_path = Path(root_dir)

        #if None is provided for preferred_name, use the folder name
        rename_to_folder = True

        #check if root directory exists
        if not root_path.exists():
            raise FileNotFoundError(f"The specified directory '{root_dir}' does not exist")
        
        #set iteration method based on 'recursive' flag
        files = root_path.rglob("*") if recursive else root_path.glob("*")

        #dictionary to track count for each folder
        folder_counts = {}

        for file_path in files:
            if file_path.is_file():
                try:
                    if not pattern or file_path.match(pattern):
                        folder = file_path.parent
                        #update the count for the folder
                        count = folder_counts.get(folder, 0) +1
                        folder_counts[folder] = count

                        if rename_to_folder:
                            base_name = folder.name
                        else:
                            base_name = preferred_name
                        
                        new_name = f"{base_name} ({count}{file_path.suffix})"
                        new_path = folder / new_name

                        file_path.rename(new_name)
                        print(f"Renamed '{file_path.name}' to '{new_path.name}'")

                except PermissionError:
                    print(f"Permission denied: Unable to rename '{file_path}'")

    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except PermissionError as perm_error:
        print(perm_error)
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")


def main():
    #example path
    root_dir = "Users/phoenixthomasbird/Coursera"

    #None to rename all files, or pattern in quotation marks
    pattern = None

    #True to rename files in subfolders, otherwise: False
    recursive = True

    #None for folder name; otherwise name in quotation marks
    preferred_name = None

    print(f"\nRenaming files in '{root_dir}', recursive={recursive}")
    rename_files(root_dir, pattern, recursive, preferred_name)
    print("Renaming completed. \n")


if __name__ == "__main__":
    main()