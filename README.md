# A* Pathfinding Algorithm - Advanced Visualization

<div align="center">

**Professional implementation with comprehensive visualization for presentations and education**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.5+-green.svg)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## 🌟 Features

### Core Algorithm
- ✅ **Optimal pathfinding** using A* algorithm
- ✅ **8-directional movement** with proper diagonal handling
- ✅ **Euclidean heuristic** for accurate distance estimation
- ✅ **Priority queue** implementation using heapq
- ✅ **Complete and optimal** - guaranteed to find shortest path

### Advanced Visualization
- 🎨 **Real-time f/g/h scores** displayed on each node
- 🎨 **Color-coded exploration** showing algorithm progress
- 🎨 **Current node highlighting** in pink during exploration
- 🎨 **Animated path reveal** with directional arrows
- 🎨 **Gradient effects** and smooth animations
- 🎨 **Hover inspection** for detailed node information

### Statistics & Metrics
- 📊 **Live algorithm metrics** (iterations, nodes explored, etc.)
- 📊 **Execution time tracking** in milliseconds
- 📊 **Path cost calculation** with accurate movement costs
- 📊 **Open/closed set sizes** for complexity analysis
- 📊 **Comprehensive statistics panel** with all metrics

### Interactive Controls
- 🎮 **Draw obstacles** with mouse drag
- 🎮 **Set start/end points** interactively
- 🎮 **Adjustable animation speed** (+/- keys)
- 🎮 **Step-by-step mode** for detailed analysis
- 🎮 **Toggle features** (arrows, scores, etc.)
- 🎮 **Preset maze patterns** for demonstrations

## 🚀 Quick Start

### Installation
```bash
# Clone or download the repository
cd A-star-algorithm

# Install dependencies
pip install -r requirements.txt

# Run the visualization
python main.py
```

### Basic Usage
1. **Launch** the program
2. **Press SPACE** to run A* on the default maze
3. **Watch** the algorithm explore and find the optimal path
4. **Experiment** by drawing your own obstacles

## 📖 Documentation

- **[QUICK_START.md](QUICK_START.md)** - Step-by-step guide for beginners
- **[ALGORITHM_EXPLANATION.md](ALGORITHM_EXPLANATION.md)** - Detailed algorithm explanation
- **[test_astar.py](test_astar.py)** - Comprehensive test suite

## 🎮 Controls Reference

| Key | Action |
|-----|--------|
| `SPACE` | Run/Pause A* algorithm |
| `R` | Reset visualization (keep obstacles) |
| `C` | Clear entire grid |
| `S` | Set start point (hover over cell) |
| `E` | Set end point (hover over cell) |
| `A` | Toggle path arrows |
| `+` / `-` | Adjust animation speed |
| `LEFT DRAG` | Draw obstacles |
| `RIGHT DRAG` | Erase obstacles |

## 🎨 Visualization Guide

### Color Scheme
- 🟢 **Green** - Start point
- 🔴 **Red** - End/goal point
- ⬛ **Dark Gray** - Obstacles/walls
- 🔵 **Blue** - Open set (nodes being considered)
- ⚪ **Gray** - Closed set (already explored)
- 🟡 **Gold** - Final optimal path
- 💗 **Pink** - Current node being processed

### Node Information Display
```
g:5.0  ← Cost from start to this node
  10.2 ← f-score (total estimated cost)
h:5.2  ← Heuristic estimate to goal
```

## 🧪 Testing

Run the comprehensive test suite:
```bash
python test_astar.py
```

All 8 tests should pass:
- ✓ Heuristic calculation
- ✓ Movement cost accuracy
- ✓ Grid neighbor generation
- ✓ Simple pathfinding
- ✓ Diagonal movement
- ✓ Obstacle avoidance
- ✓ No-path detection
- ✓ Algorithm statistics

## 🏗️ Architecture

### Core Components
1. **Node** - Priority queue element with f/g/h scores
2. **Grid** - 2D grid representation with validation
3. **AStar** - Pure algorithm implementation
4. **AlgorithmStats** - Metrics tracking
5. **AdvancedVisualizer** - Pygame-based visualization

### Algorithm Formula
```
f(n) = g(n) + h(n)

where:
  f(n) = total estimated cost
  g(n) = actual cost from start
  h(n) = heuristic estimate to goal
```

## 📊 Performance

- **Time Complexity**: O(b^d) where b=branching factor, d=depth
- **Space Complexity**: O(b^d) for node storage
- **Optimality**: Guaranteed with admissible heuristic
- **Completeness**: Always finds path if one exists

## 🎓 Educational Value

Perfect for:
- **Algorithm courses** - Visual demonstration of A* mechanics
- **Presentations** - Professional visualization with metrics
- **Learning** - Interactive experimentation
- **Research** - Baseline implementation for comparisons

## 📁 Project Structure

```
A-star-algorithm/
├── main.py                    # Main implementation (807 lines)
├── test_astar.py              # Test suite (169 lines)
├── requirements.txt           # Dependencies
├── README.md                  # This file
├── QUICK_START.md            # Beginner guide
└── ALGORITHM_EXPLANATION.md  # Detailed documentation
```

## 🔬 Key Implementation Details

- **Diagonal blocking prevention** - No squeezing through corners
- **Tie-breaking** - Consistent ordering in priority queue
- **Path reconstruction** - Efficient parent pointer backtracking
- **Real-time callbacks** - Step-by-step visualization support
- **Comprehensive metrics** - Full algorithm introspection

## 💡 Tips for Presentations

1. **Slow down** animation with `-` key for explanations
2. **Show scores** on nodes to explain f/g/h values
3. **Hover over nodes** to display detailed information
4. **Use preset mazes** for consistent demonstrations
5. **Toggle arrows** to show path direction clearly

## 🤝 Contributing

This is an educational implementation. Feel free to:
- Extend with new heuristics (Manhattan, Chebyshev)
- Add algorithm comparisons (Dijkstra, BFS, DFS)
- Implement weighted grids
- Add more visualization features

## 📄 License

MIT License - Free for educational and commercial use

---

<div align="center">

**Built with attention to code quality, educational value, and presentation readiness**

⭐ Star this repository if you find it useful!

</div>

