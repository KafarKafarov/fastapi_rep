from database import Base
from sqlalchemy import String, Integer, ForeignKey, Column, DateTime, func
from sqlalchemy.orm import relationship


class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    path = Column(String, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())

    texts = relationship('DocumentText', back_populates='document', cascade='all, delete-orphan')

class DocumentText(Base):
    __tablename__ = 'document_texts'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey('documents.id'), nullable=False)
    text = Column(String, nullable=True)

    document = relationship('Document', back_populates='texts')
