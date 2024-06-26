from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    fullname = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    username = Column(String(255), primary_key=True, index=True)
    role = Column(String(50), nullable=False, default="user")

class GeneratedWav(Base):
    __tablename__ = 'generated_wavs'
    
    wav_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), ForeignKey('users.username'), nullable=False)
    pdf_file_name = Column(String(255), nullable=False)
    wav_file_name = Column(String(255), nullable=False)
    wav_file_path = Column(String(255), nullable=False)
    generation_date = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="generated_wavs")

User.generated_wavs = relationship("GeneratedWav", order_by=GeneratedWav.wav_id, back_populates="user")
