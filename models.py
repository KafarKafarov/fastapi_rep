from database import Base
from sqlalchemy import String, Integer, ForeignKey, Column, DateTime, func, Text
from sqlalchemy.orm import relationship

class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    path = Column(String, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())

    _text_obj = relationship(
        'DocumentText',
        uselist=False,
        back_populates='document',
        cascade='all, delete-orphan'
    )

    @property
    def text(self) -> str:
        return self._text_obj.text if self._text_obj and self._text_obj.text else "Not found text"

class DocumentText(Base):
    __tablename__ = 'document_texts'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey('documents.id'), nullable=False)
    text = Column(Text, nullable=True)

    document = relationship('Document', back_populates='_text_obj')

