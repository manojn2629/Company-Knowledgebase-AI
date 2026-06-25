import pandas as pd


def load_excel(file_path):
    # Load CSV or Excel
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    rows = []

    # Convert each row into structured text
    for _, row in df.iterrows():
        row_text = " | ".join(
            [
                f"{col}: {row[col]}"
                for col in df.columns
            ]
        )

        rows.append(row_text)

    return rows