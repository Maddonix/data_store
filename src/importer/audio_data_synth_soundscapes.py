from ..importer.base_importer import BaseImporter, import_tuple
from typing import List, Optional
from pathlib import Path
from pydantic import BaseModel
import pandas as pd
import torchaudio
from ..schemas.base_schemas import DataModel
from ..crud import create_import_tuple
from tqdm.auto import tqdm

class SynthAudioConfig(BaseModel):
    ref_db: int
    duration: float
    min_events: int
    max_events:int
    pitch: dict
    snr: dict
    source_time:dict
    event_duration:dict
    event_time:dict
    time_stretch: dict
    fg_labels_used: List
    original_filename: Optional[str]

    class Config:
        orm_mode = True

class ImporterAudioDataSynthSoundscapes(BaseImporter):
    '''
    Expects two filelists
    '''
    def __init__(self):
        self.name = "ImporterAudioDataSynthSoundscapes"
        self.label_colnames = ["onset", "offset", "label"]
        self.multiclass = True
        self.multilabel = True
        

    def import_file_list(self, paths_data: List[Path], paths_labels: List[Path], synth_config: dict):
        assert len(paths_data) == len(paths_labels)
        self.synth_config = SynthAudioConfig(**synth_config)

        for i, path_data in enumerate(tqdm(paths_data)):
            path_label = paths_labels[i]
            new_import = self.make_import_tuple(path_data, path_label)
            create_import_tuple(new_import, ImporterAudioDataSynthSoundscapes)

    def read_audio(self, path: Path):
        sig, sr = torchaudio.load(path)
        return sig, sr

    def read_label(self, path: Path) -> pd.DataFrame:
        return pd.read_csv(
            path, sep = "\t", names = self.label_colnames, index_col = False
        )

    def get_db_engine(self): 
        engine = None
        return engine

    def make_import_tuple(self, path_data, path_label) -> import_tuple:
        data = self.read_audio(path_data)
        labels = self.read_label(path_label)
        config = self.synth_config.dict()
        config["original_filename"] = path_data.name
        config["samplerate"] = data[1]
        config["labels"] = config.pop("fg_labels_used")
        data_object = DataModel(
            labelmap_id = 0,
            dataloader_id = 0,
            base_path = Path("data/audio/synth").absolute().as_posix(),
            multiclass = self.multiclass,
            multilabel = self.multilabel
        )
        return import_tuple(data_object, data, labels, config)

    def save(self, path: Path, data):
        path = path.with_suffix(".wav")
        sig, sr = data[0], data[1]
        torchaudio.save(path, sig, sr)

