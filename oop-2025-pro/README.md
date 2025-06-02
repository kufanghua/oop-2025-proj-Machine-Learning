# oop-2025-proj-Tower Defense Games
# 🏰 Tower Defense Game - OOP Final Project

> A comprehensive tower defense game demonstrating Object-Oriented Programming principles
> 
> **Course**: Object-Oriented Programming  
> **University**: National Yang Ming Chiao Tung University  
> **Semester**: 2024 Fall  
> **Group**: X

## 🎮 Game Overview

An engaging tower defense game where players strategically place towers to defend against waves of enemies. Built using Python and Pygame with strong emphasis on OOP design patterns.

### ✨ Features
- **Multiple Tower Types**: Cannon, Machine Gun, Freeze towers
- **Diverse Enemies**: Basic, Fast, Tank enemies with unique abilities  
- **Progressive Difficulty**: Wave-based gameplay with increasing challenge
- **Economic System**: Resource management and strategic planning
- **Visual Effects**: Smooth animations and particle effects

## 🎯 OOP Concepts Demonstrated

### 🔒 Encapsulation
- Private attributes with `_` prefix
- Property decorators for controlled access
- Method encapsulation within classes

### 🏗️ Inheritance  
- `BaseEntity` as parent class for all game objects
- Tower hierarchy: `BaseTower` → `CannonTower`, `MachineTower`, `FreezeTower`
- Enemy hierarchy: `BaseEnemy` → `BasicEnemy`, `FastEnemy`, `TankEnemy`

### 🔄 Polymorphism
- Abstract methods requiring implementation in subclasses
- Same interface, different behaviors (`attack()`, `move()`, `draw()`)
- Duck typing leveraging Python's dynamic nature

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Pygame 2.5.0+

### Installation
```bash
git clone https://github.com/yourusername/tower-defense-oop.git
cd tower-defense-oop
pip install -r requirements.txt


tower-defense-oop/
├── README.md                   # 專案說明文檔
├── requirements.txt            # Python套件需求
├── .gitignore                 # Git忽略檔案
├── main.py                    # 主程式入口
├── docs/                      # 文檔資料夾
│   ├── README.md
│   ├── gameplay.md            # 遊戲玩法說明
│   ├── oop_design.md          # OOP設計說明
│   └── images/                # 文檔用圖片
├── src/                       # 原始碼資料夾
│   ├── __init__.py
│   ├── game/                  # 遊戲核心模組
│   │   ├── __init__.py
│   │   ├── game_manager.py    # 遊戲管理器
│   │   ├── map_manager.py     # 地圖管理
│   │   └── wave_manager.py    # 波數管理
│   ├── entities/              # 遊戲實體模組
│   │   ├── __init__.py
│   │   ├── base_entity.py     # 基礎實體類別
│   │   ├── towers/            # 塔類別模組
│   │   │   ├── __init__.py
│   │   │   ├── base_tower.py  # 塔基礎類別
│   │   │   ├── cannon_tower.py
│   │   │   ├── machine_tower.py
│   │   │   └── freeze_tower.py
│   │   ├── enemies/           # 敵人類別模組
│   │   │   ├── __init__.py
│   │   │   ├── base_enemy.py  # 敵人基礎類別
│   │   │   ├── basic_enemy.py
│   │   │   ├── fast_enemy.py
│   │   │   └── tank_enemy.py
│   │   └── projectiles/       # 投射物類別模組
│   │       ├── __init__.py
│   │       ├── base_projectile.py
│   │       ├── cannon_ball.py
│   │       ├── bullet.py
│   │       └── ice_ball.py
│   ├── ui/                    # 使用者介面模組
│   │   ├── __init__.py
│   │   ├── game_ui.py         # 遊戲UI
│   │   └── menu.py            # 選單系統
│   └── utils/                 # 工具模組
│       ├── __init__.py
│       ├── constants.py       # 常數定義
│       ├── helpers.py         # 輔助函數
│       └── animation.py       # 動畫處理
├── assets/                    # 遊戲資源
│   ├── images/
│   │   ├── towers/
│   │   ├── enemies/
│   │   ├── projectiles/
│   │   ├── map/
│   │   └── ui/
│   └── sounds/
├── tests/                     # 測試檔案
│   ├── __init__.py
│   ├── test_towers.py
│   ├── test_enemies.py
│   └── test_game_logic.py
└── screenshots/               # 遊戲截圖
    ├── gameplay1.png
    ├── gameplay2.png
    └── demo.gif
