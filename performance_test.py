import cProfile
import time
import tracemalloc
import gc
import pstats


from two_dim_graph import  create_grid_graph as create_heavy_graph
from Graph import create_grid_graph as create_light_graph


SIZES = [
    (100, 100),
    (500, 500),
    (1000, 1000),
    (2000, 2000),
    # (5000, 5000)
]

def benchmark():
    print("GRID CREATION BENCHMARK".center(80, "="))
    print(f"{'Size':>12} | {'2D List':>15} | {'1D List':>15} | {'Speedup':>10}")
    print("-" * 80)

    for w, h in SIZES:
        print(f"\nTesting Graph{w}×{h}", end="")
        gc.collect()
        # --- Heavy Graph ---
        tracemalloc.start()
        start = time.perf_counter()
        stats_heavy = cProfile.runctx(
            'create_heavy_graph(w, h)',
            globals(),
            locals(),
            filename=f'stats_2d_list{w}.prof',
            sort='cumulative'
        )
        time_heavy = time.perf_counter() - start
        current, peak_heavy = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        gc.collect()
        # --- Light Graph ---
        tracemalloc.start()
        start = time.perf_counter()
        stats_light = cProfile.runctx(
            'create_light_graph(w, h, seed=42)',
            globals(),
            locals(),
            filename=f'stats_1d_list{w}.prof',
            sort='cumulative'
        )
        time_light = time.perf_counter() - start
        _, peak_light = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        speedup = time_heavy / time_light if time_light > 0 else float('inf')

        print(f"\n{w:>6}×{h:<6} | {time_heavy:>8.3f}s | {time_light:>8.3f}s | {speedup:>8.1f}×")
        print(f"{'':>13} |{peak_heavy/1e6:>8.1f} MB|{peak_light/1e6:>8.1f} MB|")





if __name__ == '__main__':

    #benchmark()
    stats = pstats.Stats("stats_2d_list{w}.prof")
    print('A*')
    stats.strip_dirs().print_stats(10)
    stats = pstats.Stats("stats_1d_list{w}.prof")
    print('dijkstra')
    stats.strip_dirs().print_stats(10)
