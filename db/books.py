from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from backend.const import USERS_DB
from .models import Book, TtsModel
from io import BytesIO  
import os
import logging


load_dotenv()
Base = declarative_base()

engine = create_engine(USERS_DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_file(file_obj: BytesIO, file_path: str) -> bool:
    """
    Save the file to the media assets.

    Parameters:
    file_obj (BytesIO): The file object to be saved.
    """

    if os.path.exists(file_path):
        print(f"File already exists. Skipping save.")
        return False

    try:
        with open(f"{file_path}", 'wb') as f:
            f.write(file_obj.getbuffer())
        print(f"File saved successfully to {file_path}")
        return True
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")
        return False
    

def create_book(db: Session, path: str, metadata: dict) -> Book:
    logger.info(f'Creating a new book with path: {path} and metadata: {metadata}')
    new_book = Book(path=path, metadata_=metadata, page_idx=0)
    
    # Create the associated TtsModel with standard values
    new_tts_model = TtsModel(
        model_name="standard",
        model_keys={},
        path=path
    )

    try:
        db.add(new_book)
        db.add(new_tts_model)
        db.commit()
        db.refresh(new_book)
        logger.info(f'Book created with path: {new_book.path}')
        return new_book
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f'Failed to create book with path: {path}. Error: {e}')
        return None

def get_all_books(db: Session, username: str) -> list[Book]:
    books = db.query(Book).filter(Book.path.like(f"%{username}%")).all()
    return books if books else []


def get_book(db: Session, username: str) -> Book:
    return db.query(Book).filter(Book.path.like(f"%{username}%")).first()

def delete_book(db: Session, path: str) -> bool:
    book = db.query(Book).filter(Book.path == path).first()
    if book:
        db.delete(book)
        db.commit()
        return True
    else:
        return False

def get_book_image_path(db: Session, book_path: str) -> str:
    book = db.query(Book).filter(Book.path == book_path).first()
    if book:
        return book.metadata_['img_path']
    else:
        raise HTTPException(status_code=404, detail="Book not found")


def update_book_img_path(db: Session, book_path: str, img_path: str) -> None:
    book = db.query(Book).filter(Book.path == book_path).first()
    if book:
        # Initialize metadata if it doesn't exist
        if not book.metadata_:
            book.metadata_ = {}
        if 'img_path' not in book.metadata_:
            book.metadata_['img_path'] = ''
        
        book.metadata_['img_path'] = img_path
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Book not found")
