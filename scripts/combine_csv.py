import os
import pandas as pd

# Folders where download_onedrive.py stored the files
folders = [
    "data/work_hour_data",
    "data/emp_details",
    "data/dept_tft_work_hour"
]

output_folder = "data/combined"
os.makedirs(output_folder, exist_ok=True)

dfs = []
for folder in folders:
    for file in os.listdir(folder):
        if file.endswith(".csv"):
            path = os.path.join(folder, file)
            print(f"Reading {path}")
            df = pd.read_csv(path)
            dfs.append(df)

combined = pd.concat(dfs, ignore_index=True)
output_file = os.path.join(output_folder, "combined.csv")
combined.to_csv(output_file, index=False)
print(f"Combined file saved to {output_file}")
