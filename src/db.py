from pathlib import Path
import json
from sqlalchemy import create_engine

# with open(Path("config.json"), "r") as f:
#     config = json.load(f)
    
# database_path = Path(config["db_path"])
database_path = Path("/home/lux_t1/Desktop/data_store/src/db.db")

def get_engine(test: bool = False):
    if not test:
        return create_engine(f"sqlite+pysqlite:///{database_path.as_posix()}", echo = False, future = True)
    else:
        return create_engine(f"sqlite+pysqlite:///test.db", echo = True, future = True)
