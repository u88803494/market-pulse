import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routers.stock_routes import router as stock_router
from services.mock_shioaji_service import mock_shioaji_service as shioaji_service
from utils.auth import verify_api_key, optional_verify_api_key

# 在應用程式啟動時，從 .env 檔案載入環境變數
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    應用程式生命週期管理
    處理 Shioaji API 的初始化和清理
    """
    # 啟動時的初始化
    print("🚀 MarketPulse API 正在啟動...")
    
    # 初始化 Shioaji API
    success = await shioaji_service.initialize()
    if success:
        print("✅ Shioaji API 初始化成功")
    else:
        print("❌ Shioaji API 初始化失敗")
    
    yield
    
    # 關閉時的清理
    print("🔄 MarketPulse API 正在關閉...")
    await shioaji_service.close()
    print("✅ 資源清理完成")


# 建立 FastAPI 應用程式
app = FastAPI(
    title="MarketPulse API",
    description="一個現代、高效能的後端 API 服務，旨在提供即時與歷史的台灣股市數據",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# 設定 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生產環境中應該設定具體的來源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 註冊路由
app.include_router(stock_router)


@app.get("/")
async def read_root():
    """
    根路徑端點
    
    Returns:
        dict: 歡迎訊息和 API 資訊
    """
    return {
        "message": "Welcome to MarketPulse API 📈",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """
    健康狀態檢查端點
    
    Returns:
        dict: 服務狀態資訊
    """
    return {
        "status": "healthy",
        "service": "MarketPulse API",
        "shioaji_connected": shioaji_service.is_logged_in
    }


# 受保護的測試端點 (需要 API Key)
@app.get("/protected")
async def protected_route(api_key: str = Depends(verify_api_key)):
    """
    受保護的測試端點
    
    Args:
        api_key: 驗證通過的 API Key
    
    Returns:
        dict: 受保護的資訊
    """
    return {
        "message": "You have access to protected content!",
        "api_key": f"{api_key[:4]}..." if len(api_key) > 4 else api_key
    }