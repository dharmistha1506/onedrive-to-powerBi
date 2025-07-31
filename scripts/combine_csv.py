import os
import pandas as pd

# Local paths in GitHub runner
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
            csv_path = os.path.join(folder, file)
            print(f"Reading {csv_path}")
            df = pd.read_csv(csv_path)
            dfs.append(df)

combined = pd.concat(dfs, ignore_index=True)
combined_file = os.path.join(output_folder, "combined.csv")
combined.to_csv(combined_file, index=False)
print(f"Combined file saved to {combined_file}")
