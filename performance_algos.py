import cProfile
import gc
import time
import tracemalloc
from Graph import create_grid_graph
from algorithms import shortest_path


SIZES = [500, 600, 700, 800, 900]
TRIALS = 5
SEED = 42
WALL_PROB = 0.10

ALGOS = ("dijkstra", "astar")


def get_test_cases(width: int, height: int):
    """Define standard path-finding test variants"""
    return [
        ("horizontal", (0, height // 2), (width - 1, height // 2)),
        ("diagonal",   (0, 0),         (width - 1, height - 1)),
        ("center",   (0, height-1),         (width//2, height//2)),
    ]


def benchmark_pathfinding():
    print("=" * 90)
    print("PATH-FINDING ALGORITHMS BENCHMARK".center(90))
    print(f"{'Size':>10} | {'Variant':>12} | {'Dijkstra':>15} | {'A*':>15} | {'A* Speedup':>12}")
    print("-" * 90)

    for size in SIZES:
        width = height = size
        print(f"\nBenchmarking {width}x{height} grid")
        
        graph = create_grid_graph(width, height, seed=SEED, wall_probability=WALL_PROB)

        for variant_name, start, goal in get_test_cases(width, height):
            print(f"  Variant: {variant_name}")

            results = {}

            for algo in ALGOS:
                times = []
                peaks = []

                for trial in range(TRIALS):
                    gc.collect()
                    tracemalloc.start()

                    profiler = cProfile.Profile()
                    profiler.enable()

                    t0 = time.perf_counter()
                    shortest_path(graph, start, goal, algorithm=algo)
                    elapsed = time.perf_counter() - t0

                    profiler.disable()
                    _, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()

                    times.append(elapsed)
                    peaks.append(peak)

                    # Save profile only for first trial
                    if trial == 0:
                        profile_file = f"profile_{algo}_{size}_{variant_name}.prof"
                        profiler.dump_stats(profile_file)

                avg_time = sum(times) / TRIALS
                avg_peak_mb = sum(peaks) / TRIALS / 1e6

                results[algo] = {"time": avg_time, "memory_mb": avg_peak_mb}

                print(f"    {algo:9}: {avg_time:>8.4f}s | {avg_peak_mb:>6.1f} MB")

            # Speedup
            d_time = results["dijkstra"]["time"]
            a_time = results["astar"]["time"]
            speedup = d_time / a_time if a_time > 0 else float('inf')

            print(f"    -> A* speedup: {speedup:>6.2f}x")

        del graph
        gc.collect()

    print("\n" + "=" * 90)
    print("BENCHMARK COMPLETE".center(90))
    print("Detailed profiles saved as: profile_<algo>_<size>_<variant>_1.prof")
    print("=" * 90)


if __name__ == "__main__":
    benchmark_pathfinding()
    
    #stats = pstats.Stats("profile_astar_1000_horizontal.prof")
    #print('A*')
    #stats.strip_dirs().print_stats(10)
    #stats = pstats.Stats("profile_dijkstra_1000_horizontal.prof")
    #print('dijkstra')
    #stats.strip_dirs().print_stats(10)
    