import asyncio
from typing import Optional
from datetime import datetime
from models.stock_models import QuoteResponse
import random


class MockShioajiService:
    """Mock Shioaji API 服務類別 (用於測試)"""
    
    def __init__(self):
        self.is_logged_in = False
        
    async def initialize(self) -> bool:
        """初始化 Mock Shioaji API"""
        print("🔧 使用 Mock Shioaji 服務 (測試模式)")
        await asyncio.sleep(0.1)  # 模擬初始化延遲
        self.is_logged_in = True
        return True
    
    async def get_quote(self, symbol: str) -> QuoteResponse:
        """取得模擬股票報價"""
        # 防禦性程式設計：檢查前置條件
        if not self.is_logged_in:
            raise ValueError("Mock Shioaji API not logged in")
        
        if not symbol:
            raise ValueError("Symbol cannot be empty")
        
        # 模擬 API 延遲
        await asyncio.sleep(0.1)
        
        # 生成模擬數據
        base_price = 100.0
        if symbol == "2330":
            base_price = 500.0
        elif symbol == "2317":
            base_price = 30.0
        elif symbol == "2454":
            base_price = 45.0
        
        # 隨機生成變化
        change = random.uniform(-10.0, 10.0)
        price = base_price + change
        change_percent = (change / base_price) * 100
        volume = random.randint(1000, 100000)
        
        return QuoteResponse(
            symbol=symbol,
            name=f"Mock Company {symbol}",
            price=round(price, 2),
            change=round(change, 2),
            change_percent=round(change_percent, 2),
            volume=volume,
            timestamp=datetime.now()
        )
    
    async def close(self):
        """關閉 Mock Shioaji API 連接"""
        print("🔧 Mock Shioaji 服務關閉")
        self.is_logged_in = False


# 全域 mock 服務實例
mock_shioaji_service = MockShioajiService()


async def get_mock_shioaji_service() -> MockShioajiService:
    """取得 Mock Shioaji 服務實例 (依賴注入)"""
    return mock_shioaji_service 