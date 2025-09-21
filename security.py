from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt, JWTError
from config import settings
#Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password:str) -> str:
    return pwd_context.hash(password)
def verify_password(password: str, hashed: str)-> bool:
    return pwd_context.verify(password, hashed)
#Token URL 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
#JWT token creation and verification
def create_access_token(data: dict, expires_delta: timedelta | None=None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes= settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
def decode_token(token: str):
    try:
        payload = decode_token(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None