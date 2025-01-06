import brute_force as bf
import dictionary_filter as df
import greedy
import TrieNode as tn
import game
import matplotlib.pyplot as plt
import numpy as np

data = game.data
solutions = game.solutions
n = 9
ranks_percentages = [0, 2, 5, 8, 15, 25, 40, 50, 70, 100]
x_axis = np.array(ranks_percentages[0:n])


def run_on_all(heuristic, n):
  points_avg = np.zeros(n)
  times_avg = np.zeros(n)
  for i in range(0, 14):
    chars = data[i]
    solns = solutions[i]
    w, p, t = game.get_alg_solutions(heuristic, chars, solns, n)
    p_arr = np.array(p)
    t_arr = np.array(t)
    points_avg += p
    times_avg += t
  points_avg *= 1/15
  times_avg *= 1/15
  return points_avg, times_avg



# First method: Brute Forcing (the code below works)
# bf_points, bf_times = run_on_all(bf.brute_force_dprime, n)
# fig, ax = plt.subplots()
# ax.plot(x_axis, bf_times)
# ax.set(xlabel = 'Rank (percent of max possible)', ylabel = 'Time (s)', 
#        title = 'Brute Force')
# ax.grid()
# plt.show()


# Second method: Straight Dictionary Filtering
points_df, times_df = run_on_all(df.stop_at_success, n)
fig, ax = plt.subplots()
ax.plot(x_axis, times_df)
ax.set(xlabel = 'Rank (percent of max possible)', ylabel = 'Time (s)', 
       title = 'Dictionary Filtering')
ax.grid()
plt.show()