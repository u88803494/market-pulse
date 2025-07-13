# MarketPulse API 📈

一個現代、高效能的後端 API 服務，旨在提供即時與歷史的台灣股市數據。此專案使用 FastAPI 框架，並串接永豐金證券 Shioaji SDK 作為主要的數據來源。

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.11x-green.svg)
![Code Style](https://img.shields.io/badge/code%20style-PEP8-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ 主要特色 (Features)

- **即時報價**: 提供指定股票的即時五檔報價、成交價與漲跌幅。
- **歷史 K 線**: 取得日、週、月、分鐘層級的歷史 K 線數據。
- **非同步架構**: 基於 FastAPI 與 `asyncio`，所有 I/O 操作均為非同步，確保高效能。
- **資料驗證**: 使用 Pydantic V2 進行嚴格的請求與回應資料驗證，確保 API 的穩定性。
- **自動化文件**: 內建 Swagger UI 與 ReDoc，提供互動式的 API 文件。

## 🛠️ 技術棧 (Tech Stack)

- **Backend**: FastAPI, Uvicorn
- **Data Validation**: Pydantic
- **Data Source**: 永豐金證券 Shioaji Python SDK
- **Development**: Python 3.11+

## 🚀 如何開始 (Getting Started)

請依照以下步驟在本機環境中設定並啟動此專案。

### 1. 前置需求

- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)

### 2. 安裝流程

1.  **Clone 儲存庫**
    ```bash
    git clone git@github.com:u88803494/market-pulse.git
    cd market-pulse
    ```

2.  **建立並啟用虛擬環境**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **安裝依賴套件**
    ```bash
    pip install -r requirements.txt
    ```

4.  **設定環境變數**
    本專案使用 `.env` 檔案來管理環境變數。請建立 `.env` 檔案並填入您的金鑰。
    ```bash
    touch .env
    ```
    接著，請編輯 `.env` 檔案，填上您的 Shioaji API Key 和 Secret Key：
    ```
    SHIOAJI_API_KEY=your_api_key_here
    SHIOAJI_SECRET_KEY=your_secret_key_here
    ```

5.  **啟動本地伺服器**
    ```bash
    uvicorn main:app --reload
    ```

### 3. 存取 API

伺服器啟動後，您可以透過以下路徑存取服務：

- **API 服務**: `http://127.0.0.1:8000`
- **Swagger UI (互動式文件)**: `http://127.0.0.1:8000/docs`
- **ReDoc (替代文件)**: `http://127.0.0.1:8000/redoc`

### 4. 快速測試

```bash
# 測試基本功能
curl http://localhost:8000/health

# 測試股票報價 (Mock 資料)
curl "http://localhost:8000/api/v1/stocks/quotes?symbol=2330"

# 開啟 API 文件
open http://localhost:8000/docs
```

> **注意**: 目前使用 Mock 資料進行測試。要使用真實的 Shioaji API，請參閱 [DEPLOYMENT.md](DEPLOYMENT.md) 中的設定指南。

## ⚙️ 環境變數 (Environment Variables)

本專案需要以下環境變數才能正常運作：

| 變數名稱             | 說明                 |
| -------------------- | -------------------- |
| `SHIOAJI_API_KEY`    | 您的永豐 Shioaji API Key |
| `SHIOAJI_SECRET_KEY` | 您的永豐 Shioaji Secret Key |

## 📁 專案結構 (Project Structure)
```
market-pulse/
├── .gitignore          # Git 忽略檔案設定
├── .cursorrules        # Cursor IDE 規則設定
├── README.md           # 專案說明文件
├── DEPLOYMENT.md       # 部署指南
├── main.py             # FastAPI 應用程式入口點
├── requirements.txt    # Python 依賴套件
├── models/             # Pydantic 資料模型
│   ├── __init__.py
│   └── stock_models.py
├── routers/            # API 路由
│   ├── __init__.py
│   └── stock_routes.py
├── services/           # 業務邏輯服務
│   ├── __init__.py
│   ├── shioaji_service.py      # 真實 Shioaji API 服務
│   └── mock_shioaji_service.py # Mock 測試服務
├── utils/              # 工具函式
│   ├── __init__.py
│   └── auth.py         # API 認證
├── venv/               # Python 虛擬環境
└── .env                # 環境變數檔案 (需自行建立)
```


## 📄 授權 (License)

本專案採用 [MIT License](LICENSE) 授權。
