# OOP 設計說明

本專案採用物件導向設計（OOP），強調「單一職責」、「繼承」、「多型」及「模組化」原則，便於維護與擴充。

## 架構總覽

- **遊戲管理模組 (`game/`)**
  - `GameManager`：整體遊戲流程與狀態管理
  - `MapManager`：地圖、建塔格子管理
  - `WaveManager`：波數、出怪時序管理

- **實體模組 (`entities/`)**
  - `BaseEntity`：所有遊戲物件共用屬性/方法
  - `towers/`：各類塔的基底與子類
  - `enemies/`：各類敵人的基底與子類
  - `projectiles/`：各類投射物（砲彈、子彈、冰球）

- **UI 模組 (`ui/`)**
  - `GameUI`：遊戲進行中資訊顯示、操作
  - `Menu`：主選單與結束畫面

- **工具模組 (`utils/`)**
  - `constants.py`：全域常數
  - `helpers.py`：輔助函數
  - `animation.py`：動畫處理

## 類別關係圖

```
GameManager ─┬─> MapManager
             ├─> WaveManager
             ├─> GameUI
             └─> Entity 管理（Towers/Enemies/Projectiles）
Towers/Enemies/Projectiles 均繼承自 BaseEntity
```

## 設計說明

- **繼承**：所有塔、敵人、投射物皆有基底類別，可方便擴充新種類。
- **多型**：不同塔、敵人可覆寫攻擊/移動/特效方法。
- **組合**：管理器協作，UI 與邏輯分離。
- **模組化**：每個功能獨立，易於維護與測試。

## 擴充建議

- 新增塔/敵人，只需繼承對應基底類別並實作差異。
- 可獨立開發新 UI 或特殊地圖。

## 類別圖示意

（請參考 `docs/images/oop_class_diagram.png`，或自行用 UML 工具繪製）

