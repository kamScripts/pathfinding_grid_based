import os
import time
from typing import Any, Tuple

from algorithms import shortest_path
from Graph import Graph, create_grid_graph, print_grid_graph


class App:
    """
    A terminal-based interactive path=finding visualizer supporting Dijkstra's algorithm
    and A* with Manhattan distance heuristic on weighted grid graphs.

    Features:
        - Random grid generation with configurable size, seed, and wall probability
        - Visual representation of grid, walls, weights, and found paths
        - Interactive menu system with safe input handling
        - Consistent layout and colorized output
        - Reproducible layouts via fixed seed

    Limitations:
        - Grid width should not exceed ~50-60 cells for proper terminal display
        - Grid height should be ≤ 100 to avoid scrolling issues
        - Weights are randomly assigned (1-9) during grid creation
    """

    # CONSTANTS
    GREEN: str = "\033[92m"  # Font Color - Bright green

    END: str = "\033[0m"  # Reset color
    DOT: str = "\u25cf"  # Large dot
    ARR0W: str = "\u2192"
    SPACE: int = 70  # menu width
    SPACER_1: str = "=" * SPACE  # spacer type 1
    SPACER_2: str = "-" * SPACE  # spacer type 2
    MAIN_MENU: list[str] = [  # menu options
        "Generate New Grid ",
        "Find Path         ",
        "Print Current Grid",
    ]
    ALGO_MENU: list[str] = [  # algorithms menu
        "Choose Algorithm:",
        "Dijkstra",
        "A* (Manhattan distance)",
        f"b {ARR0W} Back",
        f"q {ARR0W} Quit",
    ]
    HEADER: list[str] = [  # header content
        "GRID-BASED PATH-FINDING VISUALIZER",
        f"{DOT} Dijkstra {DOT}",
        f"{DOT}    A*    {DOT}",
    ]

    def __init__(self) -> None:
        """Initialize the application with a 20x10 grid and 80% wall occurrence probability."""
        self.graph: Graph = create_grid_graph(
            20, 10, wall_probability=0.2
        )  # initial grid
        self.width: int = 20
        self.height: int = 10
        self.running: bool = True  # Close App

    def clear_screen(self) -> None:
        """Clear screen cross-platform independently ."""
        os.system("cls" if os.name == "nt" else "clear")

    def print_header(self) -> None:
        """Display the application header with formatting."""
        self.clear_screen()
        print(f"{self.GREEN}" + self.SPACER_2)
        for line in self.HEADER:
            print(f"{line.center(self.SPACE)}")
        print(self.SPACER_2)

    def display_main_menu(self) -> None:
        """Display the centered main menu with ordered options."""
        print(f"{self.GREEN}{'Main Menu:'.center(self.SPACE)}")
        print(self.SPACER_2)

        for i, item in enumerate(self.MAIN_MENU):
            print(f"{f'{i + 1} {self.ARR0W} {item}'.center(self.SPACE)}")
        print(self.SPACER_2)
        print(f"{('q ' + self.ARR0W + ' Quit').center(self.SPACE)}")
        print(self.SPACER_2)

    def display_algorithm_menu(self) -> None:
        """Show algorithm selection menu."""
        print(f"{self.SPACER_2.center(self.SPACE)}")
        for line in self.ALGO_MENU:
            print(f"{self.GREEN}{line.center(self.SPACE)}{self.END}")

    def get_input(self, prompt: str, type_: type) -> Any:
        """Quit or convert input to required type based on  parameter (type_)."""
        while True:
            value = input(f"{self.GREEN}{prompt}{self.END}").strip()
            if value.lower() == "q":
                self.running = False
                return None
            if value == "":
                return None
            try:
                return type_(value)
            except ValueError:
                print(f"{self.GREEN}Invalid input. Try again.{self.END}")

    def generate_grid(self) -> None:
        """Interactive form to generate a new grid with user-defined parameters."""
        print(f"{self.GREEN}\nGenerate New Grid")
        print(self.SPACER_2)

        width: int = self.get_input("Enter width: ", int)
        height: int = self.get_input("Enter height: ", int)
        seed_input: str = self.get_input("Enter seed or press Enter for random: ", str)
        seed = int(seed_input) if seed_input else int(time.time())
        wall_prob: float = self.get_input(
            "Wall-removal probability (0.0-1.0, default 0.1): ", float
        )
        wall_prob = wall_prob if wall_prob is not None else 0.1

        print(f"\nGenerating {width}x{height} grid (seed={seed})")
        self.graph = create_grid_graph(
            width, height, seed=seed, wall_probability=wall_prob
        )
        self.width, self.height = width, height

        print(f"{' GRID PREVIEW '.center((width * 4 + 1), '=')}")
        print_grid_graph(self.graph)
        print(f"{''.center((width * 4 + 1), '=')}")

        input(f"\n{self.GREEN}Press Enter to continue ")

    def get_coordinates(self, prompt: str) -> Tuple[int, int] | None:
        """Prompt user for grid coordinates with bounds checking."""
        print(prompt)
        x = self.get_input("  X coordinate: ", int)
        if not self.running:
            return None
        y = self.get_input("  Y coordinate: ", int)
        if not self.running:
            return None

        if not (0 <= x < self.width and 0 <= y < self.height):
            print(f"Out of bounds! Must be 0-{self.width - 1}, 0-{self.height - 1}")
            return None
        return (x, y)

    def find_path(self) -> None:
        """Main path-finding workflow: select algorithm -> choose start/goal -> run -> display result."""
        if not self.graph:
            print("No grid generated yet!")
            input("Press Enter  ")
            return

        while True:  # choice == b | choice == q -> exit loop.
            self.display_algorithm_menu()
            choice = self.get_input("Choose: ", str)
            if choice == "b":
                return
            if choice == "q":
                self.running = False
            algo = "dijkstra" if choice == "1" else "astar" if choice == "2" else None
            if algo:
                break
            print("Invalid choice!")
        print(f"{self.END}{' CURRENT GRID '.center((self.width * 4 + 1), '=')}")
        print_grid_graph(self.graph)
        print(f"{''.center((self.width * 4 + 1), '=')}")
        start = self.get_coordinates(f"{self.GREEN}Enter START coordinates:")
        if not start:
            return
        goal = self.get_coordinates("Enter GOAL coordinates:")
        if not goal:
            return

        print(f"\nRunning {algo.upper()} from {start} -> {goal}")
        t0 = time.perf_counter()
        path_with_cost, total_cost = shortest_path(
            self.graph, start, goal, algorithm=algo
        )
        elapsed = time.perf_counter() - t0

        if path_with_cost is None:
            print("No path found!")
        else:
            print_grid_graph(self.graph, path_with_cost)
            print(f"{self.GREEN}{''.center((self.width * 4 + 1), '=')}")
            print(f"\nPATH FOUND in {elapsed:.4f}s!")
            print(f"Length: {len(path_with_cost)} nodes | Cost: {total_cost:.2f}")

            print(f"\n{self.END}{' FINAL PATH '.center(self.SPACE, '=')}")
            print(path_with_cost)
        input("\nPress Enter to continue ")

    def run(self):
        """Start the main application loop."""
        while self.running:
            self.print_header()
            self.display_main_menu()

            choice = self.get_input("Choose option: ", str)
            if not self.running:
                break

            if choice == "1":
                self.generate_grid()
            elif choice == "2":
                self.find_path()
            elif choice == "3":
                if self.graph:
                    print(
                        f"{self.END}{' CURRENT GRID '.center((self.width * 4 + 1), '=')}"
                    )
                    print_grid_graph(self.graph)
                    print(f"{''.center((self.width * 4 + 1), '=')}")
                else:
                    print("No grid to display!")
                input(f"\n{self.GREEN}Press Enter  ")
            elif choice.lower() == "q":
                print("\nThank you for using Path-finding Visualizer!")
                break
            else:
                print("Invalid choice!")
                time.sleep(1)


if __name__ == "__main__":
    app = App()
    app.run()
