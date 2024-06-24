import pandas as pd

excel_file = './UBC DB Data Set.xlsx'
xls = pd.ExcelFile(excel_file)

for sheet_name in xls.sheet_names:
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    output_file = f"./myLivingCity_dataset/{sheet_name}.csv"
    df.to_csv(output_file, index=False)
    print(f"Exported {sheet_name} to {output_file}")
