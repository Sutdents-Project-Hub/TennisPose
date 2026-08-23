# 學生專案 Profile

## 基本資訊

- Project name：TennisPose：AI 網球獎盃姿勢教練
- Repository name：`TennisPose`
- Project slug：`tennispose`
- Local Docker Compose project：`tennispose`
- Stage：`competition`
- Product type：`system`
- Bootstrap mode：`scaffold`
- Deployment：`none`
- Team collaboration：`true`
- Technology policy：未指定時採公司技術基線
- Structure exception：無；使用固定 component root

## 摘要

以單張側拍照片分析網球發球獎盃姿勢的手肘角度，提供可在競賽展示中清楚說明的紅綠燈回饋。

## 元件

- `pose-analysis`：path=`backend`，kind=`python`，framework=`Streamlit`，package_manager=`pip`，quality=lint, typecheck, test, build，technology_source=`specified`

## 功能領域

- 單張網球發球獎盃姿勢照片的本機上傳與預覽
- 以人體關鍵點計算肩膀、手肘、手腕三點夾角
- 依可配置目標區間顯示紅綠燈與可理解的姿勢回饋
- 正確與錯誤示例的可重現競賽 Demo 流程

## 專案限制

- MVP 僅涵蓋網球發球獎盃姿勢（Trophy Pose），不分析完整揮拍流程。
- MVP 僅分析單張定格照片，不提供即時視訊追蹤、錄影串流或鏡頭同步。
- 介面預定以 Streamlit 實作，避免額外自訂前端框架與複雜互動。
- 目標是約 10 至 15 小時可展示的競賽原型；功能、依賴與測試需維持最小範圍。
- 角度門檻是競賽展示假設，未經教練或醫療專業驗證前不可宣稱可預防傷害或作醫療診斷。

## 關注事項

- ai
- uploads
- personal-data

## 假設

- 初版在使用者本機執行，影像只用於當次分析且不建立帳號、雲端儲存或資料庫。
- Demo 影像由團隊自行拍攝或使用已獲公開與競賽使用授權的素材。
- 姿勢關鍵點將由 MediaPipe Pose 等本機套件提供；實作前需確認版本相容性、授權與歸屬要求。
- 使用者已明確授權在 main 建立初始化 commit、設定指定 origin 並推送；這不包含部署或建立外部服務。

## 未決定事項

- 正式競賽名稱、2026 年報名規則、影片長度與送件截止日尚未核實。
- 角度區間、拍攝視角與左右手姿勢的判斷規則需由網球教練或可信來源確認後才可作為評分標準。
- 影像保存期限、隱私告知方式與日後公開部署需求尚未決定。
- 專案授權條款、第三方模型與素材的最終歸屬清單尚未決定。
