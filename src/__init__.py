import brute_force as bf
import dictionary_filter as df
import greedy
import TrieNode as tn
import game
import matplotlib.pyplot as plt
import numpy as np

data = game.data
solutions = game.solutions
n = 9 # 'genius' score
ranks_percentages = [0, 2, 5, 8, 15, 25, 40, 50, 70, 100]
x_axis = np.array(ranks_percentages[0:n])


def run_on_all(heuristic, n, trie = False, greedy = False, precompute = False, DFS = False):
  points_avg = np.zeros(n)
  times_avg = np.zeros(n)
  for i in range(0, 14):
    chars = data[i]
    solns = solutions[i]
    if not trie and not greedy:
      w, p, t = game.get_alg_solutions(heuristic, chars, solns, n)
    elif trie and not greedy:
      w, p, t = game.get_alg_solutions(heuristic, chars, solns, n, True, greedy, precompute, DFS)
    else:
      w, p, t = game.get_alg_solutions(heuristic, chars, solns, n, False, greedy, precompute)
    p_arr = np.array(p)
    t_arr = np.array(t)
    points_avg += p
    times_avg += t
  points_avg *= 1/15
  times_avg *= 1/15
  return points_avg, times_avg



# First method: Brute Forcing (the code below works)
bf_points, bf_times = run_on_all(bf.brute_force_dprime, n)

# Second method: Straight Dictionary Filtering
points_df, times_df = run_on_all(df.stop_at_success, n)

# Third method(s): Trie Node
# 3a: Don't Precompute Trie, DFS:
no_prec_dfs_points, no_prec_dfs_times = run_on_all(tn.trieAlg, 
                                                  n, trie = True, 
                                                  precompute = False, 
                                                  DFS = True)
# 3b: Don't Precompute Trie, BFS:
no_prec_bfs_points, no_prec_bfs_times = run_on_all(tn.trieAlg, 
                                                  n, trie = True,
                                                  precompute = False,
                                                  DFS = False)
# 3c: Precompute, DFS: 
prec_dfs_points, prec_dfs_times = run_on_all(tn.trieAlg, 
                                                  n, trie = True, 
                                                  precompute = True, 
                                                  DFS = True)
# 3d: Precompute, BFS:
prec_bfs_points, prec_bfs_times = run_on_all(tn.trieAlg, 
                                                  n, trie = True,
                                                  precompute = True,
                                                  DFS = False)


# Fourth method(s): Greedy Dictionary
# 4a: Don't precompute filtered dictionary:
no_prec_greedy_pts, no_prec_greedy_times = run_on_all(greedy.greedy_alg, n,
                                                      trie = False,
                                                      greedy = True)

# 4b: precompute filtered dictionary: 
prec_greedy_pts, prec_greedy_times = run_on_all(greedy.greedy_alg, n, 
                                                trie = False, greedy = True,
                                                precompute = True)







plt.plot(x_axis, bf_times, color = 'r', label = 'Brute Force')
plt.plot(x_axis, times_df, color = 'b', label = 'Dictionary Filtering')
plt.plot(x_axis, no_prec_dfs_times, color = 'g', label = 'No Precompute DFS Trie')
plt.plot(x_axis, no_prec_bfs_times, color = 'c', label = 'No Precompute BFS Trie')
plt.plot(x_axis, prec_dfs_times, color = 'm', label = 'Precompute DFS Trie')
plt.plot(x_axis, prec_bfs_times, color = 'y', label = 'Precompute BFS Trie')
plt.plot(x_axis, no_prec_greedy_times, color = 'k', label = 'No Precompute Greedy')
plt.plot(x_axis, prec_greedy_times, color = 'tab:orange', label = 'Precompute Greedy')
plt.xlabel("Rank (Percentage of Max Possible Points)")
plt.ylabel("Time (s)")
plt.title("Comparing Solving Method Times")
plt.legend()
plt.show()
