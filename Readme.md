# 項目分享表：具備 CI/CD 與容器化部屬的 RESTful API 專案

**簡介：** 這個全端應用是一個基於 **Python Flask** 與 **React** 的個人化學習清單系統。專案核心著重於**數據管理**、**嚴謹的 JWT 認證**，以及實踐 **Docker 容器化**與 **GitHub Actions CI/CD** 的自動化部署流程。


| Live Demo (已部署) | https://sharing-list-frontend.onrender.com |
| Swagger API 文件 (本地) | http://localhost:5000/swagger-ui (本地啟動後可見) |

---

## 總覽
- **後端框架：** Python, Flask, Flask-Smorest
- **資料庫：** PostgreSQL, SQLAlchemy, Flask-Migrate (Alembic)
- **DevOps：** Docker, Docker Compose, Gunicorn
- **品質與安全：** Pytest (單元測試), GitHub Actions (CI/CD), JWT 認證, Passlib

---

## 後端核心工程實踐

### 1. API 設計與認證
- **RESTful API 實作：** 使用 Python Flask 框架搭配 Flask-Smorest，設計 Learn, Tag, User 等資源的 CRUD 端點。
- **使用者認證：** 導入 **JWT (JSON Web Token)** 實現用戶登入與狀態管理。
- **安全機制：** 密碼使用 **Passlib 進行 pbkdf2_sha256 雜湊** 儲存；實作 **Token Blacklist** 實現登出後 Token 立即失效。
- **權限控制：** 設計 **Admin (管理員) 和 Guest (訪客)** 模式，訪客帳號僅允許瀏覽，無法進行增刪改 (CRUD) 操作。

### 2. 資料處理與持久化 (Database & ORM)
- **資料庫選型：** 採用穩定的 **PostgreSQL** 資料庫，搭配 SQLAlchemy ORM 進行物件關係映射。
- **複雜關聯處理：** 實作 **Learn (項目) 與 Tag (標籤) 的多對多關聯 (Many-to-Many Relationship)**。
- **資料庫版本控制：** 導入 **Flask-Migrate (基於 Alembic)** 進行資料庫綱要遷移，確保版本更新的一致性和可靠性。

---

## ☁️ 容器化與 CI/CD 自動化實踐 (DevOps)

### 1. 服務容器化 (Docker & Docker Compose)
- **多容器架構：** 使用 **Docker Compose** 統一管理三個服務（`db`, `backend`, `frontend`），確保開發環境的一致性。
- **自動化啟動腳本：** 後端容器（`backend`）執行 `docker-entrypoint.sh`，自動執行 **`flask db upgrade`**（資料庫更新）並啟動 **Gunicorn** 服務。

### 2. 持續整合 (CI/CD)
- **自動化測試：** 設置 **GitHub Actions**，在每次 `push` 到 `main` 時自動觸發 CI 流程。
- **測試框架：** 使用 **Pytest** 框架 針對 API 服務（登入、註冊、CRUD 邏輯）進行功能測試，只有通過測試的程式碼才能進入部署階段。

---

### A. 本地快速啟動 (Local Quick Start)

1.  **環境需求：** 確認已安裝 Git, Docker 和 Make。
2.  **環境配置：** 複製 `Backend/.env.example` 為 `Backend/.env`，並建議使用預設配置。
3.  **一鍵啟動：** 在專案根目錄執行 `make build`。
4.  **運行測試：** 執行 `make test` 驗證所有功能。
5.  **訪問頁面：** 前往 `http://localhost:5173`。

### B. CI/CD 與雲端部署說明 (Deployment Notes)

#### 1. GitHub Actions (CI/CD) 說明
- **觸發條件：** 預設 `push` 到 `main` 分支時自動觸發。
- **配置要點：** 需於 GitHub Actions Secrets 中增加相關環境變數 (詳見 `workflows/main.yml` 與 `Backend/.env.example`)。

#### 2. Render 雲端部署流程
- **步驟 1: 資料庫 (db)**：選擇 PostgreSQL 服務，取得 **Internal Database URL**。
- **步驟 2: 後端 (Backend)**：
    - 選擇 Web Service，指定後端 Git Repo，環境語言為 Docker。
    - 環境變數需使用 Render 的 Internal Database URL 更新 `DATABASE_URL`。
- **步驟 3: 前端 (Frontend)**：
    - 選擇 Static Site，指定前端 Git Repo。
    - Build Command 填寫：`npm install && npm run build`。
    - 環境變數需新增 `VITE_API_URL`，值為 Backend 的實際網址。