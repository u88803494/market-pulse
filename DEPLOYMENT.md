# MarketPulse API 部署指南 🚀

## 🧪 MVP 測試模式 (目前狀態)

### 快速啟動
```bash
# 1. 啟動虛擬環境
source venv/bin/activate

# 2. 啟動服務器
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 測試端點
```bash
# 基本健康檢查
curl http://localhost:8000/health

# 股票報價 (Mock 數據)
curl "http://localhost:8000/api/v1/stocks/quotes?symbol=2330"
curl "http://localhost:8000/api/v1/stocks/quotes?symbol=2317"

# API 文件
open http://localhost:8000/docs
```

## 📊 API 端點總覽

| 端點 | 方法 | 描述 | 範例 |
|------|------|------|------|
| `/` | GET | 歡迎頁面 | `curl http://localhost:8000/` |
| `/health` | GET | 健康檢查 | `curl http://localhost:8000/health` |
| `/api/v1/stocks/quotes` | GET | 股票報價 | `curl "http://localhost:8000/api/v1/stocks/quotes?symbol=2330"` |
| `/api/v1/stocks/health` | GET | 股票服務健康檢查 | `curl http://localhost:8000/api/v1/stocks/health` |
| `/docs` | GET | Swagger UI | 瀏覽器開啟 |
| `/redoc` | GET | ReDoc | 瀏覽器開啟 |

## 🔧 切換到真實 Shioaji API

### 1. 安裝 Shioaji SDK
```bash
pip install shioaji==1.2.6
```

### 2. 修改 main.py
```python
# 將這行：
from services.mock_shioaji_service import mock_shioaji_service as shioaji_service

# 改為：
from services.shioaji_service import shioaji_service
```

### 3. 修改 routers/stock_routes.py
```python
# 將這行：
from services.mock_shioaji_service import MockShioajiService as ShioajiService, get_mock_shioaji_service as get_shioaji_service

# 改為：
from services.shioaji_service import ShioajiService, get_shioaji_service
```

### 4. 設定環境變數
```bash
# 建立 .env 檔案
touch .env

# 編輯 .env 檔案，加入：
SHIOAJI_API_KEY=your_api_key_here
SHIOAJI_SECRET_KEY=your_secret_key_here
```

## 🌐 部署到 Render (生產環境)

### 1. 準備部署檔案
建立 `render.yaml`:
```yaml
services:
  - type: web
    name: market-pulse-api
    env: python
    region: singapore
    plan: free
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: SHIOAJI_API_KEY
        sync: false
      - key: SHIOAJI_SECRET_KEY
        sync: false
      - key: API_KEY
        sync: false
```

### 2. 環境變數設定
在 Render 儀表板中設定：
- `SHIOAJI_API_KEY`: 您的永豐 API Key
- `SHIOAJI_SECRET_KEY`: 您的永豐 Secret Key
- `API_KEY`: 用於 API 認證的金鑰 (可選)

### 3. 部署步驟
1. 將程式碼推送到 GitHub
2. 連結 Render 到您的 GitHub 儲存庫
3. 設定環境變數
4. 部署

### 4. 測試部署
```bash
# 替換為您的 Render URL
curl https://your-app-name.onrender.com/health
curl "https://your-app-name.onrender.com/api/v1/stocks/quotes?symbol=2330"
```

## 🔒 API 認證使用

### 設定 API Key
```bash
# 在 .env 檔案中加入
API_KEY=your_secret_api_key_here
```

### 使用 API Key
```bash
# 使用 Bearer Token
curl -H "Authorization: Bearer your_secret_api_key_here" \
     http://localhost:8000/protected
```

## 📝 下一步建議

1. **前端開發**: 建立 Next.js 前端來呈現股票資訊
2. **資料庫**: 加入 PostgreSQL 或 Redis 進行快取
3. **監控**: 加入 Sentry 或 DataDog 進行錯誤追蹤
4. **測試**: 加入 pytest 進行單元測試
5. **CI/CD**: 設定 GitHub Actions 自動部署

## 🎯 MVP 完成清單

- ✅ FastAPI 基礎架構
- ✅ Pydantic 資料驗證
- ✅ 股票報價 API 端點
- ✅ Mock 資料服務 (測試用)
- ✅ Shioaji SDK 整合 (準備就緒)
- ✅ API Key 認證機制
- ✅ 自動 API 文件
- ✅ 健康檢查端點
- ✅ 部署準備 (Render)

**恭喜！您的 MarketPulse API MVP 已經準備就緒！** 🎉 