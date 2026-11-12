import matplotlib.pyplot as plt
from pipes import loadFile, Grid, show_grid, select_file
from wisdomOfCrowds import WisdomOfCrowds
from geneticAlgo import GeneticAlgo

'''
CSE-545 final project

Team members: Logan Rolfes, Griffin Hampton, and Sophia Reynolds
'''

def prompt_int(prompt_text, default, min_val=1):
    while True:
        raw = input(f"{prompt_text} [{default}]: ").strip()
        if raw == "":
            return default
        if raw.isdigit() and int(raw) >= min_val:
            return int(raw)
        print(f"Please enter an integer >= {min_val}.")

def prompt_float(prompt_text, default, min_val=0.0, max_val=1.0):
    while True:
        raw = input(f"{prompt_text} [{default}]: ").strip()
        if raw == "":
            return default
        try:
            val = float(raw)
            if min_val <= val <= max_val:
                return val
        except ValueError:
            pass
        print(f"Please enter a number between {min_val} and {max_val}.")

def prompt_bool(prompt_text, default=False):
    hint = "Y/n" if default else "y/N"
    raw = input(f"{prompt_text} ({hint}): ").strip().lower()
    if raw == "":
        return default
    return raw in ("y", "yes")

def configure_settings():
    print("\n=== Pipe Puzzle GA + Wisdom of Crowds ===")
    selected_file = select_file()
    if selected_file is None:
        return None

    print("\n--- Settings (press Enter for defaults) ---")
    settings = {
        "file_path": str(selected_file),
        "runs": prompt_int("Crowd size (number of GA runs)", default=15, min_val=1),
        "agreement_threshold": prompt_float("WoC agreement threshold (0.0 - 1.0)", default=0.80, min_val=0.0, max_val=1.0),
        "pop_size": prompt_int("GA population size", default=100, min_val=1),
        "generations": prompt_int("GA max generations per run", default=5000, min_val=1),
        "mutation_rate": prompt_float("GA mutation rate (0.0 - 1.0)", default=0.10, min_val=0.0, max_val=1.0),
        "visualize": prompt_bool("Show live grid progress?", default=False),
    }

    if settings["visualize"]:
        settings["vis_interval"] = prompt_int("Render update interval (generations)", default=100, min_val=1)
    else:
        settings["vis_interval"] = 100

    return settings

def run_single_ga(base_pipes, settings, run_num=0):
    ga = GeneticAlgo(
        base_pipes,
        popSize=settings["pop_size"],
        mutationRate=settings["mutation_rate"],
        generations=settings["generations"],
        visualize=settings["visualize"],
        vis_interval=settings["vis_interval"]
    )
    best_grid = ga.run()
    if settings["visualize"]:
        show_grid(best_grid, pause_time=0.3, title=f"Crowd Member #{run_num} Best (Cost: {ga.bestCost})")
    return [[str(p.pipe.to01()) for p in row] for row in best_grid.pipes]

if __name__ == "__main__":
    settings = configure_settings()
    if settings is None:
        exit(1)

    visualize = settings["visualize"]
    if visualize:
        plt.ion()

    base_pipes = loadFile(settings["file_path"])
    base_grid = Grid(base_pipes)

    run_counter = [0]
    def runner():
        run_counter[0] += 1
        print(f"\n--- Running Crowd Member {run_counter[0]}/{settings['runs']} ---")
        return run_single_ga(base_grid, settings, run_num=run_counter[0])

    woc = WisdomOfCrowds(
        ga_runner=runner,
        runs=settings["runs"],
        agreement_threshold=settings["agreement_threshold"]
    )

    crowd = woc.collect_crowd()

    #added score, best_member, and if statement to overcome a misinformed consensus vote
    def score(bits):
        leaks, islands = woc.build_grid_from_bitstrings(bits).check_grid()
        return sum(l[1] for l in leaks) + 2 * (islands - 1)

    best_member = min(crowd, key=score)

    if score(best_member) == 0:
        print("\n[WoC] A crowd member solved it; using that solution directly.")
        final_bits = best_member
    else:
        consensus_matrix, fixed_mask, stats = woc.aggregate_consensus(crowd)
        # ...existing locked-tiles print...
        final_bits = consensus_matrix if score(consensus_matrix) <= score(best_member) else best_member

    final_grid = woc.build_grid_from_bitstrings(final_bits)

    consensus_matrix, fixed_mask, stats = woc.aggregate_consensus(crowd)

    fixed_count = sum(sum(row) for row in fixed_mask)
    total_tiles = len(fixed_mask) * len(fixed_mask[0])
    pct = int(settings["agreement_threshold"] * 100)
    print(f"\n[WoC Result] Locked {fixed_count}/{total_tiles} tiles with >= {pct}% crowd agreement.")

    final_grid = woc.build_grid_from_bitstrings(consensus_matrix)
    leaks, islands = final_grid.check_grid()
    total_leaks = sum(l[1] for l in leaks)
    print(f"Consensus Grid Score: {total_leaks} leaks, {islands} islands.")

    if visualize:
        plt.ioff()
        show_grid(final_grid, pause_time=0.1, title=f"Final WoC Consensus | Leaks: {total_leaks}, Islands: {islands}")
        plt.show()