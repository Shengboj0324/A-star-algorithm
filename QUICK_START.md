# A* Algorithm Visualization - Quick Start Guide

## 🚀 Running the Program

```bash
python main.py
```

## 🎮 Basic Workflow

1. **Launch** the program
2. **Press SPACE** to run the algorithm with default maze
3. **Watch** the visualization:
   - Blue nodes = being considered
   - Gray nodes = already explored
   - Pink node = currently processing
   - Gold path = final solution

## 🎨 Creating Your Own Scenarios

### Setting Start/End Points
1. Press **S** key
2. Hover over desired cell
3. Press **E** key
4. Hover over desired cell

### Drawing Obstacles
- **Hold LEFT mouse button** and drag to draw walls
- **Hold RIGHT mouse button** and drag to erase

### Running the Algorithm
- Press **SPACE** to start pathfinding
- Press **R** to reset and try again
- Press **C** to clear everything

## 📊 Understanding the Visualization

### Node Scores (displayed on cells)
```
g:5.0  ← Cost from start
  10.2 ← f-score (total)
h:5.2  ← Heuristic to goal
```

### Color Meanings
- **Green**: Start position
- **Red**: Goal position
- **Dark Gray**: Obstacles/walls
- **Blue**: Open set (frontier to explore)
- **Light Gray**: Closed set (already explored)
- **Gold**: Final optimal path
- **Pink**: Current node being processed

### Statistics Panel (right side)
- **Iterations**: Number of algorithm steps
- **Nodes Explored**: Total nodes examined
- **Open Set Size**: Current frontier size
- **Path Length**: Number of steps in solution
- **Path Cost**: Total movement cost
- **Time**: Algorithm execution time

## 🎯 Tips for Presentations

### Slow Down Animation
- Press **-** (minus) to slow down
- Press **+** (plus) to speed up
- Adjust until you can explain each step

### Show Algorithm Details
- Use **larger cell size** (35-40px) to see f/g/h scores
- **Hover over nodes** to see detailed information
- **Toggle arrows** with 'A' to show path direction

### Interesting Scenarios

1. **Simple Path**: Clear grid, diagonal start to end
2. **Maze Navigation**: Use preset maze pattern
3. **No Solution**: Completely wall off the goal
4. **Multiple Paths**: Create several routes, watch A* choose optimal

## 🔧 Customization

### Change Grid Size
Edit `main.py`:
```python
grid = Grid(width=40, height=25)  # Larger grid
```

### Change Cell Size
```python
visualizer = AdvancedVisualizer(grid, cell_size=40)  # Bigger cells
```

### Create Custom Obstacles
```python
# Vertical wall
for y in range(10):
    grid.set_cell((5, y), CellType.OBSTACLE)

# Horizontal wall
for x in range(10):
    grid.set_cell((x, 5), CellType.OBSTACLE)
```

## 🎓 Educational Use

### For Teaching
1. Start with **empty grid** - show simple diagonal path
2. Add **single obstacle** - show how A* routes around it
3. Create **maze** - demonstrate intelligent exploration
4. Show **no solution** - prove algorithm completeness

### Key Points to Highlight
- **f = g + h**: The core formula
- **Priority queue**: Always explores lowest f-score first
- **Heuristic**: Guides search toward goal
- **Optimality**: Guaranteed shortest path
- **Efficiency**: Much faster than blind search

## 🐛 Troubleshooting

### Program won't start
```bash
pip install pygame
```

### Visualization too fast
- Press **-** multiple times to slow down
- Or edit `animation_speed` in code

### Can't see scores on nodes
- Increase `cell_size` parameter
- Scores only show on cells ≥30px

### Path looks wrong
- A* finds **optimal** path by cost
- Diagonal moves cost √2 ≈ 1.414
- Path minimizes total cost, not just step count

## 📝 Running Tests

Verify implementation correctness:
```bash
python test_astar.py
```

All tests should pass ✓

## 🎬 Demo Scenarios

### Scenario 1: Direct Path
- Clear grid (press C)
- Set start at (0, 0)
- Set end at (10, 10)
- Press SPACE
- **Shows**: Diagonal movement, minimal exploration

### Scenario 2: Wall Avoidance
- Use default maze
- Press SPACE
- **Shows**: Intelligent routing around obstacles

### Scenario 3: Complex Maze
- Draw intricate maze pattern
- Press SPACE
- **Shows**: Systematic exploration, optimal path finding

Enjoy exploring the A* algorithm! 🌟

