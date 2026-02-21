import json
import os


BASE_PATH = os.path.dirname(os.path.dirname(__file__))


def _load_json(filename):
    path = os.path.join(BASE_PATH, "data", filename)

    if not os.path.exists(path):
        raise FileNotFoundError(f"{filename} not found in data folder")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------- DOMAIN WEIGHTS ----------
def load_weights():
    return _load_json("domain_weights.json")


# ---------- CAREERS DATABASE ----------
def load_careers():
    return _load_json("careers.json")


# ---------- DOMAIN LIST ----------
def load_domains():
    weights = load_weights()
    return list(weights.keys())
