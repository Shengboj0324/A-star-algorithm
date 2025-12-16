"""
Unit tests for A* algorithm implementation
"""

from main import Grid, AStar, CellType, AlgorithmStats
import math


def test_simple_path():
    """Test A* finds a simple straight path"""
    grid = Grid(10, 10)
    start = (0, 0)
    end = (5, 0)
    
    path = AStar.find_path(grid, start, end)
    
    assert path is not None, "Path should be found"
    assert path[0] == start, "Path should start at start position"
    assert path[-1] == end, "Path should end at end position"
    assert len(path) == 6, f"Path length should be 6, got {len(path)}"
    print("✓ Simple path test passed")


def test_path_with_obstacle():
    """Test A* navigates around obstacles"""
    grid = Grid(10, 10)
    start = (0, 5)
    end = (9, 5)
    
    # Create vertical wall
    for y in range(10):
        if y != 5:  # Leave gap at y=5
            grid.set_cell((5, y), CellType.OBSTACLE)
    
    path = AStar.find_path(grid, start, end)
    
    assert path is not None, "Path should be found"
    assert path[0] == start, "Path should start at start position"
    assert path[-1] == end, "Path should end at end position"
    
    # Verify path doesn't go through obstacles
    for pos in path:
        assert grid.is_walkable(pos), f"Path goes through obstacle at {pos}"
    
    print("✓ Obstacle avoidance test passed")


def test_no_path():
    """Test A* returns None when no path exists"""
    grid = Grid(10, 10)
    start = (0, 0)
    end = (9, 9)
    
    # Create complete wall blocking the path
    for y in range(10):
        grid.set_cell((5, y), CellType.OBSTACLE)
    
    path = AStar.find_path(grid, start, end)
    
    assert path is None, "No path should be found when completely blocked"
    print("✓ No path test passed")


def test_diagonal_movement():
    """Test A* uses diagonal movement efficiently"""
    grid = Grid(10, 10)
    start = (0, 0)
    end = (5, 5)
    
    path = AStar.find_path(grid, start, end)
    
    assert path is not None, "Path should be found"
    assert path[0] == start, "Path should start at start position"
    assert path[-1] == end, "Path should end at end position"
    
    # Diagonal path should be shorter than cardinal-only path
    assert len(path) <= 6, f"Diagonal path should be efficient, got length {len(path)}"
    print("✓ Diagonal movement test passed")


def test_heuristic():
    """Test heuristic function"""
    # Test Euclidean distance
    dist = AStar.heuristic((0, 0), (3, 4))
    expected = 5.0  # 3-4-5 triangle
    assert abs(dist - expected) < 0.01, f"Heuristic should be {expected}, got {dist}"
    
    # Test same position
    dist = AStar.heuristic((5, 5), (5, 5))
    assert dist == 0.0, "Heuristic for same position should be 0"
    
    print("✓ Heuristic test passed")


def test_movement_cost():
    """Test movement cost calculation"""
    # Cardinal movement
    cost = AStar.get_movement_cost((0, 0), (1, 0))
    assert cost == 1.0, f"Cardinal movement cost should be 1.0, got {cost}"

    # Diagonal movement
    cost = AStar.get_movement_cost((0, 0), (1, 1))
    expected = math.sqrt(2)
    assert abs(cost - expected) < 0.01, f"Diagonal movement cost should be ~{expected}, got {cost}"

    print("✓ Movement cost test passed")


def test_algorithm_stats():
    """Test statistics tracking"""
    grid = Grid(10, 10)
    start = (0, 0)
    end = (5, 5)
    stats = AlgorithmStats()

    path = AStar.find_path(grid, start, end, stats=stats)

    assert path is not None, "Path should be found"
    assert stats.nodes_explored > 0, "Should have explored nodes"
    assert stats.path_length > 0, "Path length should be recorded"
    assert stats.path_cost > 0, "Path cost should be recorded"
    assert stats.execution_time > 0, "Execution time should be recorded"

    print("✓ Algorithm stats test passed")


def test_grid_neighbors():
    """Test neighbor generation"""
    grid = Grid(5, 5)
    
    # Corner position should have 3 neighbors
    neighbors = grid.get_neighbors((0, 0))
    assert len(neighbors) == 3, f"Corner should have 3 neighbors, got {len(neighbors)}"
    
    # Center position should have 8 neighbors
    neighbors = grid.get_neighbors((2, 2))
    assert len(neighbors) == 8, f"Center should have 8 neighbors, got {len(neighbors)}"
    
    # Add obstacle and check neighbors are reduced
    grid.set_cell((2, 1), CellType.OBSTACLE)
    neighbors = grid.get_neighbors((2, 2))
    assert len(neighbors) < 8, "Neighbors should be reduced when obstacle present"
    
    print("✓ Grid neighbors test passed")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Running A* Algorithm Tests")
    print("=" * 60)

    test_heuristic()
    test_movement_cost()
    test_grid_neighbors()
    test_simple_path()
    test_diagonal_movement()
    test_path_with_obstacle()
    test_no_path()
    test_algorithm_stats()

    print("=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()

