# 🐝 SwarmOracle

> **Lightweight Swarm Intelligence Prediction Engine** — Zero Dependencies, 4 Algorithms, TUI Dashboard, Multi-Format Export

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)

---

<a href="https://github.com/gitstq/SwarmOracle/releases"><img src="https://img.shields.io/badge/Release-v1.0.0-blue.svg" alt="Release"></a>
<a href="https://github.com/gitstq/SwarmOracle/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License"></a>
<a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/Python-3.7+-yellow.svg" alt="Python"></a>
<img src="https://img.shields.io/badge/Dependencies-Zero-success.svg" alt="Zero Dependencies">

---

## English

### 🎉 About

**SwarmOracle** is a lightweight, zero-dependency Python engine for swarm intelligence optimization and prediction. It implements four classic metaheuristic algorithms — **PSO, ACO, GA, DE** — with a beautiful terminal UI dashboard, multi-format result export, and 10 built-in benchmark functions.

**Why SwarmOracle?**
- 🚀 **Zero Dependencies** — Pure Python standard library, no pip install needed
- 🧠 **4 Algorithms** — PSO, ACO, GA, DE in one unified interface
- 📊 **TUI Dashboard** — Real-time ASCII convergence charts and progress visualization
- 📐 **10 Benchmarks** — Sphere, Rastrigin, Rosenbrock, Ackley, and more
- 📁 **Multi-Format Export** — JSON, CSV, Markdown result export
- 🎯 **Custom Functions** — Use your own objective functions with any bounds
- ⚡ **Fast & Lightweight** — Optimized for speed, minimal memory footprint
- 🔧 **Highly Configurable** — Fine-tune every algorithm parameter

### ✨ Core Features

| Feature | Description |
|---------|-------------|
| **PSO** | Particle Swarm Optimization with adaptive inertia weight |
| **ACO** | Ant Colony Optimization for continuous domains |
| **GA** | Genetic Algorithm with tournament selection & blend crossover |
| **DE** | Differential Evolution with multiple strategies (rand1, best1, rand2) |
| **TUI Dashboard** | ASCII charts, progress bars, color-coded output |
| **Benchmark Suite** | 10 classic optimization test functions |
| **Result Export** | JSON, CSV, Markdown formats |
| **Algorithm Comparison** | Side-by-side comparison with ranking |

### 🚀 Quick Start

**No installation required** — just clone and run:

```bash
# Clone the repository
git clone https://github.com/gitstq/SwarmOracle.git
cd SwarmOracle

# Run PSO on Sphere function
python swarmoracle.py run --algo pso --func sphere --dim 10 --iter 100

# Compare all algorithms on Rastrigin
python swarmoracle.py compare --func rastrigin --dim 10 --iter 100

# Run full benchmark suite
python swarmoracle.py bench --dim 5 --iter 50

# List available algorithms and functions
python swarmoracle.py list
```

### 📖 Usage Guide

#### Run Single Optimization

```bash
# Basic usage
python swarmoracle.py run --algo pso --func sphere --dim 10 --iter 200 --pop 50

# With custom parameters
python swarmoracle.py run --algo ga --func rosenbrock --dim 5 --iter 300 --pop 40 --seed 42

# Export results
python swarmoracle.py run --algo de --func ackley --dim 10 --iter 100 --export ./results

# Without TUI dashboard
python swarmoracle.py run --algo pso --func sphere --dim 5 --iter 50 --no-ui
```

#### Compare Algorithms

```bash
# Compare all 4 algorithms on a benchmark
python swarmoracle.py compare --func rastrigin --dim 10 --iter 200 --pop 50

# With export
python swarmoracle.py compare --func rosenbrock --dim 5 --iter 100 --export ./comparison
```

#### Full Benchmark

```bash
# Run all algorithms on all benchmarks
python swarmoracle.py bench --dim 5 --iter 50 --pop 20

# With larger dimensions
python swarmoracle.py bench --dim 10 --iter 100 --pop 30 --export ./bench_results
```

#### Custom Bounds

```bash
# Custom search space bounds
python swarmoracle.py custom --algo pso --dim 3 --bounds "-10,10" "-5,5" "-3,3" --iter 100
```

#### Use as Python Library

```python
import sys
sys.path.insert(0, "path/to/SwarmOracle")

from src.algorithms import PSO, DE
from src.utils.benchmarks import sphere, rastrigin

# Simple optimization
optimizer = PSO(
    objective_func=sphere,
    dim=10,
    bounds=[(-5.12, 5.12)] * 10,
    seed=42,
)
result = optimizer.optimize(max_iter=200, pop_size=30)
print(result.summary())

# Custom objective function
def my_function(x):
    return sum((xi - 3.0) ** 2 for xi in x)

optimizer = DE(
    objective_func=my_function,
    dim=5,
    bounds=[(-10, 10)] * 5,
    seed=42,
)
result = optimizer.optimize(max_iter=100, pop_size=20)
print(f"Best position: {result.best_position}")
print(f"Best fitness: {result.best_fitness}")
```

### 💡 Design Philosophy & Roadmap

