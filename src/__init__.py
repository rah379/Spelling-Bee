import brute_force as bf
import dictionary_filter as df
import game as g
import matplotlib.pyplot as plt
import numpy as np
import csv

# - Ranks, in terms of percent of maximum total points: 
#0         Beginner: 0% -> discrete
#1         Good Start: 2% -> rounded UP
#2         Moving up: 5% -> rounded DOWN
#3         Good: 8% -> discrete
#4         Solid: 15% -> rounded UP 
#5         Nice: 25% -> rounded DOWN
#6         Great: 40% -> discrete
#7         Amazing: 50% -> rounded UP 
#8         Genius: 70% -> rounded DOWN (for some reason?)
#9         Queen Bee: 100% (ignore for the most part)

x_axis = np.array(['0', '2', '5', '8', '15', '25', '40', '50', '70'])
data = list(csv.reader(open('src/data/letters.csv', newline = ''), delimiter = ' '))
solutions = list(csv.reader(open('src/data/solutions.csv', newline = ''), delimiter = ' '))

def plot_sep(stacks, alg_name, colors):
  fig, axs = plt.subplots(2, 2, sharex = True)
  if len(alg_name) == 1:
    fig.suptitle(alg_name[0] + ' Statistics')
  else:
    fig.suptitle('Multiple Model Statistics')
  for i in range(0, len(stacks)):
    stack = stacks[i]
    label_i = alg_name[i]
    color_i = colors[i]
    axs[1, 0].set_xlabel('Ranks (% of Total Points Needed)')
    axs[1, 1].set_xlabel('Ranks (% of Total Points Needed)')
    axs[0, 0].plot(x_axis, stack[0], color = color_i, label = label_i)
    axs[0, 0].set_title('Average Word Length')
    axs[0, 0].set_ylabel('Average # of Characters')


    axs[0, 1].plot(x_axis, stack[1], color = color_i, label = label_i)
    axs[0, 1].set_title('Average Number of Words Needed')
    axs[0, 1].set_ylabel('Number of Words')

    axs[1, 0].plot(x_axis, stack[3], color = color_i, label = label_i)
    axs[1, 0].set_title('Average Time Taken')
    axs[1, 0].set_ylabel('Seconds')

    axs[1, 1].plot(x_axis, stack[2], color = color_i, label = label_i)
    axs[1, 1].set_title('Average Points Earned')
    axs[1, 1].set_ylabel('Points')
  for ax in axs.flat:
    ax.legend()
  plt.show()



def benchmark_bf(bf_alg, data, solution, priority = None):
  time_vals = np.zeros(9)
  point_vals = np.zeros(9)
  avg_word_length = np.zeros(9)
  avg_words_used = np.zeros(9)
  for i in range(0, len(data)):
    game = data[i]
    solns = solution[i]
    for r in range(1, 9):
      words, point_val, time_val = g.use_bf(bf_alg, game, solns, r, priority)
      point_vals[r] += point_val
      time_vals[r] += time_val
      num_words = len(words)
      avg_words_used[r] += num_words
      word_lengths = [len(w) for w in words]
      avg_word_length[r] += sum(word_lengths) / num_words

  return np.stack((avg_word_length / len(data), avg_words_used / len(data), 
                    point_vals / len(data), time_vals / len(data)))
  

def plot_bf_differences():
  naive_bf_stack = benchmark_bf(bf.naive_bf, data, solutions)
  length_priority = [6, 5, 7, 4, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
  optimized_bf_stack = benchmark_bf(bf.optimized_bf, data, solutions, length_priority)
  both_stacks = [naive_bf_stack, optimized_bf_stack]
  titles = ['Naive BF', 'Optimized BF']
  color_lst = ['b', 'r']
  plot_sep(both_stacks, titles, color_lst)


def benchmark_df(df_alg, data, solution, precompute, dicts):
  time_vals = np.zeros(9)
  point_vals = np.zeros(9)
  avg_word_length = np.zeros(9)
  avg_words_used = np.zeros(9)
  for i in range(0, len(data)):
    game = data[i]
    solns = solution[i]
    for r in range(1, 9):
      words, point_val, time_val = g.use_df(df_alg, game, solns, r, precompute, dicts[i])
      point_vals[r] += point_val
      time_vals[r] += time_val
      num_words = len(words)
      avg_words_used[r] += num_words
      word_lengths = [len(w) for w in words]
      avg_word_length[r] += sum(word_lengths) / num_words
  return np.stack((avg_word_length / len(data), avg_words_used / len(data), 
                    point_vals / len(data), time_vals / len(data)))

precomputations = [0, 1, 2, 3, 4]
zero_dicts = [None] * len(data)
one_dicts = []
two_dicts = []
three_dicts = []
four_dicts = []
def do_all_precomps():
  for i in data:
    one_dicts.append(df.build_dict(1, i))
    two_dicts.append(df.build_dict(2, i))
    three_dicts.append(df.build_dict(3, i))
    four_dicts.append(df.build_dict(4, i))
def plot_naive_precomps():
  s0 = benchmark_df(df.naive_df_prime, data, solutions, 0, zero_dicts)
  s1 = benchmark_df(df.naive_df_prime, data, solutions, 1, one_dicts)
  s2 = benchmark_df(df.naive_df_prime, data, solutions, 2, two_dicts)
  s3 = benchmark_df(df.naive_df_prime, data, solutions, 3, three_dicts)
  s4 = benchmark_df(df.naive_df_prime, data, solutions, 4, four_dicts)
  all_stacks = [s0, s1, s2, s3, s4]
  titles = ['Naive w/ Precomp 0', 'Naive w/ Precomp 1', 'Naive w/ Precomp 2', 
            'Naive w/ Precomp 3', 'Naive w/ Precomp 4']
  color_lst = ['b', 'r', 'g', 'm', 'y']
  plot_sep(all_stacks, titles, color_lst)


# All Plots: 
# s = benchmark_bf(bf.naive_bf, data, solutions)
# plot_sep([s], ['Naive Brute Force'], ['b'])
plot_bf_differences()
# plot_naive_precomps()