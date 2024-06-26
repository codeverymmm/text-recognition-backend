import os
from fastapi import HTTPException, status
SECRET_KEY = os.getenv('SECRET_KEY')
USERS_DB = os.getenv('DATABASE_URL')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
CREDENTIALS_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )