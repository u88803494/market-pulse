import os
from fastapi import FastAPI
from dotenv import load_dotenv

# 在應用程式啟動時，從 .env 檔案載入環境變數
load_dotenv()

# --- 從環境變數中讀取您的金鑰 ---
# os.getenv() 會讀取您在 .env 中設定的變數
api_key = os.getenv("SHIOAJI_API_KEY")
secret_key = os.getenv("SHIOAJI_SECRET_KEY")
# --------------------------------

app = FastAPI()

@app.get("/")
async def read_root():
    # 為了測試，我們可以在根路徑回傳部分金鑰資訊 (注意：實際上線時不該這樣做)
    # 這裡只顯示 API Key 的前 4 個字元，以確認讀取成功
    return {
        "message": "Welcome to MarketPulse API",
        "api_key_loaded": f"{api_key[:4]}... (僅顯示前四碼供確認)",
        "secret_key_loaded": "Secret Key has been loaded." # Secret Key 通常完全不顯示
    }