**Design Principles:**
- **Simplicity First** — Zero external dependencies, works everywhere Python runs
- **Performance Matters** — Optimized inner loops, minimal object creation
- **Extensibility** — Clean base class makes adding new algorithms trivial
- **Developer Experience** — Beautiful TUI, clear error messages, comprehensive docs

**Roadmap:**
- [ ] Multi-objective optimization (NSGA-II, MOEA/D)
- [ ] Parallel evaluation support
- [ ] Constraint handling mechanisms
- [ ] Interactive parameter tuning mode
- [ ] Web-based visualization dashboard
- [ ] Plugin system for custom algorithms

### 📦 Project Structure

```
SwarmOracle/
├── swarmoracle.py          # CLI entry point
├── pyproject.toml          # Project configuration
├── LICENSE                 # MIT License
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── models.py       # Base classes & data structures
│   ├── algorithms/
│   │   ├── __init__.py
│   │   ├── pso.py          # Particle Swarm Optimization
│   │   ├── aco.py          # Ant Colony Optimization
│   │   ├── ga.py           # Genetic Algorithm
│   │   └── de.py           # Differential Evolution
│   ├── ui/
│   │   ├── __init__.py
│   │   └── dashboard.py    # TUI Dashboard
│   ├── export/
│   │   ├── __init__.py
│   │   └── formats.py      # JSON/CSV/Markdown export
│   └── utils/
│       ├── __init__.py
│       └── benchmarks.py   # 10 benchmark functions
├── tests/
│   └── test_algorithms.py  # Unit tests
└── examples/
    └── quickstart.py       # Usage examples
```

### 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Commit Convention:** Follow Angular commit format — `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`

### 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 简体中文

### 🎉 项目介绍

**SwarmOracle** 是一个轻量级、零依赖的 Python 群体智能优化与预测引擎。它实现了四种经典元启发式算法 — **PSO（粒子群）、ACO（蚁群）、GA（遗传算法）、DE（差分进化）** — 配备精美的终端仪表盘、多格式结果导出和10个内置基准测试函数。

**为什么选择 SwarmOracle？**
- 🚀 **零依赖** — 纯 Python 标准库，无需 pip install
- 🧠 **4种算法** — PSO、ACO、GA、DE 统一接口
- 📊 **TUI仪表盘** — 实时ASCII收敛曲线和进度可视化
- 📐 **10个基准函数** — Sphere、Rastrigin、Rosenbrock、Ackley 等
- 📁 **多格式导出** — JSON、CSV、Markdown 结果导出
- 🎯 **自定义函数** — 支持任意目标函数和搜索边界
- ⚡ **快速轻量** — 优化内循环，最小内存占用
- 🔧 **高度可配置** — 精细调节每个算法参数

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| **PSO** | 带自适应惯性权重的粒子群优化 |
| **ACO** | 连续域蚁群优化 |
| **GA** | 锦标赛选择 + 混合交叉的遗传算法 |
| **DE** | 多策略差分进化（rand1、best1、rand2） |
| **TUI仪表盘** | ASCII图表、进度条、彩色输出 |
| **基准测试套件** | 10个经典优化测试函数 |
| **结果导出** | JSON、CSV、Markdown 格式 |
| **算法对比** | 并排比较与排名 |

### 🚀 快速开始

**无需安装** — 克隆即可运行：

```bash
# 克隆仓库
git clone https://github.com/gitstq/SwarmOracle.git
cd SwarmOracle

# 在Sphere函数上运行PSO
python swarmoracle.py run --algo pso --func sphere --dim 10 --iter 100

# 在Rastrigin上对比所有算法
python swarmoracle.py compare --func rastrigin --dim 10 --iter 100

# 运行完整基准测试
python swarmoracle.py bench --dim 5 --iter 50

# 查看可用算法和函数
python swarmoracle.py list
```

### 📖 详细使用指南

#### 运行单次优化

```bash
# 基本用法
python swarmoracle.py run --algo pso --func sphere --dim 10 --iter 200 --pop 50

# 自定义参数
python swarmoracle.py run --algo ga --func rosenbrock --dim 5 --iter 300 --pop 40 --seed 42

# 导出结果
python swarmoracle.py run --algo de --func ackley --dim 10 --iter 100 --export ./results
```

#### 算法对比

```bash
# 在一个基准函数上对比所有4种算法
python swarmoracle.py compare --func rastrigin --dim 10 --iter 200 --pop 50
```

#### 作为Python库使用

```python
import sys
sys.path.insert(0, "SwarmOracle路径")

from src.algorithms import PSO, DE
from src.utils.benchmarks import sphere

optimizer = PSO(
    objective_func=sphere,
    dim=10,
    bounds=[(-5.12, 5.12)] * 10,
    seed=42,
)
result = optimizer.optimize(max_iter=200, pop_size=30)
print(result.summary())
```

### 💡 设计思路与迭代规划

**设计原则：**
- **简洁优先** — 零外部依赖，随处可运行
- **性能至上** — 优化内循环，最小化对象创建
- **可扩展性** — 清晰的基类，新增算法非常简单
- **开发者体验** — 精美TUI、清晰错误提示、完善文档

