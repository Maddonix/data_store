from sqlalchemy.orm import Session
from .schemas.base_schemas import Data, DataModel
from .db import get_engine
from .importer.base_importer import import_tuple
from pathlib import Path
import json
from .utils.filepaths import get_data_storage_path
from .labelmaps.labelmaps import labelmaps
import pandas as pd
from typing import List

debug = False

# CREATE
def create_import_tuple(import_data: import_tuple, Importer):
    """Expects a import tuple and an Importer. Will Generate a db entry for the new file and save a data, a metadata (config), and a label file.

    Args:
        import_data (import_tuple): Data to import.
        Importer (Importer Class): Class which importer to use for the data.
    """
    data_object = import_data.data_object
    with Session(get_engine(test = debug)) as sess:
        new_data = Data(**data_object.dict())
        sess.add(new_data)
        sess.commit()
        sess.refresh(new_data)
        path = get_data_storage_path(new_data.base_path, new_data.id, ".HALLODRI")

    save_data(path, import_data.data, Importer)
    save_labels(path, import_data.labels, data_object.labelmap_id)
    save_config(path, import_data.config)

def save_data(data_path: Path, data, Importer):
    importer = Importer()
    importer.save(data_path, data)

def save_config(data_path: Path, config:dict):
    data_path = data_path.with_suffix(".json")
    with open(data_path, "w") as f:
        json.dump(config, f)

def save_labels(data_path: str, labels, labelmap_id:int):
    assert labelmap_id in labelmaps
    LabelMap = labelmaps[labelmap_id]
    labels = LabelMap(labels, data_path.with_suffix(".csv"))
    labels.save()


# READ
def read_data_by_labelmap_id(labelmap_id: int, data_suffix: str) -> pd.DataFrame:
    """Expects a labelmap id and a file suffix. Will return a dataframe containing information for all data tagged with this labelmap id.

    Args:
        labelmap_id (int): id of the labelmap we want to filter for
        data_suffix (str): suffix to append to all filepaths

    Returns:
        pd.DataFrame: Dataframe with two columns. Paths: strings to the data file. Labels: Set of all possible labels for this labelmap.
    """
    with Session(get_engine(test = debug)) as sess:
        q = sess.query(Data).filter(Data.labelmap_id == labelmap_id).all()
        results = [DataModel.from_orm(r) for r in q]
    paths = []
    labels = []
    for object in results:
        path_cfg = get_data_storage_path(object.base_path, object.id, ".json")
        paths.append(path_cfg.with_suffix(data_suffix))
        with open(path_cfg, "r") as f:
            cfg = json.load(f)
            labels.append(set(cfg["labels"]))

    df = pd.DataFrame(data = {"paths": paths, "labels": labels})
    return df
    
def filter_data_by_labels(df:pd.DataFrame, classes: List) -> pd.DataFrame:
    """Expects a dataframe. Dataframe needs to have column "labels" containing sets of all labels annotated for this class.

    Args:
        df (pd.DataFrame): 
        classes (List): List of classes we want to match 

    Returns:
        pd.DataFrame: [description]
    """
    labels = df["labels"].copy()
    # targets = [set(classes)]*len(labels)
    targets = set(classes)

    keep_values = [_ == targets for _ in labels]#(targets - labels).apply(len) == 0
    df = df[keep_values]

    return df


# UPDATE


# DELETE

