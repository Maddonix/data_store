import pandas as pd
from pathlib import Path

class AudioStrongLabels:
    def __init__(self, labels: pd.DataFrame = None, path: Path = None):
        self.labels = labels
        self.path = path
        self.name = "AudioStrongLabels"

    def save(self):
        self.labels.to_csv(self.path, sep = "\t", index = False)

    def read(self, path: Path, label_type: str):
        assert label_type in ["strong", "weak"]
        colnames = ["onset", "offset", "label"]
        if label_type == "strong":
            return pd.read_csv(path, sep = "\t", index_col = False)
        elif label_type == "weak":
            return pd.read_csv(path, sep = "\t", index_col = False)["label"].to_list()

