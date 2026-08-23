# 外部整合與 AI

## 適用原因

本專案 concerns：ai, uploads, personal-data。

## 必須確認

- API、模型或服務的官方來源、授權、成本、rate limit、timeout、錯誤與替代流程。
- Key 與敏感請求由可信任環境管理；不得將 production secret 放入 App 或公開 Web。
- AI 功能需記錄模型用途、輸入資料、限制、錯誤可能性、人工覆核與競賽揭露方式。
- 外部服務失效、回傳不完整或不可用時，demo 與主要流程應有可理解的降級行為。

## MVP 技術計畫

- 預定使用 `MediaPipe Pose` 做本機人體關鍵點推論，使用 `OpenCV` 做影像讀取／繪製，以及 `NumPy` 做幾何運算；實際套件版本、Python 相容性與授權尚未驗證。
- 此版本不規劃呼叫雲端 AI、LLM、教練資料庫或第三方 API，因此不應設定 API key，也不需要 `.env`。
- 實作完成後需記錄每個實際依賴的來源、版本範圍、授權和可重現安裝方式；若競賽規則要求，將模型／套件 attribution 放入 README 或提交資料。
