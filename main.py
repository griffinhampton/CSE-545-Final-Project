import matplotlib.pyplot as plt
from pipes import loadFile, Grid, show_grid
from wisdomOfCrowds import WisdomOfCrowds
from geneticAlgo import GeneticAlgo

def run_single_ga(base_pipes, show_ga_progress=False, run_num = 0):
    ga = GeneticAlgo(base_pipes, visualize=show_ga_progress, vis_interval=100)
    best_grid = ga.run()
    if show_ga_progress:
        show_grid(best_grid, pause_time=0.3, title=f"Crowd Member #{run_num} Best (Cost: {ga.bestCost})")
    return [[str(p.pipe.to01()) for p in row] for row in best_grid.pipes]

if __name__ == "__main__":
    choice = input("Show live grid progress? (y/n): ").strip().lower()
    visualize = choice in ("y", "yes")

    if visualize:
        plt.ion()
    
    base_pipes = loadFile("tiles.txt")
    base_grid = Grid(base_pipes)
    
    run_counter = [0]
    def runner():
        run_counter[0] += 1
        return run_single_ga(base_grid, show_ga_progress=visualize, run_num=run_counter[0])
    
    woc = WisdomOfCrowds(ga_runner=runner,
                         runs=15,
                         agreement_threshold=0.80
                         )
    
    crowd = woc.collect_crowd()
    
    consensus_matrix, fixed_mask, stats = woc.aggregate_consensus(crowd)
    
    fixed_count = sum(sum(row) for row in fixed_mask)
    total_tiles = len(fixed_mask) * len(fixed_mask[0])
    print(f"\n[WoC Result] Locked {fixed_count}/{total_tiles} tiles with >= 80% crowd agreement.")
    
    final_grid = woc.build_grid_from_bitstrings(consensus_matrix)
    leaks, islands = final_grid.check_grid()
    total_leaks = sum(l[1] for l in leaks)
    print(f"Consensus Grid Score: {total_leaks} leaks, {islands} islands.")
    
    if visualize:
        plt.ioff()
        show_grid(final_grid, pause_time=0.1, title=f"Final WoC Consensus | Leaks: {total_leaks}, Islands: {islands}")
        plt.show()