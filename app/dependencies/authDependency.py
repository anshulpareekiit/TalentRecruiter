from fastapi import Header, HTTPException, status, Depends
from typing import Optional
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database.mysqlConnection import Dbsession, get_db #db mysql connection created
from app.entities.userSessionToken import UserSessionToken

security = HTTPBearer()

def checkUserAuthorization(db:Dbsession,credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    # Your token validation logic
    if not credentials.scheme.startswith("Bearer"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format"
        )
    # strip Bearer if needed    
    session_token = db.query(UserSessionToken).filter_by(token=token).first()
    print(session_token.token_expiry)
    if not session_token or session_token.token_expiry < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid or expired"
        )

    session_token.token_expiry = datetime.now() + timedelta(minutes=10)
    db.commit()

    return session_token.users
