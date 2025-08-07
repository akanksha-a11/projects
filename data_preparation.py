# data_preparation.py

import pandas as pd

def load_and_clean_data(file_path):
    try:
        print(f"Loading data from: {file_path}")
        df = pd.read_csv(file_path)

        # Drop any completely empty columns
        df.dropna(axis=1, how='all', inplace=True)

        # Fill missing numeric values with 0
        numeric_cols = df.select_dtypes(include=['number']).columns
        df[numeric_cols] = df[numeric_cols].fillna(0)

        # Fill missing object (string) values with 'Unknown'
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].fillna('Unknown')

        # Normalize column names (remove spaces, lowercase, underscore)
        df.rename(columns={
            'drug source': 'drug_source',
            'drug name': 'drug_name',
            'FDA Code': 'fda_code',
            'medeicare': 'medicare_id'
        }, inplace=True)

        # Create a summary column: drug+source
        df['drug_id'] = df['drug_name'].str.lower().str.replace(" ", "_") + "_" + df['fda_code'].astype(str)

        # Save cleaned file
        cleaned_path = 'cleaned_midcare_data.csv'
        df.to_csv(cleaned_path, index=False)
        return cleaned_path

    except Exception as e:
        print(f"Error during data preparation: {e}")
        return None



# if __name__ == "__main__":
#     load_and_clean_data("midcare_data.csv")

# print(f"Cleaned data saved to: {cleaned_path}")
# print(f"Total Records: {len(df)} | Columns: {df.shape[1]}")