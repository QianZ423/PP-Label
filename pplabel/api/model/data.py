from datetime import datetime

from pplabel.config import db
from ..util import nncol
from .base import BaseModel


class Data(BaseModel):
    __tablename__ = "data"
    __table_args__ = {"comment": "Contains all the data files"}
    data_id = nncol(db.Integer(), primary_key=True)
    task_id = db.Column(db.Integer(), db.ForeignKey("task.task_id", ondelete="CASCADE"))
    path = nncol(db.String())
    slice_count = db.Column(db.Integer())

    _immutables = BaseModel._immutables + ["data_id", "task_id"]