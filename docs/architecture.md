# 系統架構與元件邊界

## 架構原則

- Repository 預設為單一 Git repository，只有根目錄可擁有 `.git/`。
- `web/`、`app/`、`cms/`、`backend/`、`worker/` 等 component 本身就是 framework root；manifest 與 lockfile 直接位於該目錄。
- 不建立 project-name 或 framework-name wrapper。跨 component 共用程式碼只有在至少兩個真實使用者存在時才放入 `packages/`。
- 未指定技術時採公司基線：Node.js 24 LTS、TypeScript、pnpm、Next.js、React Native with Expo、Payload CMS、NestJS 與 PostgreSQL。
- 學生因競賽、既有 starter、硬體、授權或團隊能力採不同技術時，以核准 Profile 記錄的選型為準。
- 本機 Docker Compose project 固定為 `tennispose`。
- 主要 Compose 檔明確設定頂層 `name: tennispose`，service 使用責任角色且原則上不設定 `container_name`。



## 已核准元件

- `backend/`：Python 原型／服務；framework=`Streamlit`；package_manager=`pip`；technology_source=`specified`。

## 規劃中的單元流程

```text
使用者選擇一張本機圖片
  → Streamlit 於執行記憶體讀取圖片
  → MediaPipe Pose 偵測人體關鍵點
  → 取同一側的 shoulder、elbow、wrist 三點
  → 三點夾角公式計算肘關節角度
  → 以已設定的示範區間比較
  → 疊加骨架、連線、角度數值與紅／綠回饋後顯示
```

- 這是一個單一 Python 元件；不規劃獨立 API、資料庫、帳號或背景 worker。
- 初版只量測一側手臂。左右手判定、相機角度校正與多關節評分皆不是本階段範圍。
- 三點角度以向量 `shoulder - elbow` 與 `wrist - elbow` 的夾角計算。公式、座標系、例外輸入與門檻常數實作後須以單元測試或固定示例驗證。
- 目前提出的 90°–105° 僅為 Demo 候選區間，尚不可視為運動或醫療建議；最後門檻與引用來源必須在實作前確認。

## 失敗與降級原則

- 無檔案、格式不支援、影像模糊或無法偵測到完整關鍵點時，顯示原因與重新拍攝提示，不輸出偽造角度。
- 輸入影像不送往外部 API；若日後改用雲端模型或持久化儲存，屬於架構與隱私範圍變更，需先取得明確授權並同步文件。

## 結構例外

無；使用公司固定 component root。

## 跨元件與信任邊界

- UI 可見性不是授權；秘密、資料庫、重要外部 API 與高風險操作由可信任的 backend／platform 邊界持有。
- 新增 component、改變 framework／runtime／package manager、移動責任或建立新的外部服務前，先更新本文件與 Profile 並取得批准。

## 專案限制

- MVP 僅涵蓋網球發球獎盃姿勢（Trophy Pose），不分析完整揮拍流程。
- MVP 僅分析單張定格照片，不提供即時視訊追蹤、錄影串流或鏡頭同步。
- 介面預定以 Streamlit 實作，避免額外自訂前端框架與複雜互動。
- 目標是約 10 至 15 小時可展示的競賽原型；功能、依賴與測試需維持最小範圍。
- 角度門檻是競賽展示假設，未經教練或醫療專業驗證前不可宣稱可預防傷害或作醫療診斷。
