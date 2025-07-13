import os
import asyncio
from typing import Optional
from datetime import datetime
import shioaji as sj
from models.stock_models import QuoteResponse, ErrorResponse
from contextlib import asynccontextmanager


class ShioajiService:
    """Shioaji API 服務類別"""
    
    def __init__(self):
        self.api: Optional[sj.Shioaji] = None
        self.is_logged_in = False
        
    async def initialize(self) -> bool:
        """初始化 Shioaji API"""
        try:
            # 從環境變數取得 API 金鑰
            api_key = os.getenv("SHIOAJI_API_KEY")
            secret_key = os.getenv("SHIOAJI_SECRET_KEY")
            
            if not api_key or not secret_key:
                raise ValueError("Missing SHIOAJI_API_KEY or SHIOAJI_SECRET_KEY environment variables")
            
            # 建立 Shioaji API 實例
            self.api = sj.Shioaji()
            
            # 登入
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.api.login(api_key, secret_key)
            )
            
            self.is_logged_in = True
            return True
            
        except Exception as e:
            print(f"Shioaji initialization failed: {e}")
            return False
    
    async def get_quote(self, symbol: str) -> QuoteResponse:
        """取得股票報價"""
        # 防禦性程式設計：檢查前置條件
        if not self.api:
            raise ValueError("Shioaji API not initialized")
        
        if not self.is_logged_in:
            raise ValueError("Shioaji API not logged in")
        
        if not symbol:
            raise ValueError("Symbol cannot be empty")
        
        try:
            # 取得股票合約
            contract = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.api.Contracts.Stocks.get(symbol)
            )
            
            if not contract:
                raise ValueError(f"Stock symbol {symbol} not found")
            
            # 取得快照報價
            snapshot = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.api.snapshots([contract])
            )
            
            if not snapshot or len(snapshot) == 0:
                raise ValueError(f"No quote data available for {symbol}")
            
            quote_data = snapshot[0]
            
            # 計算漲跌幅
            change = quote_data.get('close', 0) - quote_data.get('reference', 0)
            change_percent = (change / quote_data.get('reference', 1)) * 100 if quote_data.get('reference', 0) > 0 else 0
            
            # 建立回應模型
            return QuoteResponse(
                symbol=symbol,
                name=getattr(contract, 'name', symbol),
                price=float(quote_data.get('close', 0)),
                change=float(change),
                change_percent=float(change_percent),
                volume=int(quote_data.get('volume', 0)),
                timestamp=datetime.now()
            )
            
        except Exception as e:
            raise ValueError(f"Failed to get quote for {symbol}: {str(e)}")
    
    async def close(self):
        """關閉 Shioaji API 連接"""
        if self.api and self.is_logged_in:
            try:
                await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: self.api.logout()
                )
            except Exception as e:
                print(f"Error during logout: {e}")
            finally:
                self.is_logged_in = False
                self.api = None


# 全域服務實例
shioaji_service = ShioajiService()


async def get_shioaji_service() -> ShioajiService:
    """取得 Shioaji 服務實例 (依賴注入)"""
    return shioaji_service 