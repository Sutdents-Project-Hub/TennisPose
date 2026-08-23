# backend 元件

## 元件責任

- 類型：Python 原型／服務
- 專案：TennisPose：AI 網球獎盃姿勢教練
- 本元件只負責與其執行環境及部署生命週期一致的功能。

## 技術證據

- 技術：Streamlit
- Framework：Streamlit
- Package manager：pip
- Manifest／入口：尚無（scaffold 規劃階段）

## 本機開發

目前只建立元件邊界與文件，尚未執行 framework bootstrap、依賴安裝或啟動。請使用官方 initializer 建立骨架後再補上並驗證前置需求、安裝、啟動、port 與本機 URL。

## 品質與建置

- 目前沒有 manifest、quality script 或已驗證指令。`lint`、`typecheck`、`test`、`build` 是初始化規則要求日後納入的品質類別，不代表已存在或可執行。
- 實作後至少需建立角度公式與無法偵測姿勢的測試；只把實際執行成功的 lint、typecheck、test、build 指令寫入本文件。
- 詳細的實作順序、人工驗收與交付物見 [極限 MVP 實作與驗收計畫](../docs/mvp-plan.md)。

## 環境變數

以本元件的 `.env.example` 記錄名稱與安全 placeholder；不得提交真實值。

## 部署與限制

- 部署狀態：目前不部署
- 跨元件資料、API、權限或秘密邊界需在根 README 或 `docs/` 說明。
