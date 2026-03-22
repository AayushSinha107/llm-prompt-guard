import pandas as pd
from datasets import load_dataset
import os

def download_and_save():
    # 1. Create the data folder if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Created 'data/' directory.")

    print("Downloading dataset from Hugging Face...")
    # 2. Load the dataset (this might take a second)
    dataset = load_dataset("deepset/prompt-injections")
    
    # 3. Convert to a Pandas DataFrame
    # This dataset has 'train' and 'test' splits; we'll combine or just use train
    df = pd.DataFrame(dataset['train'])
    
    # 4. Save to your data folder
    file_path = 'data/prompt_injections.csv'
    df.to_csv(file_path, index=False)
    
    print(f"✅ Success! Data saved to {file_path}")
    print(f"Total rows: {len(df)}")
    print("\nFirst few rows:")
    print(df.head())

if __name__ == "__main__":
    download_and_save()