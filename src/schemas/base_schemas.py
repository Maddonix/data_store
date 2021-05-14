from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.sqltypes import Boolean, Integer, String, Date
from ..db import get_engine
from pydantic import BaseModel, constr
from typing import List, Optional
from datetime import date

Base = declarative_base()
engine = get_engine()


class Data(Base):
    __tablename__ = "data_storage"

    id = Column(Integer, primary_key=True)
    labelmap_id = Column(Integer, nullable=False)
    dataloader_id = Column(Integer, nullable=False)
    base_path = Column(String(255), nullable=False)
    multiclass = Column(Boolean, nullable=False)
    multilabel = Column(Boolean, nullable=False)
    creation_date = Column(Date, default = date.today())

    def __repr__(self):
        return f"id={self.id!r},labelmap_id= {self.labelmap_id!r}, dataloader_id= {self.dataloader_id!r},base_path: {self.base_path!r}, multiclass: {self.multiclass!r}, multilabel: {self.multilabel!r}, creation_date: {self.creation_date!r}"


class DataModel(BaseModel):
    id: Optional[int]
    labelmap_id: int
    dataloader_id: int
    base_path: constr(max_length=255)
    multiclass: bool
    multilabel: bool
    creation_date: Optional[date]

    class Config:
        orm_mode = True


Base.metadata.create_all(engine)
