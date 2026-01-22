import pandas as pd
import re
import os

def clean_text(text):
    """
    Cleans text by lowercasing and removing special characters.
    """
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

def load_data(filepath):
    """
    Loads data from a CSV file.
    """
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return None
    return pd.read_csv(filepath)

def save_data(df, filepath):
    """
    Saves DataFrame to a CSV file.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"Data saved to {filepath}")
