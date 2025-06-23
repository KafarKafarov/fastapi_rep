from datetime import datetime
from pydantic import BaseModel

class Document(BaseModel):
    id: int
    path: str
    date: datetime| None

    class Config:
        from_attributes = True

class DocumentText(BaseModel):
    id: int
    text: str

    class Config:
       from_attributes = True


class DocumentCreate(Document):
    text: str

class DocumentOut(BaseModel):
    id: int
    path: str
    date: datetime | None
    text: str

    class Config:
        orm_mode = True







