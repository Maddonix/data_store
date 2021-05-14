import torchaudio
from sklearn.preprocessing import MultiLabelBinarizer
from torch.utils.data import Dataset
from tqdm.auto import tqdm
from typing import List
from ..labelmaps.labelmaps import labelmaps
from .. import crud

from ..utils.audio_utils import resample


class AudioDatasetStrong(Dataset):
    def __init__(self, sr: int, classes: List, label_type:str):
        self.labelmap_id = 0
        LabelMap = labelmaps[self.labelmap_id]
        self.labelmap = LabelMap()
        self.sr = sr
        self.label_type = label_type
        self.classes = classes
        self.wav_paths, self.labels = self.get_dataset_labels()

    def __getitem__(self, idx: int):
        audiofile_path = self.wav_paths[idx]
        label_df = self.labels[idx]

        sig, sr = torchaudio.load(audiofile_path)
        if sr is not self.sr:
            sig, sr = resample((sig, sr), self.sr)

        return sig, label_df

    def __len__(self):
        return len(self.wav_paths)

    def get_dataset_labels(self):
        df = crud.read_data_by_labelmap_id(0, ".wav")
        df = crud.filter_data_by_labels(df, self.classes)
        label_paths = [_.with_suffix(".csv") for _ in df["paths"]]
        labels = [self.labelmap.read(_, self.label_type) for _ in tqdm(label_paths)]

        if self.label_type == "weak":
            mlb = MultiLabelBinarizer(classes = self.classes)
            labels = mlb.fit_transform(labels)    
            
        return df["paths"].to_list(), labels