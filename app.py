import os
import time
from typing import Tuple, Any
from Graph import create_grid_graph, print_grid_graph
from algorithms import shortest_path


class App:
    GREEN = "\033[92m"  # Font Color - Bright green
    END = "\033[0m"  # Reset color

    def __init__(self) -> None:
        self.graph = None
        self.width = 0
        self.height = 0
        self.running = True

        self.main_menu = [
            "Generate New Grid",
            "Find Path",
            "Print Current Grid",
            "Exit",
        ]

    def clear_screen(self) -> None:
        """Clear screen windows/unix - cross-platform."""
        os.system("cls" if os.name == "nt" else "clear")

    def print_header(self) -> None:
        """Print header of app interface"""
        self.clear_screen()
        print(f"{self.GREEN}{'=' * 70}")
        print("GRID-BASED PATH-FINDING VISUALIZER".center(70))
        print("Dijkstra + A*".center(70))
        print("=" * 70)

    def display_main_menu(self) -> None:
        """Print App Main Menu"""
        print("Main Menu:")
        print("-" * 70)
        for i, item in enumerate(self.main_menu, 1):
            print(f"{i}. {item}")
        print("-" * 70)
        print("q - Quit")
        print("-" * 70)

    def display_algorithm_menu(self):
        """Print Algorithms  Sub-menu"""
        print("Choose Algorithm:")
        print("-" * 70)
        print("1. Dijkstra")
        print("2. A*")
        print("b - Back")
        print("q - Quit")
        print("-" * 70)

    def get_input(self, prompt: str, type_: type) -> Any:
        """Follow menu option or convert input to required type based on type_"""
        while True:
            value = input(f"{self.GREEN}{prompt}{self.END}").strip()
            if value.lower() == "q":
                self.running = False
                return None
            if value.lower() == "b":
                return "back"
            if value == "":
                print("enter correct value")
                self.get_input(prompt, type_)
            try:
                return type_(value)
            except ValueError:
                print(f"{self.GREEN}Invalid input. Try again.{self.END}")

    def generate_grid(self) -> None:
        """Form to gather grid generation arguments.
        To generate the same walls layout same values
        of seed and wall_probability"""
        print(f"{self.GREEN}\nGenerate New Grid")
        print("-" * 70)
        width = self.get_input("Enter width: ", int)

        height = self.get_input("Enter height: ", int)

        seed_input = self.get_input("Enter seed or press Enter for random: ", str)
        seed = int(seed_input) if seed_input else int(time.time())

        wall_prob = self.get_input(
            "Wall-removal probability (0.0-1.0, default 0.1): ", float
        )
        wall_prob = wall_prob if wall_prob is not None else 0.1

        print(f"\nGenerating {width}x{height} grid (seed={seed})")
        self.graph = create_grid_graph(
            width, height, seed=seed, wall_probability=wall_prob
        )
        self.width, self.height = width, height
        print("Grid generated!\n")

        # Print grid — temporarily disable color so grid looks clean
        print(f"{self.END}{' GRID PREVIEW '.center(70, '=')}")
        print_grid_graph(self.graph)
        print(f"{self.GREEN}{''.center(70, '=')}")

        input("\nPress Enter to continue ")

    def get_coordinates(self, prompt: str) -> Tuple[int, int] | None:
        """Form to gather coordinates arguments."""
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
        """Handle algorithm selection"""
        if not self.graph:
            print("No grid generated yet!")
            input("Press Enter  ")
            return

        while True:
            self.display_algorithm_menu()
            choice = self.get_input("Choose: ", str)
            if choice == "back":
                return
            if choice == "q":
                self.running = False
            algo = "dijkstra" if choice == "1" else "astar" if choice == "2" else None
            if algo:
                break
            print("Invalid choice!")
        print(f"{self.END}{' CURRENT GRID '.center(70, '=')}")
        print_grid_graph(self.graph)
        print(f"{self.GREEN}{''.center(70, '=')}")
        start = self.get_coordinates("Enter START coordinates:")
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
            path_coords = [c for c, _ in path_with_cost]

            print_grid_graph(self.graph, path_with_cost)
            print(f"{self.GREEN}{''.center(70, '=')}")
            print(f"\nPATH FOUND in {elapsed:.4f}s!")
            print(f"Length: {len(path_coords)} nodes | Cost: {total_cost:.2f}")

            print(f"\n{self.END}{' FINAL PATH '.center(70, '=')}")
            print(path_with_cost)
        input("\nPress Enter to continue ")

    def run(self):
        """Run application, self.running = False to exit."""
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
                    print(f"{self.END}{' CURRENT GRID '.center(70, '=')}")
                    print_grid_graph(self.graph)
                    print(f"{self.GREEN}{''.center(70, '=')}")
                else:
                    print("No grid to display!")
                input("\nPress Enter  ")
            elif choice.lower() == "q":
                print("\nThank you for using Path-finding Visualizer!")
                break
            else:
                print("Invalid choice!")
                time.sleep(1)


if __name__ == "__main__":
    app = App()
    app.run()
