import json
import matplotlib.pyplot as plt


def plot_pathfinding_benchmark(json_file="dijkstra_astar.json"):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    metadata = data["metadata"]
    results = data["data"]

    # Extract sizes
    sizes = sorted(int(key.split("x")[0]) for key in results.keys())

    # Extract data for all three variants
    variants = ["horizontal", "diagonal", "center"]
    colors = {"dijkstra": "#d62728", "astar": "#1f77b4"}  # Red & Blue
    markers = {"dijkstra": "s", "astar": "o"}  # Square & Circle
    linestyles = {"dijkstra": "-", "astar": "--"}

    # Prepare figure: 1 row, 3 columns
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    for idx, variant in enumerate(variants):
        ax = axes[idx]

        # Dijkstra
        dijk_times = [results[f"{s}x{s}"][f"{variant}_dijkstra"] for s in sizes]
        # A*
        astar_times = [results[f"{s}x{s}"][f"{variant}_astar"] for s in sizes]

        ax.plot(
            sizes,
            dijk_times,
            marker=markers["dijkstra"],
            linestyle=linestyles["dijkstra"],
            color=colors["dijkstra"],
            label="Dijkstra",
            linewidth=2,
            markersize=6,
        )

        ax.plot(
            sizes,
            astar_times,
            marker=markers["astar"],
            linestyle=linestyles["astar"],
            color=colors["astar"],
            label="A*",
            linewidth=2,
            markersize=6,
        )

        ax.set_title(f"{variant.capitalize()} Path", fontsize=14, fontweight="bold")
        ax.set_xlabel("Grid Size (n x n)")
        ax.set_ylabel("Time (seconds)")
        if idx == 0:
            ax.set_ylabel("Time (seconds)")
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_xticks(sizes)
        ax.set_xticklabels([f"{s}×{s}" for s in sizes], rotation=45)

    # Main title
    plt.suptitle(
        "Pathfinding Performance: Dijkstra vs A*\n"
        f"Seed: {metadata['seed']} | Wall Prob: {metadata['wall_probability']} | "
        f"{metadata['trials_per_test']} trials avg | "
        f"Three Path Variants",
        fontsize=16,
        fontweight="bold",
        y=1.02,
    )

    plt.savefig("pathfinding_benchmark_3_variants.png", dpi=300, bbox_inches="tight")
    plt.show()

    print("Chart saved as 'pathfinding_benchmark_3_variants.png'")


if __name__ == "__main__":
    plot_pathfinding_benchmark()
