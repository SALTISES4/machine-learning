import io
import os
import pickle
import zipfile
from itertools import product
from typing import Dict, List

import requests

from src.utils import done_print, load_print


def read_data(language: str) -> Dict[int, List[Dict[str, float]]]:
    path = os.path.join(
        os.path.dirname(__file__), *[os.pardir] * 3, "data", "ngrams", language
    )

    pkl_path = os.path.join(path, "data.pkl")

    if os.path.exists(pkl_path):
        load_print(f"Reading pickled file for {language}...")
        with open(pkl_path, "rb") as f:
            data = pickle.load(f)
        done_print(f"Read pickled file for {language}.")

    else:
        data = {
            gram: read_gram_file(language, gram, path) for gram in (1, 2, 3)
        }
        data = {
            gram: {
                "".join(g): val.get("".join(g), 1e-16)
                for g in product(*["".join(data[1].keys())] * gram)
            }
            for gram, val in data.items()
        }
        load_print(f"Pickling data for {language}...")
        with open(pkl_path, "wb") as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        done_print(f"Pickled data for {language}.")

    return data


def read_gram_file(
    language: str, gram: int, path: str
) -> List[Dict[str, float]]:
    path = os.path.join(path, f"{gram}-grams.txt")
    if os.path.exists(path):
        load_print(f"Reading {gram}-gram file for {language}...")
        with open(path, "r") as f:
            f.readline()
            lines = [line.strip().split() for line in f]
            data = {line[0]: float(line[1]) for line in lines}
        done_print(f"Read {gram}-gram file for {language}.")
    else:
        data = download_gram_file(language, gram, path)

    return data


def download_gram_file(
    language: str, gram: int, path: str
) -> List[Dict[str, float]]:
    load_print(f"Downloading {gram}-gram file for {language}...")
    base_url = "http://practicalcryptography.com/media/cryptanalysis/files"
    if language == "english":
        if gram == 1:
            url = f"{base_url}/english_monograms.txt"
        elif gram == 2:
            url = f"{base_url}/english_bigrams_1.txt"
        elif gram == 3:
            url = f"{base_url}/english_trigrams.txt.zip"
        else:
            raise ValueError(
                f"There is no file for {gram}-grams in {language}."
            )
    elif language == "french":
        if gram == 1:
            url = f"{base_url}/french_monograms.txt"
        elif gram == 2:
            url = f"{base_url}/french_bigrams.txt"
        elif gram == 3:
            url = f"{base_url}/french_trigrams.txt.zip"
        else:
            raise ValueError(
                f"There is no file for {gram}-grams in {language}."
            )
    else:
        raise ValueError(f"There is no file for {gram}-grams in {language}.")

    resp = requests.get(url)

    if url.endswith("zip"):
        with zipfile.ZipFile(io.BytesIO(resp.content)) as f_zip:
            with f_zip.open(os.path.basename(url)[:-4]) as f:
                lines = [line.strip().split() for line in f]
                data = {
                    line[0].decode().lower(): int(line[1]) for line in lines
                }

    else:
        lines = [
            line.strip().split()
            for line in resp.content.decode().split("\n")
            if line
        ]
        data = {line[0].lower(): int(line[1]) for line in lines}

    total = sum(data.values())
    data = {key: val / total for key, val in data.items()}

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write("n-gram\tfrequency\n")
        for n_gram, frequency in data.items():
            f.write(f"{n_gram}\t{frequency}\n")

    done_print(f"Downloaded {gram}-gram file for {language}.")
    return data
