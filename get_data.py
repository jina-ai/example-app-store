import os
import pandas as pd
from backend_config import dataset_url, dataset_filename, random_seed

datadir = "data"

if not os.path.isdir(datadir):
    os.makedirs(datadir)

os.chdir(datadir)

os.system(f"wget {dataset_url} -O {dataset_filename}")

df = pd.read_csv(dataset_filename)
shuffled_df = df.sample(frac=1, random_state=random_seed)

output_filename = f'{dataset_filename.split(".")[0]}-shuffled.csv'
shuffled_df.to_csv(f'{output_filename}')

