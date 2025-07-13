from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated
from models.stock_models import QuoteResponse, ErrorResponse
from services.mock_shioaji_service import MockShioajiService as ShioajiService, get_mock_shioaji_service as get_shioaji_service

# 建立股票路由器
router = APIRouter(
    prefix="/api/v1/stocks",
    tags=["stocks"],
    responses={404: {"model": ErrorResponse}}
)


@router.get("/quotes", response_model=QuoteResponse)
async def get_stock_quote(
    symbol: Annotated[str, Query(description="股票代碼 (例如: 2330)")],
    shioaji_service: ShioajiService = Depends(get_shioaji_service)
) -> QuoteResponse:
    """
    取得指定股票的即時報價
    
    Args:
        symbol: 股票代碼 (例如: 2330)
        shioaji_service: Shioaji 服務實例
    
    Returns:
        QuoteResponse: 股票報價資料
    
    Raises:
        HTTPException: 當股票代碼不存在或其他錯誤時
    """
    # 防禦性程式設計：檢查參數
    if not symbol:
        raise HTTPException(status_code=400, detail="Symbol is required")
    
    if not symbol.isalnum():
        raise HTTPException(status_code=400, detail="Invalid symbol format")
    
    try:
        # 取得股票報價
        quote = await shioaji_service.get_quote(symbol)
        return quote
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/health")
async def health_check():
    """
    健康狀態檢查端點
    
    Returns:
        dict: 服務狀態資訊
    """
    return {"status": "healthy", "service": "MarketPulse Stock API"} 