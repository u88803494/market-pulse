from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class QuoteRequest(BaseModel):
    """股票報價請求模型"""
    symbol: str = Field(..., description="股票代碼 (例如: 2330.TW)")
    

class QuoteResponse(BaseModel):
    """股票報價回應模型"""
    symbol: str = Field(..., description="股票代碼")
    name: str = Field(..., description="股票名稱")
    price: float = Field(..., description="當前股價")
    change: float = Field(..., description="漲跌金額")
    change_percent: float = Field(..., description="漲跌幅(%)")
    volume: int = Field(..., description="成交量")
    timestamp: datetime = Field(..., description="報價時間")
    
    class Config:
        # 允許 JSON 序列化
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ErrorResponse(BaseModel):
    """錯誤回應模型"""
    error: str = Field(..., description="錯誤訊息")
    details: Optional[str] = Field(None, description="詳細錯誤資訊")


class APIKeyRequest(BaseModel):
    """API Key 驗證請求模型"""
    api_key: str = Field(..., description="API 金鑰") 