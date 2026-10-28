
import openpyxl

def update_excel(file_path):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    sheet['A1'] = "Updated Value"
    workbook.save(file_path)

update_excel("data.xlsx")

