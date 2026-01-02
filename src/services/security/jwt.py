import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, Any
from config import JWT_ACCESS_SECRET, JWT_REFRESH_SECRET

class JWTSecurity:
    def __init__(self):
        self.ACCESS_SECRET = JWT_ACCESS_SECRET
        self.REFRESH_SECRET = JWT_REFRESH_SECRET
        self.ALG = "HS256"
        self.ACCESS_TOKEN_EXP = 15 # minutes
        self.REFRESH_TOKEN_EXP = 7 # days


    def _create_token(
        self,
        expire: int,
        secret: str,
        type: str,
        data: dict = dict(),
        expires_delta: Optional[timedelta] = None
    ) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=expire))
        
        to_encode.update({
            "exp": expire, 
            "iat": datetime.now(timezone.utc),
            "type": type
        })
        return jwt.encode(to_encode, secret, algorithm=self.ALG)


    def _verify_token(self, secret: str, token: str) -> Optional[dict[str, Any]]:
        try:
            payload = jwt.decode(token, secret, algorithms=[self.ALG])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        
    
    def create_access_token(self, data: dict = dict()):
        return self._create_token(
            self.ACCESS_TOKEN_EXP, 
            self.ACCESS_SECRET, 
            "access", 
            data
        )
    

    def create_refresh_token(self, data: dict = dict()):
        return self._create_token(
            self.REFRESH_TOKEN_EXP, 
            self.REFRESH_SECRET, 
            "refresh",
            data,
            timedelta(days=self.REFRESH_TOKEN_EXP)
        )
    

    def verify_access_token(self, token: str):
        return self._verify_token(self.ACCESS_SECRET, token)
    

    def verify_refresh_token(self, token: str):
        data = self._verify_token(self.REFRESH_SECRET, token)
        if data and data.get("type") != "refresh":
            return None
        return data