**迭代规划：**
- [ ] 多目标优化（NSGA-II、MOEA/D）
- [ ] 并行评估支持
- [ ] 约束处理机制
- [ ] 交互式参数调优模式
- [ ] Web可视化仪表盘
- [ ] 自定义算法插件系统

### 🤝 贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建功能分支（`git checkout -b feature/amazing-feature`）
3. 提交更改（`git commit -m 'feat: 新增超棒功能'`）
4. 推送分支（`git push origin feature/amazing-feature`）
5. 发起 Pull Request

**提交规范：** 遵循 Angular 提交格式 — `feat:`、`fix:`、`docs:`、`refactor:`、`test:`、`chore:`

### 📄 开源协议

本项目基于 MIT 协议开源 — 详见 [LICENSE](LICENSE) 文件。

---

## 繁體中文

### 🎉 專案介紹

**SwarmOracle** 是一個輕量級、零依賴的 Python 群體智慧最佳化與預測引擎。它實現了四種經典元啟發式演算法 — **PSO（粒子群）、ACO（蟻群）、GA（遺傳演算法）、DE（差分進化）** — 配備精美的終端儀表板、多格式結果匯出和10個內建基準測試函數。

**為什麼選擇 SwarmOracle？**
- 🚀 **零依賴** — 純 Python 標準庫，無需 pip install
- 🧠 **4種演算法** — PSO、ACO、GA、DE 統一介面
- 📊 **TUI儀表板** — 即時ASCII收斂曲線和進度視覺化
- 📐 **10個基準函數** — Sphere、Rastrigin、Rosenbrock、Ackley 等
- 📁 **多格式匯出** — JSON、CSV、Markdown 結果匯出
- 🎯 **自訂函數** — 支援任意目標函數和搜尋邊界
- ⚡ **快速輕量** — 最佳化內迴圈，最小記憶體佔用
- 🔧 **高度可配置** — 精細調節每個演算法參數

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| **PSO** | 帶自適應慣性權重的粒子群最佳化 |
| **ACO** | 連續域蟻群最佳化 |
| **GA** | 錦標賽選擇 + 混合交叉的遺傳演算法 |
| **DE** | 多策略差分進化（rand1、best1、rand2） |
| **TUI儀表板** | ASCII圖表、進度條、彩色輸出 |
| **基準測試套件** | 10個經典最佳化測試函數 |
| **結果匯出** | JSON、CSV、Markdown 格式 |
| **演算法對比** | 並排比較與排名 |

### 🚀 快速開始

**無需安裝** — 克隆即可執行：

```bash
# 克隆倉庫
git clone https://github.com/gitstq/SwarmOracle.git
cd SwarmOracle

# 在Sphere函數上執行PSO
python swarmoracle.py run --algo pso --func sphere --dim 10 --iter 100

# 在Rastrigin上對比所有演算法
python swarmoracle.py compare --func rastrigin --dim 10 --iter 100

# 執行完整基準測試
python swarmoracle.py bench --dim 5 --iter 50

# 查看可用演算法和函數
python swarmoracle.py list
```

### 📖 詳細使用指南

#### 執行單次最佳化

```bash
# 基本用法
python swarmoracle.py run --algo pso --func sphere --dim 10 --iter 200 --pop 50

# 自訂參數
python swarmoracle.py run --algo ga --func rosenbrock --dim 5 --iter 300 --pop 40 --seed 42

# 匯出結果
python swarmoracle.py run --algo de --func ackley --dim 10 --iter 100 --export ./results
```

#### 作為Python庫使用

```python
import sys
sys.path.insert(0, "SwarmOracle路徑")

from src.algorithms import PSO, DE
from src.utils.benchmarks import sphere

optimizer = PSO(
    objective_func=sphere,
    dim=10,
    bounds=[(-5.12, 5.12)] * 10,
    seed=42,
)
result = optimizer.optimize(max_iter=200, pop_size=30)
print(result.summary())
```

### 💡 設計理念與迭代規劃

**設計原則：**
- **簡潔優先** — 零外部依賴，隨處可執行
- **效能至上** — 最佳化內迴圈，最小化物件建立
- **可擴展性** — 清晰的基礎類別，新增演算法非常簡單
- **開發者體驗** — 精美TUI、清晰錯誤提示、完善文件

**迭代規劃：**
- [ ] 多目標最佳化（NSGA-II、MOEA/D）
- [ ] 平行評估支援
- [ ] 約束處理機制
- [ ] 互動式參數調優模式
- [ ] Web視覺化儀表板
- [ ] 自訂演算法外掛系統

### 🤝 貢獻指南

歡迎貢獻！請遵循以下步驟：

1. Fork 本倉庫
2. 建立功能分支（`git checkout -b feature/amazing-feature`）
3. 提交變更（`git commit -m 'feat: 新增超棒功能'`）
4. 推送分支（`git push origin feature/amazing-feature`）
5. 發起 Pull Request

**提交規範：** 遵循 Angular 提交格式 — `feat:`、`fix:`、`docs:`、`refactor:`、`test:`、`chore:`

### 📄 開源協議

本專案基於 MIT 協議開源 — 詳見 [LICENSE](LICENSE) 檔案。
