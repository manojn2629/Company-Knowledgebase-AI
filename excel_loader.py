import pandas as pd


def load_excel(file_path):
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    rows = []

    for _, row in df.iterrows():
        row_text = " | ".join(
            [str(value) for value in row.values]
        )
        rows.append(row_text)

    return rows