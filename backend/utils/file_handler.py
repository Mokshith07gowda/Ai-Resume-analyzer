import os

UPLOAD_DIR = "uploads"

def save_file(filename, content):

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as f:
        f.write(content)

    return path