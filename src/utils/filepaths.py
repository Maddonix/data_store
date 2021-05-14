from pathlib import Path


def get_data_storage_path(base_path: str, id: int, suffix: str = ""):
    """Asserts that base path exists, then joins with id and given suffix

    Args:
        base_path (str): pointing to an existing folder
        id (int): id of object to create a path forr
        suffix (str, optional): suffix to append to the filepath. Defaults to "".

    Returns:
        [type]: [description]
    """
    base_path = Path(base_path)
    assert base_path.exists()
    return base_path.joinpath(str(id)).with_suffix(suffix)