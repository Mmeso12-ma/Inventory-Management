from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt, JWTError
from config import settings
from database import get_db
from sqlalchemy.orm import Session
from models import User
from config import settings
#Password hashing
pwd_context = CryptContext(schemes=["argon2", "bcrypt_sha256", "bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    try:
        # CryptContext will pick the first available scheme (argon2 if installed)
        return pwd_context.hash(password)
    except ValueError as e:
        # clear actionable error for runtime failures (bcrypt backend missing/old)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "Password hashing failed (bcrypt backend missing or incompatible). "
                "Run: pip install --upgrade bcrypt passlib argon2-cffi and restart the app."
            ),
        )

def verify_password(password: str, hashed: str) -> bool:
    try:
        return pwd_context.verify(password, hashed)
    except ValueError as e:
        msg = str(e)
        if "longer than 72" in msg or "72 bytes" in msg:
            truncated = password[:72]
            try:
                return pwd_context.verify(truncated, hashed)
            except Exception:
                return False
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "Password verification failed (bcrypt backend missing or incompatible). "
                "Run: pip install --upgrade bcrypt passlib argon2-cffi and restart the app."
            ),
        )

#Token URL 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
#JWT token creation and verification
def create_access_token(data: dict, expires_delta: timedelta | None=None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes= settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
def decode_token(token, secret_key, algorithm):
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
#get current logged in user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_token(token, settings.SECRET_KEY, settings.ALGORITHM)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    username: str | None = payload.get("sub")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
# role checker 
def require_role(required_roles: list[str]):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in required_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Permission Denied.")
        return current_user
    return role_checker