from datetime import datetime, timedelta, timezone
#Import JSON Web Token
from jose import jwt
from passlib.context import CryptContext
from app.config import SECRET_KEY
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials



ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
security = HTTPBearer()



# Creating  password manager
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# Hashing  password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verifying  password
def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)

# Creating the access token
def create_access_token(user_id: int) -> str:
    # Calculate when the token expires
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expire,
    }
    #  create the JWT
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(
    credentials: HTTPAuthorizationCredentials,
) -> int:
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

# get user id
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return int(user_id)

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
