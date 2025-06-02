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


tower_defense_game/
├── main.py                 # 主程式入口
├── game/
│   ├── __init__.py
│   ├── game_manager.py     # 遊戲主控制器
│   ├── map.py             # 地圖系統
│   └── ui.py              # 使用者介面
├── entities/
│   ├── __init__.py
│   ├── base_entity.py     # 基礎實體類別
│   ├── tower.py           # 塔類別系統
│   ├── enemy.py           # 敵人類別系統
│   └── projectile.py      # 子彈/投射物系統
├── utils/
│   ├── __init__.py
│   ├── constants.py       # 遊戲常數
│   ├── helpers.py         # 輔助函數
│   └── animation.py       # 動畫處理
├── assets/
│   ├── images/
│   │   ├── towers/        # 塔的圖片
│   │   ├── enemies/       # 敵人圖片
│   │   ├── projectiles/   # 子彈圖片
│   │   ├── map/           # 地圖素材
│   │   └── ui/           # UI元素
│   └── sounds/           # 音效檔案
├── levels/
│   └── level_data.py     # 關卡資料
└── requirements.txt      # 套件需求
