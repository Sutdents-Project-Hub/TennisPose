# TennisPose：AI 網球獎盃姿勢教練

> 目前階段：競賽／展示｜部署：目前不部署

## 專案簡介

以單張側拍照片分析網球發球獎盃姿勢的手肘角度，提供可在競賽展示中清楚說明的紅綠燈回饋。


## 專案資訊

- Repository：`TennisPose`
- Project slug：`tennispose`
- 產品型態：`system`
- Bootstrap 模式：`scaffold`
- 技術政策：使用者未指定時採公司技術基線；已指定的學生選型以 Profile 為準。


## 命名對照

| 用途 | 名稱 |
|---|---|
| GitHub repository／本機根資料夾 | `TennisPose` |
| Project slug | `tennispose` |
| 本機 Docker Compose project | `tennispose` |


- 主要 Compose 檔若存在，頂層固定為 `name: tennispose`；service 使用責任角色，原則上不設定 `container_name`。



## 目標與主要功能

- 單張網球發球獎盃姿勢照片的本機上傳與預覽
- 以人體關鍵點計算肩膀、手肘、手腕三點夾角
- 依可配置目標區間顯示紅綠燈與可理解的姿勢回饋
- 正確與錯誤示例的可重現競賽 Demo 流程

- 只列入本階段已確認、可展示或可驗收的功能；構想與未來功能請明確標示為非本階段範圍。

本專案以「只做好一個動作」作為競賽 MVP 策略：讓沒有私人教練資源的新手，能從一張側拍照片理解手肘角度是否落在預先設定的示範區間。這是姿勢視覺化與練習輔助工具，不是醫療、受傷預防或動作品質的專業判定。

## 技術與元件

| 路徑 | 責任 | 技術 | 狀態 |
|---|---|---|---|
| `backend` | Python 原型／服務 | Streamlit | 已規劃；尚未建立 framework skeleton |

## 專案結構

- 新專案使用固定 component root；每個 component 本身就是 framework root，不再建立 project-name 或 framework-name wrapper。
- 目前只記錄已核准且實際需要的元件；不建立未使用的空資料夾。
- 每個獨立元件直接擁有自己的 manifest、lockfile、README、環境範例與框架慣例。

## 快速開始

目前只有核准的專案結構與文件，尚未建立 framework manifest、安裝依賴或服務。請依 Student Project Profile 使用官方 initializer 完成需要的元件後，再記錄並驗證前置需求、安裝、啟動、port 與本機 URL。

## 測試與品質

只記錄實際存在且已執行成功的 lint、typecheck、test、build 或手動驗收方式。若目前沒有自動化測試，請明確記錄主要人工驗收流程與限制。

## 環境變數與敏感資訊

- 真實值只存放於本機或部署平台，不提交 `.env`。
- 以 `.env.example` 記錄必要的變數名稱、用途與安全 placeholder；公開前端設定不可用來保存秘密。

## 部署狀態

目前狀態：目前不部署。只有在設定與流程實際驗證後，才補上平台、base directory、build/start command、port、healthcheck、資料與回滾方式。

## Git 與版本控制

- Repository 名稱：`TennisPose`
- 全新專案由初始化器建立本機 `main` branch，並在安全掃描後以 `chore(init): 初始化學生專案結構` 提交本次初始化產物。
- 既有 Git repository 保留原 branch 與歷史，不自動 commit。
- 初始化不設定 `user.name`／`user.email`，不建立 remote，也不 push；後續 Git 操作遵守 [AGENTS.md](AGENTS.md)。
- 後續操作先以 `git remote -v` 判斷本機或遠端模式；只要求 commit 時維持目前分支，獲准合併並驗證 `main` 後才安全關閉已完整合併的任務 branch。

## 文件索引

- [專案 Profile](docs/project-profile.md)
- [系統架構與元件邊界](docs/architecture.md)
- [專案範圍與驗收](docs/project-overview.md)
- [競賽與展示準備](docs/competition.md)
- [安全、身份與隱私](docs/security-and-privacy.md)
- [資料與儲存](docs/data-and-storage.md)
- [外部整合與 AI](docs/integrations.md)
- [極限 MVP 實作與驗收計畫](docs/mvp-plan.md)
- [backend 元件說明](backend/README.md)

## 維護與交接

- 開發規則與變更分類請見 [AGENTS.md](AGENTS.md)。
- 功能、架構、指令、環境變數、資料、測試、部署、競賽內容或限制改變時，在同一任務同步更新擁有該事實的 README／`docs/`／元件文件；文件同步是完成條件。
- 優先維護既有權威文件，不為了形式建立空文件；若沒有文件需要變更，完成回報需說明理由。
- LICENSE、資料集、模型與素材授權須依作者、學校及競賽規則確認，不由初始化工具自行決定。
