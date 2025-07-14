from datetime import datetime
from database import Base
from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional

class Document(Base):
    __tablename__ = 'documents'

    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

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

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey('documents.id'), nullable=False)
    text: Mapped[Optional[str]] = mapped_column(nullable=True)

    document = relationship('Document', back_populates='_text_obj')

