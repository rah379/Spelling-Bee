import nltk
from nltk.corpus import wordnet as wn
import game
import csv
import matplotlib.pyplot as plt
import numpy as np
import itertools
import string

data = list(csv.reader(open('src/data/letters.csv', newline = ''), delimiter = ' '))
solutions = list(csv.reader(open('src/data/solutions.csv', newline = ''), delimiter = ' '))

generated_games = list(csv.reader(open('src/data/out_bees.csv', newline = ''), delimiter = ' '))
generated_solutions = list(csv.reader(open('src/data/out_solns.csv', newline = ''), delimiter = ' '))

# This was used to generate out_bees.csv and out_solns.csv

def gen_games(big_set):
  pangrams = set()
  for word in big_set:
    chars = frozenset(word)
    if len(chars) == 7:
      pangrams.add(chars) # write chars to thing
  with open('src/data/out_bees.csv', 'w', newline = '') as new:
    spamwriter = csv.writer(new, delimiter = ' ')
    for elt in pangrams:
      for set_mid in elt:
        non_center = list(elt - frozenset(set_mid))
        spamwriter.writerow([set_mid] + non_center)
  games = list(csv.reader(open('src/data/out_bees.csv', newline = ''), delimiter = ' '))
  gen_sol = []
  for i in range(len(games)):
    solutions_here = []
    center = games[i][0]
    others = games[i][1:]
    gameset = set(center).union(set(others))
    for word in big_set:
      chars = set(word)
      if center in chars and chars.issubset(gameset):
        solutions_here.append(word)
    gen_sol.append(solutions_here)
  with open('src/data/out_solns.csv', 'w', newline = '') as solnCSV:
    spamwriter_solution = csv.writer(solnCSV, delimiter = ' ')
    for l in gen_sol:
      spamwriter_solution.writerow(l)

def plot_solution_info(inp_data, inp_solutions):
  num_games = len(inp_data)
  total_words_solutions = np.zeros(num_games)
  total_potential_points_dist = np.zeros(num_games)
  for i in range(0, num_games):
    total_words_solutions[i] = len(inp_solutions[i])
    total_potential_points_dist[i] = game.count_total_points(inp_solutions[i])
  fig, axs = plt.subplots(2)
  fig.suptitle('Distributions of # Solution Words and Total Potential Points')
  axs[0].hist(total_words_solutions, bins = 'auto', edgecolor = 'black', alpha = 0.7)
  axs[0].set_xlabel('Total Solution Words')
  axs[0].set_ylabel('Frequency')

  axs[1].hist(total_potential_points_dist, bins = 'auto', edgecolor = 'black', alpha = 0.7)
  axs[1].set_xlabel('Total Potential Points')
  axs[1].set_ylabel('Frequency')
  plt.show()

def eliminate_games():
  # Eliminate games with > 60 total solution words (or < 20)
  with open('src/data/fixed_bees.csv', 'w', newline = '') as newbees:
    with open('src/data/fixed_solutions.csv', 'w', newline = '') as newsolns:
      spamwriter_bee = csv.writer(newbees, delimiter = ' ')
      spamwriter_soln = csv.writer(newsolns, delimiter = ' ')
      for i in range(len(generated_solutions)):
        if 20 <= len(generated_solutions[i]) <= 60:
          spamwriter_bee.writerow(generated_games[i])
          spamwriter_soln.writerow(generated_solutions[i])

fixed_games = list(csv.reader(open('src/data/fixed_bees.csv', newline = ''), delimiter = ' '))
fixed_solutions = list(csv.reader(open('src/data/fixed_solutions.csv', newline = ''), delimiter = ' '))
# plot_solution_info(fixed_games, fixed_solutions)
# plot_solution_info(generated_games, generated_solutions) # -> plots already generated and saved

def plot_avg_points_per_word_length(inp_data, inp_solutions):
  buckets_a = np.zeros(20)
  buckets_b = np.zeros(20)
  for i in inp_solutions:
    this_game_buckets = np.zeros(20)
    this_game_nums = np.array([1] * 20)
    total_points = 0
    for word in i:
      idx = len(word)
      points = game.get_word_points(word)
      this_game_buckets[idx] += points
      total_points += points
      this_game_nums[idx] += 1
    this_game_buckets = this_game_buckets / total_points
    buckets_a += this_game_buckets
    buckets_b += np.divide(this_game_buckets, this_game_nums)
  buckets_a = buckets_a / len(inp_data)
  buckets_b = buckets_b / len(inp_data)
  x_axis = np.arange(0, 20)
  fig, axs = plt.subplots(2)
  axs[0].bar(x_axis, buckets_a)
  axs[1].bar(x_axis, buckets_b)
  axs[0].set_xticks(np.arange(0, 21, 1))
  axs[0].set_xlabel('Size of Word')
  axs[0].set_ylabel('Avg % of Potential Points From Length')
  fig.suptitle('Avg % of Points From Words, Total and Individual')
  axs[1].set_xticks(np.arange(0, 21, 1))
  axs[1].set_xlabel('Size of Word')
  axs[1].set_ylabel('Avg % of Potential Points Per Word of Length n')
  plt.show()

plot_avg_points_per_word_length(fixed_games, fixed_solutions) 