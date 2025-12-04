import json
import time
import gc
from datetime import datetime
from Graph import create_grid_graph
from algorithms import shortest_path


SIZES = [10, 50, 100, 200, 500, 1000]  # Graph size
TRIALS = 20       # Number of benchmarks
SEED = 42         # Graph layout
WALL_PROB = 0.10  # Wall removal probability
ALGOS = (
    "dijkstra",
    "astar",
    )

def get_test_cases(width: int, height: int):
    """horizontal and diagonal start and goal vertices"""
    return [
        ("horizontal", (0, height // 2), (width - 1, height // 2)),
        ("diagonal",   (0, 0),         (width - 1, height - 1)),
    ]

def benchmark_running_times():
    results = {
        "metadata": {
            "date": datetime.now().isoformat(),
            "description": "Pathfinding running times (SECONDS)",
            "seed": SEED,
            "wall_probability": WALL_PROB,
            "trials_per_test": TRIALS,
            "variants": ["horizontal", "diagonal"]
        },
        "data": {}
    }

    print("=" * 80)
    print("PATH-FINDING ALGORITHMS BENCHMARK".center(80))
    print("=" * 80)

    for size in SIZES:
        width = height = size
        print(f"\nBenchmarking {width}x{height} grid")

        graph = create_grid_graph(width, height, seed=SEED, wall_probability=WALL_PROB)
        results["data"][f"{size}x{size}"] = {}

        for variant_name, start, goal in get_test_cases(width, height):
            print(f"  {variant_name:12} | Start {start} -> Goal {goal}")

            times = {algo:[] for algo in ALGOS}

            for algo in ALGOS:
                for _ in range(TRIALS):
                    t0 = time.perf_counter()
                    
                    elapsed = time.perf_counter() - t0

                    times[algo].append(elapsed)

                avg_time = sum(times[algo]) / TRIALS
                results["data"][f"{size}x{size}"][f"{variant_name}_{algo}"] = round(avg_time, 6)

                print(f"    {algo:9}: {avg_time:>8.5f} s (avg over {TRIALS} runs)")

        del graph
        gc.collect()

    # Save to JSON
    with open("dijkstra_astar.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print("\n" + "=" * 80)
    print("BENCHMARK COMPLETE - Results saved to running_times.json".center(80))
    print("=" * 80)

    return results

if __name__ == "__main__":
    benchmark_running_times()
