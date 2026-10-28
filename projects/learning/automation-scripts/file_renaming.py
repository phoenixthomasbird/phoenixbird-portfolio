
import os

def rename_files(folder_path):
    for count, filename in enumerate(os.listdir(folder_path)):
        new_name = f"file_{count}.txt"
        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_name))
    print("Files renamed successfully.")

#run this script in Google Colab with a valid folder path
rename_files("/content/sample_data/")

