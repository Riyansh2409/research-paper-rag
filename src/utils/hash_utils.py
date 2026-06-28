import os
import hashlib


def generate_documents_hash(folder_path):

    sha256 = hashlib.sha256()

    pdf_files = sorted(
        [f for f in os.listdir(folder_path) if f.endswith(".pdf")]
    )

    for pdf in pdf_files:

        pdf_path = os.path.join(folder_path, pdf)

        with open(pdf_path, "rb") as file:

            while True:

                chunk = file.read(8192)

                if not chunk:
                    break

                sha256.update(chunk)

    return sha256.hexdigest()

HASH_FILE = "data/metadata/document_hash.txt"


def save_hash(document_hash):

    with open(HASH_FILE, "w") as file:
        file.write(document_hash)


def load_hash():

    if not os.path.exists(HASH_FILE):
        return None

    with open(HASH_FILE, "r") as file:
        return file.read().strip()