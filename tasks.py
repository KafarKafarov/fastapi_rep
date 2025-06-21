import pytesseract
from PIL import Image
from database import SessionLocal
from models import DocumentText
from celery_worker import celery_app


@celery_app.task(name='tasks.analyse_doc')
def analyse_doc(doc_id: int, path: str):
    db = SessionLocal()
    try:
        text = pytesseract.image_to_string(Image.open(path))
        db_text = DocumentText(text=text, document_id=doc_id)
        db.add(db_text)
        db.commit()
    except Exception as e:
        print(f'Ошибка: {e}')
    finally:
        db.close()
