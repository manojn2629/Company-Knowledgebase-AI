import os


def get_pdf_files(folder_path):
    files = []

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            files.append(os.path.join(folder_path, file))

    return files