"""
A* Pathfinding Algorithm - Advanced Implementation with Professional Visualization
Comprehensive implementation with detailed metrics, animations, and educational features
"""

import pygame
import heapq
import math
import time
from dataclasses import dataclass, field
from typing import Optional, List, Tuple, Set, Dict
from enum import Enum
from collections import deque


class CellType(Enum):
    """Cell types in the grid"""
    EMPTY = 0
    OBSTACLE = 1
    START = 2
    END = 3
    PATH = 4
    OPEN = 5
    CLOSED = 6


@dataclass(order=True)
class Node:
    """Node in the A* search space with priority queue support"""
    f_score: float
    position: Tuple[int, int] = field(compare=False)
    g_score: float = field(compare=False)
    h_score: float = field(compare=False)
    parent: Optional['Node'] = field(default=None, compare=False)
    timestamp: float = field(default=0.0, compare=False)  # For animation


class AlgorithmStats:
    """Track algorithm execution statistics"""
    def __init__(self):
        self.nodes_explored = 0
        self.nodes_in_open = 0
        self.max_open_size = 0
        self.path_length = 0
        self.path_cost = 0.0
        self.execution_time = 0.0
        self.iterations = 0

    def reset(self):
        self.__init__()


class Grid:
    """Grid representation for pathfinding"""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.cells = [[CellType.EMPTY for _ in range(width)] for _ in range(height)]
        self.start: Optional[Tuple[int, int]] = None
        self.end: Optional[Tuple[int, int]] = None

    def is_valid(self, pos: Tuple[int, int]) -> bool:
        """Check if position is within grid bounds"""
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def is_walkable(self, pos: Tuple[int, int]) -> bool:
        """Check if position is walkable (not an obstacle)"""
        if not self.is_valid(pos):
            return False
        x, y = pos
        return self.cells[y][x] != CellType.OBSTACLE

    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid neighboring positions (8-directional movement)"""
        x, y = pos
        neighbors = []

        # 8 directions: up, down, left, right, and diagonals
        directions = [
            (0, -1), (0, 1), (-1, 0), (1, 0),  # Cardinal
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonal
        ]

        for dx, dy in directions:
            new_pos = (x + dx, y + dy)
            if self.is_walkable(new_pos):
                # For diagonal movement, check if path is not blocked
                if dx != 0 and dy != 0:
                    if not (self.is_walkable((x + dx, y)) or self.is_walkable((x, y + dy))):
                        continue
                neighbors.append(new_pos)

        return neighbors

    def set_cell(self, pos: Tuple[int, int], cell_type: CellType):
        """Set cell type at position"""
        if self.is_valid(pos):
            x, y = pos
            self.cells[y][x] = cell_type

    def get_cell(self, pos: Tuple[int, int]) -> CellType:
        """Get cell type at position"""
        if self.is_valid(pos):
            x, y = pos
            return self.cells[y][x]
        return CellType.OBSTACLE


class AStar:
    """A* pathfinding algorithm implementation with detailed tracking"""

    @staticmethod
    def heuristic(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """Calculate heuristic (Euclidean distance)"""
        x1, y1 = pos1
        x2, y2 = pos2
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    @staticmethod
    def get_movement_cost(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """Calculate movement cost between adjacent cells"""
        x1, y1 = pos1
        x2, y2 = pos2
        # Diagonal movement costs sqrt(2), cardinal movement costs 1
        if abs(x2 - x1) + abs(y2 - y1) == 2:
            return math.sqrt(2)
        return 1.0

    @staticmethod
    def find_path(grid: Grid, start: Tuple[int, int], end: Tuple[int, int],
                  visualize_callback=None, stats: Optional[AlgorithmStats] = None) -> Optional[List[Tuple[int, int]]]:
        """
        Find shortest path using A* algorithm with detailed tracking

        Args:
            grid: Grid object
            start: Start position (x, y)
            end: End position (x, y)
            visualize_callback: Optional callback for visualization
            stats: Optional statistics tracker

        Returns:
            List of positions forming the path, or None if no path exists
        """
        start_time = time.time()

        if not grid.is_walkable(start) or not grid.is_walkable(end):
            return None

        # Priority queue: stores (f_score, counter, node)
        open_set = []
        counter = 0

        # Track best g_score for each position
        g_scores = {start: 0.0}

        # Track visited positions
        closed_set: Set[Tuple[int, int]] = set()

        # Track all nodes for visualization
        node_map: Dict[Tuple[int, int], Node] = {}

        # Create start node
        h_start = AStar.heuristic(start, end)
        start_node = Node(f_score=h_start, position=start, g_score=0.0, h_score=h_start, timestamp=time.time())
        heapq.heappush(open_set, (start_node.f_score, counter, start_node))
        counter += 1
        node_map[start] = start_node

        # Track open positions for visualization
        open_positions: Set[Tuple[int, int]] = {start}

        while open_set:
            # Update stats
            if stats:
                stats.iterations += 1
                stats.nodes_in_open = len(open_set)
                stats.max_open_size = max(stats.max_open_size, len(open_set))

            # Get node with lowest f_score
            _, _, current = heapq.heappop(open_set)

            # Skip if already processed
            if current.position in closed_set:
                continue

            # Mark as visited
            closed_set.add(current.position)
            open_positions.discard(current.position)

            if stats:
                stats.nodes_explored += 1

            # Visualize current state
            if visualize_callback:
                visualize_callback(open_positions, closed_set, None, node_map, current.position)

            # Check if reached goal
            if current.position == end:
                path = AStar._reconstruct_path(current)
                if stats:
                    stats.path_length = len(path)
                    stats.path_cost = current.g_score
                    stats.execution_time = time.time() - start_time
                return path

            # Explore neighbors
            for neighbor_pos in grid.get_neighbors(current.position):
                if neighbor_pos in closed_set:
                    continue

                # Calculate tentative g_score
                movement_cost = AStar.get_movement_cost(current.position, neighbor_pos)
                tentative_g = current.g_score + movement_cost

                # Skip if not a better path
                if neighbor_pos in g_scores and tentative_g >= g_scores[neighbor_pos]:
                    continue

                # Update best path to neighbor
                g_scores[neighbor_pos] = tentative_g
                h_score = AStar.heuristic(neighbor_pos, end)
                f_score = tentative_g + h_score

                neighbor_node = Node(
                    f_score=f_score,
                    position=neighbor_pos,
                    g_score=tentative_g,
                    h_score=h_score,
                    parent=current,
                    timestamp=time.time()
                )

                heapq.heappush(open_set, (f_score, counter, neighbor_node))
                counter += 1
                open_positions.add(neighbor_pos)
                node_map[neighbor_pos] = neighbor_node

        # No path found
        if stats:
            stats.execution_time = time.time() - start_time
        return None

    @staticmethod
    def _reconstruct_path(node: Node) -> List[Tuple[int, int]]:
        """Reconstruct path from end node to start"""
        path = []
        current = node
        while current:
            path.append(current.position)
            current = current.parent
        return path[::-1]


class AdvancedVisualizer:
    """Advanced pygame-based visualization for A* algorithm with detailed metrics"""

    # Enhanced color scheme
    COLORS = {
        CellType.EMPTY: (250, 250, 250),      # Off-white
        CellType.OBSTACLE: (30, 30, 35),      # Very dark gray
        CellType.START: (46, 204, 113),       # Emerald green
        CellType.END: (231, 76, 60),          # Alizarin red
        CellType.PATH: (241, 196, 15),        # Sun yellow
        CellType.OPEN: (52, 152, 219),        # Peter river blue
        CellType.CLOSED: (149, 165, 166),     # Concrete gray
    }

    # UI Colors
    BG_COLOR = (245, 245, 245)
    GRID_COLOR = (220, 220, 220)
    PANEL_BG = (40, 44, 52)
    PANEL_TEXT = (255, 255, 255)
    HIGHLIGHT_COLOR = (255, 215, 0)
    CURRENT_NODE_COLOR = (255, 105, 180)  # Hot pink for current exploration

    def __init__(self, grid: Grid, cell_size: int = 35):
        self.grid = grid
        self.cell_size = cell_size
        self.grid_width = grid.width * cell_size
        self.grid_height = grid.height * cell_size

        # Add panel for statistics
        self.panel_width = 350
        self.width = self.grid_width + self.panel_width
        self.height = self.grid_height

        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("A* Pathfinding Algorithm - Advanced Visualization")
        self.clock = pygame.time.Clock()

        # Fonts
        self.font_large = pygame.font.SysFont('Arial', 24, bold=True)
        self.font_medium = pygame.font.SysFont('Arial', 18)
        self.font_small = pygame.font.SysFont('Arial', 14)
        self.font_mono = pygame.font.SysFont('Courier New', 14)

        # State
        self.running = True
        self.path: Optional[List[Tuple[int, int]]] = None
        self.open_set: Set[Tuple[int, int]] = set()
        self.closed_set: Set[Tuple[int, int]] = set()
        self.node_map: Dict[Tuple[int, int], Node] = {}
        self.current_node: Optional[Tuple[int, int]] = None
        self.stats = AlgorithmStats()
        self.hovered_cell: Optional[Tuple[int, int]] = None

        # Animation
        self.animation_speed = 50  # milliseconds per step
        self.step_mode = False
        self.paused = False

        # Path animation
        self.path_animation_progress = 0
        self.show_arrows = True

    def draw_grid(self):
        """Draw the grid with enhanced visuals"""
        # Fill background
        self.screen.fill(self.BG_COLOR)

        # Draw cells with gradients and effects
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                pos = (x, y)
                rect = pygame.Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )

                # Determine cell color and effects
                cell_type = self.grid.get_cell(pos)
                color = self.COLORS[cell_type]
                border_width = 1

                # Current node being explored (highlight)
                if pos == self.current_node:
                    color = self.CURRENT_NODE_COLOR
                    border_width = 3

                # Override with algorithm visualization
                elif pos in self.open_set and cell_type == CellType.EMPTY:
                    color = self.COLORS[CellType.OPEN]
                    # Add pulsing effect based on f_score
                    if pos in self.node_map:
                        node = self.node_map[pos]
                        intensity = min(255, int(150 + 50 * math.sin(time.time() * 3)))
                        color = (color[0], color[1], min(255, intensity))

                elif pos in self.closed_set and cell_type == CellType.EMPTY:
                    color = self.COLORS[CellType.CLOSED]

                elif self.path and pos in self.path and cell_type not in [CellType.START, CellType.END]:
                    # Animated path
                    path_index = self.path.index(pos)
                    if path_index < self.path_animation_progress:
                        color = self.COLORS[CellType.PATH]
                        # Gradient effect along path
                        progress = path_index / max(1, len(self.path) - 1)
                        brightness = int(200 + 55 * (1 - progress))
                        color = (brightness, brightness - 40, 0)

                # Hover effect
                if pos == self.hovered_cell:
                    color = tuple(min(255, c + 30) for c in color)
                    border_width = 2

                # Draw cell
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, self.GRID_COLOR, rect, border_width)

                # Draw f, g, h scores for open/closed nodes
                if pos in self.node_map and (pos in self.open_set or pos in self.closed_set):
                    node = self.node_map[pos]
                    self._draw_node_scores(rect, node)

                # Draw arrows for path
                if self.show_arrows and self.path and pos in self.path:
                    path_index = self.path.index(pos)
                    if path_index < len(self.path) - 1 and path_index < self.path_animation_progress:
                        next_pos = self.path[path_index + 1]
                        self._draw_arrow(rect, pos, next_pos)

    def _draw_node_scores(self, rect: pygame.Rect, node: Node):
        """Draw f, g, h scores on a node"""
        # Only draw if cell is large enough
        if self.cell_size < 30:
            return

        # Draw g score (top-left)
        g_text = self.font_small.render(f"g:{node.g_score:.1f}", True, (0, 100, 0))
        self.screen.blit(g_text, (rect.x + 2, rect.y + 2))

        # Draw h score (top-right)
        h_text = self.font_small.render(f"h:{node.h_score:.1f}", True, (100, 0, 0))
        self.screen.blit(h_text, (rect.x + 2, rect.y + rect.height - 16))

        # Draw f score (center, larger)
        if self.cell_size >= 40:
            f_text = self.font_small.render(f"{node.f_score:.1f}", True, (0, 0, 100))
            text_rect = f_text.get_rect(center=rect.center)
            self.screen.blit(f_text, text_rect)

    def _draw_arrow(self, rect: pygame.Rect, from_pos: Tuple[int, int], to_pos: Tuple[int, int]):
        """Draw directional arrow showing path flow"""
        if self.cell_size < 25:
            return

        # Calculate arrow direction
        dx = to_pos[0] - from_pos[0]
        dy = to_pos[1] - from_pos[1]

        # Arrow center
        center_x = rect.centerx
        center_y = rect.centery

        # Arrow endpoint
        arrow_length = self.cell_size // 4
        end_x = center_x + dx * arrow_length
        end_y = center_y + dy * arrow_length

        # Draw arrow line
        pygame.draw.line(self.screen, (50, 50, 50), (center_x, center_y), (end_x, end_y), 2)

        # Draw arrowhead
        angle = math.atan2(dy, dx)
        arrow_size = 5
        left_x = end_x - arrow_size * math.cos(angle - math.pi / 6)
        left_y = end_y - arrow_size * math.sin(angle - math.pi / 6)
        right_x = end_x - arrow_size * math.cos(angle + math.pi / 6)
        right_y = end_y - arrow_size * math.sin(angle + math.pi / 6)

        pygame.draw.polygon(self.screen, (50, 50, 50), [(end_x, end_y), (left_x, left_y), (right_x, right_y)])

    def draw_info_panel(self):
        """Draw information panel with statistics and controls"""
        panel_x = self.grid_width

        # Panel background
        panel_rect = pygame.Rect(panel_x, 0, self.panel_width, self.height)
        pygame.draw.rect(self.screen, self.PANEL_BG, panel_rect)

        y_offset = 20

        # Title
        title = self.font_large.render("A* ALGORITHM", True, self.PANEL_TEXT)
        self.screen.blit(title, (panel_x + 20, y_offset))
        y_offset += 50

        # Statistics
        stats_title = self.font_medium.render("Statistics:", True, self.HIGHLIGHT_COLOR)
        self.screen.blit(stats_title, (panel_x + 20, y_offset))
        y_offset += 30

        stats_data = [
            f"Iterations: {self.stats.iterations}",
            f"Nodes Explored: {self.stats.nodes_explored}",
            f"Open Set Size: {self.stats.nodes_in_open}",
            f"Max Open Size: {self.stats.max_open_size}",
            f"Closed Set: {len(self.closed_set)}",
            f"Path Length: {self.stats.path_length}",
            f"Path Cost: {self.stats.path_cost:.2f}",
            f"Time: {self.stats.execution_time*1000:.1f}ms",
        ]

        for stat in stats_data:
            text = self.font_mono.render(stat, True, self.PANEL_TEXT)
            self.screen.blit(text, (panel_x + 20, y_offset))
            y_offset += 22

        y_offset += 20

        # Hovered cell info
        if self.hovered_cell and self.hovered_cell in self.node_map:
            hover_title = self.font_medium.render("Hovered Node:", True, self.HIGHLIGHT_COLOR)
            self.screen.blit(hover_title, (panel_x + 20, y_offset))
            y_offset += 30

            node = self.node_map[self.hovered_cell]
            hover_data = [
                f"Position: {self.hovered_cell}",
                f"F-score: {node.f_score:.2f}",
                f"G-score: {node.g_score:.2f}",
                f"H-score: {node.h_score:.2f}",
            ]

            for data in hover_data:
                text = self.font_mono.render(data, True, self.PANEL_TEXT)
                self.screen.blit(text, (panel_x + 20, y_offset))
                y_offset += 22

            y_offset += 20

        # Controls
        controls_title = self.font_medium.render("Controls:", True, self.HIGHLIGHT_COLOR)
        self.screen.blit(controls_title, (panel_x + 20, y_offset))
        y_offset += 30

        controls = [
            "SPACE - Run/Pause",
            "STEP  - Step Mode",
            "R     - Reset",
            "C     - Clear Grid",
            "S     - Set Start",
            "E     - Set End",
            "A     - Toggle Arrows",
            "+/-   - Speed",
            "LEFT  - Draw Walls",
            "RIGHT - Erase",
        ]

        for control in controls:
            text = self.font_small.render(control, True, self.PANEL_TEXT)
            self.screen.blit(text, (panel_x + 20, y_offset))
            y_offset += 20

        # Legend
        y_offset += 20
        legend_title = self.font_medium.render("Legend:", True, self.HIGHLIGHT_COLOR)
        self.screen.blit(legend_title, (panel_x + 20, y_offset))
        y_offset += 30

        legend_items = [
            ("Start", self.COLORS[CellType.START]),
            ("End", self.COLORS[CellType.END]),
            ("Obstacle", self.COLORS[CellType.OBSTACLE]),
            ("Open Set", self.COLORS[CellType.OPEN]),
            ("Closed Set", self.COLORS[CellType.CLOSED]),
            ("Path", self.COLORS[CellType.PATH]),
            ("Current", self.CURRENT_NODE_COLOR),
        ]

        for label, color in legend_items:
            # Color box
            box_rect = pygame.Rect(panel_x + 20, y_offset, 20, 15)
            pygame.draw.rect(self.screen, color, box_rect)
            pygame.draw.rect(self.screen, self.PANEL_TEXT, box_rect, 1)

            # Label
            text = self.font_small.render(label, True, self.PANEL_TEXT)
            self.screen.blit(text, (panel_x + 50, y_offset))
            y_offset += 22

    def update_visualization(self, open_set: Set[Tuple[int, int]],
                           closed_set: Set[Tuple[int, int]],
                           path: Optional[List[Tuple[int, int]]],
                           node_map: Dict[Tuple[int, int], Node],
                           current_node: Optional[Tuple[int, int]] = None):
        """Update visualization state"""
        self.open_set = open_set.copy()
        self.closed_set = closed_set.copy()
        self.node_map = node_map.copy()
        self.current_node = current_node

        if path:
            self.path = path
            self.path_animation_progress = len(path)

        self.draw_grid()
        self.draw_info_panel()
        pygame.display.flip()

        # Control animation speed
        if self.animation_speed > 0:
            pygame.time.wait(self.animation_speed)

        self.clock.tick(60)

    def run(self):
        """Main visualization loop with enhanced controls"""
        drawing_obstacle = False
        erasing = False
        setting_start = False
        setting_end = False

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Run A* algorithm
                        if self.grid.start and self.grid.end:
                            self._run_algorithm()

                    elif event.key == pygame.K_r:
                        # Reset visualization
                        self._reset_visualization()

                    elif event.key == pygame.K_c:
                        # Clear grid
                        self._clear_grid()

                    elif event.key == pygame.K_s:
                        # Toggle start point setting mode
                        setting_start = not setting_start
                        setting_end = False

                    elif event.key == pygame.K_e:
                        # Toggle end point setting mode
                        setting_end = not setting_end
                        setting_start = False

                    elif event.key == pygame.K_a:
                        # Toggle arrows
                        self.show_arrows = not self.show_arrows

                    elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                        # Increase speed (decrease delay)
                        self.animation_speed = max(0, self.animation_speed - 10)

                    elif event.key == pygame.K_MINUS:
                        # Decrease speed (increase delay)
                        self.animation_speed = min(500, self.animation_speed + 10)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        drawing_obstacle = True
                    elif event.button == 3:  # Right click
                        erasing = True

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        drawing_obstacle = False
                    elif event.button == 3:
                        erasing = False

                elif event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Update hovered cell
                    if mouse_x < self.grid_width:
                        grid_x = mouse_x // self.cell_size
                        grid_y = mouse_y // self.cell_size
                        pos = (grid_x, grid_y)

                        if self.grid.is_valid(pos):
                            self.hovered_cell = pos

                            # Handle drawing/erasing
                            if setting_start:
                                if self.grid.start:
                                    self.grid.set_cell(self.grid.start, CellType.EMPTY)
                                self.grid.start = pos
                                self.grid.set_cell(pos, CellType.START)
                                setting_start = False

                            elif setting_end:
                                if self.grid.end:
                                    self.grid.set_cell(self.grid.end, CellType.EMPTY)
                                self.grid.end = pos
                                self.grid.set_cell(pos, CellType.END)
                                setting_end = False

                            elif drawing_obstacle:
                                if pos != self.grid.start and pos != self.grid.end:
                                    self.grid.set_cell(pos, CellType.OBSTACLE)

                            elif erasing:
                                if pos != self.grid.start and pos != self.grid.end:
                                    self.grid.set_cell(pos, CellType.EMPTY)
                    else:
                        self.hovered_cell = None

            # Animate path if exists
            if self.path and self.path_animation_progress < len(self.path):
                self.path_animation_progress += 0.5

            self.draw_grid()
            self.draw_info_panel()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def _run_algorithm(self):
        """Execute A* algorithm with visualization"""
        self.stats.reset()
        self.open_set.clear()
        self.closed_set.clear()
        self.node_map.clear()
        self.path = None
        self.path_animation_progress = 0

        self.path = AStar.find_path(
            self.grid,
            self.grid.start,
            self.grid.end,
            self.update_visualization,
            self.stats
        )

        if self.path:
            # Animate path reveal
            for i in range(len(self.path)):
                self.path_animation_progress = i + 1
                self.draw_grid()
                self.draw_info_panel()
                pygame.display.flip()
                pygame.time.wait(50)

    def _reset_visualization(self):
        """Reset visualization state"""
        self.open_set.clear()
        self.closed_set.clear()
        self.node_map.clear()
        self.path = None
        self.path_animation_progress = 0
        self.stats.reset()

    def _clear_grid(self):
        """Clear entire grid"""
        self.grid.cells = [[CellType.EMPTY for _ in range(self.grid.width)]
                          for _ in range(self.grid.height)]
        self.grid.start = None
        self.grid.end = None
        self._reset_visualization()


def create_maze_pattern(grid: Grid):
    """Create an interesting maze pattern"""
    # Vertical walls with gaps
    for x in [8, 16, 24]:
        for y in range(grid.height):
            if y % 4 != 0:  # Leave gaps
                grid.set_cell((x, y), CellType.OBSTACLE)

    # Horizontal walls with gaps
    for y in [6, 12]:
        for x in range(grid.width):
            if x % 5 != 0:  # Leave gaps
                grid.set_cell((x, y), CellType.OBSTACLE)


def create_spiral_pattern(grid: Grid):
    """Create a spiral obstacle pattern"""
    cx, cy = grid.width // 2, grid.height // 2

    for radius in range(2, min(cx, cy), 3):
        for angle in range(0, 270, 5):
            rad = math.radians(angle)
            x = int(cx + radius * math.cos(rad))
            y = int(cy + radius * math.sin(rad))
            if grid.is_valid((x, y)):
                grid.set_cell((x, y), CellType.OBSTACLE)


def main():
    """Main entry point"""
    # Create grid (35x20 cells for better aspect ratio)
    grid = Grid(width=35, height=20)

    # Set default start and end positions
    grid.start = (2, 2)
    grid.end = (32, 17)
    grid.set_cell(grid.start, CellType.START)
    grid.set_cell(grid.end, CellType.END)

    # Create interesting obstacle pattern
    create_maze_pattern(grid)

    # Create visualizer and run
    visualizer = AdvancedVisualizer(grid, cell_size=35)

    print("=" * 80)
    print(" " * 20 + "A* PATHFINDING ALGORITHM")
    print(" " * 15 + "Advanced Visualization & Analysis")
    print("=" * 80)
    print("\n📋 CONTROLS:")
    print("  SPACE      - Run A* algorithm")
    print("  R          - Reset visualization (keep obstacles)")
    print("  C          - Clear entire grid")
    print("  S          - Set start point (hover over cell)")
    print("  E          - Set end point (hover over cell)")
    print("  A          - Toggle path arrows")
    print("  +/-        - Adjust animation speed")
    print("  LEFT DRAG  - Draw obstacles")
    print("  RIGHT DRAG - Erase obstacles")
    print("\n🎨 VISUALIZATION FEATURES:")
    print("  • Real-time f, g, h scores on nodes")
    print("  • Current exploration node highlighted in pink")
    print("  • Open set shown in blue (nodes to explore)")
    print("  • Closed set shown in gray (already explored)")
    print("  • Final path animated in gold with directional arrows")
    print("  • Hover over nodes to see detailed information")
    print("  • Live statistics panel with algorithm metrics")
    print("\n📊 ALGORITHM INSIGHTS:")
    print("  • f(n) = g(n) + h(n)  [Total estimated cost]")
    print("  • g(n) = Cost from start to current node")
    print("  • h(n) = Heuristic estimate to goal (Euclidean)")
    print("  • Explores nodes with lowest f-score first")
    print("  • Guarantees optimal path with admissible heuristic")
    print("=" * 80)
    print("\n🚀 Starting visualization...\n")

    visualizer.run()


if __name__ == "__main__":
    main()
