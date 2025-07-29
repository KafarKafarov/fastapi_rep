import os
from uuid import uuid4
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session, selectinload
from fastapi.responses import FileResponse, JSONResponse
from typing import List
from database import SessionLocal, engine, Base
from models import Document, DocumentText
import schemas
from tasks import analyse_doc
import aiofiles
import shutil

UPLOAD_DIR = 'documents'
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/documents', response_model=schemas.Document,
          summary='Создание документа', tags=['Документы'])
def create_document(doc_in: schemas.DocumentCreate, db: Session = Depends(get_db)):
    db_doc = Document(path=doc_in.path)
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    db_texts = DocumentText(text=doc_in.text, document_id=db_doc.id)
    db.add(db_texts)
    db.commit()
    db.refresh(db_doc)

    return db_doc

@app.get('/documents/{doc_id}/', response_model=schemas.DocumentOut,
    summary='Получение документа по индексу', tags=['Документы'])
def get_doc(doc_id: int, db: Session = Depends(get_db)):
    doc = (
        db.query(Document)
          .options(selectinload(Document._text_obj))
          .filter(Document.id == doc_id)
          .first()
    )
    if not doc:
        raise HTTPException(status_code=404, detail='Документ не найден')
    return doc


@app.get('/documents', response_model=List[schemas.DocumentOut],
    summary='Список документов', tags=['Документы'])
def list_documents(db: Session = Depends(get_db)):
    docs = db.query(Document).all()
    result = []
    for d in docs:
        result.append({
            "id": d.id,
            "path": d.path,
            "date": d.date,
            "text": d.text or "Text not found"
        })
    return result




@app.post('/upload_doc', response_model=schemas.DocumentOut,
          summary='Загрузка документа в файл', tags=['Документы'])
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail='Разрешена загрузка только изображений')

    ext = os.path.splitext(file.filename)[1]
    unique_name = f'{uuid4().hex}{ext}'
    file_path = os.path.join(UPLOAD_DIR, unique_name)


    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)


    db_doc = Document(path=file_path)
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)

    return JSONResponse({
        "id": db_doc.id,
        "path": db_doc.path,
        "date": db_doc.date.isoformat() if db_doc.date else None,
        "text": db_doc.text or ""
    })


@app.get('/document/{doc_id}/file', summary='Скачать файл документа', tags=['Документы'])
def download_document(doc_id: int, db: Session = Depends(get_db)):
    db_doc = db.query(Document).filter(Document.id == doc_id).first()
    if not db_doc:
        raise HTTPException(status_code=404, detail='Файл не найден')
    return FileResponse(path=db_doc.path, filename=os.path.abspath(db_doc.path))


@app.delete('/documents/{doc_id}', summary='Удаление документа', tags=['Документы'])
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    db_doc = db.query(Document).filter(Document.id == doc_id).first()
    if not db_doc:
        raise HTTPException(status_code=404, detail='Документ не найден')
    try:
        os.remove(db_doc.path)
    except FileNotFoundError:
        pass
    except Exception as e:
        raise HTTPException(status_code=418, detail=f'Ошибка удаления файла: {e}')
    db.delete(db_doc)
    db.commit()
    return Response(status_code=204)


@app.post('/doc_analyse/{doc_id}', summary='Запустить анализ', tags=['Анализ'])
def doc_analyse(doc_id: int, db: Session = Depends(get_db)):
    db_doc = db.query(Document).get(doc_id)
    if not db_doc:
        raise HTTPException(status_code=404, detail='Документ не найден')
    analyse_doc.delay(db_doc.id, db_doc.path)
    return {'status': 200, 'msg': 'Анализ запущен'}

@app.get('/health_check', summary='Проверка работы', tags=['Сервис проверки'])
def health_check():
    return {"status": True, "service": "fastapi_ocr", "version": "1.0"}
