import os
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional


# 建立 HTTP Bearer 認證
security = HTTPBearer()


def get_api_key_from_env() -> Optional[str]:
    """從環境變數取得 API Key"""
    return os.getenv("API_KEY")


async def verify_api_key(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> str:
    """
    驗證 API Key
    
    Args:
        credentials: HTTP Bearer Token 憑證
    
    Returns:
        str: 驗證通過的 API Key
    
    Raises:
        HTTPException: 當 API Key 無效時
    """
    # 取得環境變數中的 API Key
    valid_api_key = get_api_key_from_env()
    
    # 如果沒有設定 API Key，則跳過驗證 (開發模式)
    if not valid_api_key:
        return "development"
    
    # 檢查 Bearer Token 是否存在
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key is required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 驗證 API Key
    if credentials.credentials != valid_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return credentials.credentials


# 可選的 API Key 驗證 (用於開發時的便利性)
async def optional_verify_api_key(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(HTTPBearer(auto_error=False))
) -> Optional[str]:
    """
    可選的 API Key 驗證 (不會在未提供時拋出錯誤)
    
    Args:
        credentials: HTTP Bearer Token 憑證
    
    Returns:
        Optional[str]: 驗證通過的 API Key 或 None
    """
    if not credentials:
        return None
    
    try:
        return await verify_api_key(credentials)
    except HTTPException:
        return None 