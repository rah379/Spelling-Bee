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

def generate_bees():
  letters = list(string.ascii_lowercase)
  for i, first_letter in enumerate(letters):
    others = letters[:i] + letters[i + 1:]
    for combo in itertools.combinations(others, 6):
      yield [first_letter] + sorted(combo)


def generate_pangrams():
  pangram_set = set()
  sets_of_chars_seen = set()
  for syn in wn.all_synsets():
    for lemma in syn.lemma_names():
      if "_" in lemma:
        continue
      word = lemma.lower()
      if "-" in word or "'" in word:
        continue
      if not (4 <= len(word) <= 17):
        continue
      word_set = frozenset(word)
      if len(word_set) != 7:
        continue
      if word_set in sets_of_chars_seen:
        continue
      sets_of_chars_seen.add(word_set)
      pangram_set.add((word, word_set))
  return pangram_set

# p_set is a set of tuples (pangram, word_frozenset)
def filter_assumptions(p_set):
  out_set = set()
  vowel_set_no_y = set(('a', 'e', 'i', 'o', 'u'))
  for pangram, word_frozenset in p_set:
    # assumption 1: at least two vowels (no y)
    # assumption 2: no more than three vowels (with y)
    min_vowels = 0
    max_vowels = 0
    for char in word_frozenset:
      if char in vowel_set_no_y:
        min_vowels += 1
        max_vowels += 1
      if char == 'y':
        max_vowels += 1
    if min_vowels > 1 and max_vowels < 4:
      out_set.add((pangram, word_frozenset))
  return out_set

def generate_bees(p_set):
  with open('src/data/generated_bees.csv', 'w', newline = '') as csvfile_bee:
    with open('src/data/generated_bees_solutions.csv', 'w', newline = '') as csvfile_solutions:
      for pangram, word_frozenset in p_set:
        spamwriter_bee = csv.writer(csvfile_bee, delimiter = ' ')
        spamwriter_solution = csv.writer(csvfile_solutions, delimiter = ' ')
        word_list = list(word_frozenset)
        for i in range(0, 7):
          all_but_i = word_list[:i] + word_list[i + 1:]
          at_i = word_list[i]
          spamwriter_bee.writerow([at_i] + all_but_i) # write all seven solutions
          spamwriter_solution.writerow([pangram]) # write the pangram for each row


def fill_in_new_files():
  p_set = generate_pangrams()
  fit_assumptions = filter_assumptions(p_set)
  generate_bees(fit_assumptions)


# fill_in_new_files() -> only needs to be ran the once

generated_data = list(csv.reader(open('src/data/generated_bees.csv', newline = ''), delimiter = ' '))
generated_solutions = list(csv.reader(open('src/data/generated_bees_solutions.csv', newline = ''), delimiter = ' '))




# Filling in src/data/generated_bees_solutions.csv
# Build wordnet set of all possible solution words
def build_wordnet_set():
  word_set = set()
  for syn in wn.all_synsets():
    for lemma in syn.lemma_names():
      if "_" in lemma:
        continue
      word = lemma.lower()
      if "-" in word or "'" in word:
        continue
      if not (4 <= len(word) <= 19):
        continue
      if len(set(word)) > 7:
        continue
      word_set.add(word)
  return word_set


def fill_in_all_solutions(word_set):
  with open('src/data/generated_bees_solutions.csv', 'w', newline = '') as csvfile_solutions:
    for i in range(0, len(generated_data)):
      solution_words = [generated_solutions[i][0]] #pangrams first
      chars = generated_data[i]
      required = chars[0]
      allowed_letters = set(chars)
      for word in word_set:
        if (not set(word).issubset(allowed_letters)) or required not in word:
          continue
        solution_words.append(word)
      spamwriter = csv.writer(csvfile_solutions, delimiter = ' ')
      spamwriter.writerow(solution_words)


# word_set = build_wordnet_set()
# fill_in_all_solutions(word_set) -> only needed to do once, to fill src/data/generated_bees_solutions.csv


# Eliminating Elements of Dataset that are outrageous
def plot_num_solutions(generated_data, generated_solutions):
  num_games = len(generated_data)
  total_words_solutions = np.zeros(num_games)
  for i in range(0, num_games):
    total_words_solutions[i] = len(generated_solutions[i])
  plt.figure()
  plt.hist(total_words_solutions, bins = 'auto', edgecolor = 'black', alpha = 0.7)
  plt.title('Distribution of Number of Solution Words')
  plt.xlabel('Total Solution Words')
  plt.ylabel('Frequency')
  plt.show()

def eliminate_too_many():
  with open('src/data/out_solns.csv', 'w', newline = '') as res_one:
    with open('src/data/out_bees.csv', 'w', newline = '') as res_two:
      writer_one = csv.writer(res_one, delimiter = ' ')
      writer_two = csv.writer(res_two, delimiter = ' ')
      for i in range(0, len(generated_data)):
        if len(generated_solutions[i]) < 60:
          writer_one.writerow(generated_solutions[i])
          writer_two.writerow(generated_data[i])

# eliminate_too_many() -> only needed to be ran once

def eliminate_too_few():
  with open('src/data/out_solns.csv', 'w', newline = '') as res_one:
    with open('src/data/out_bees.csv', 'w', newline = '') as res_two:
      writer_one = csv.writer(res_one, delimiter = ' ')
      writer_two = csv.writer(res_two, delimiter = ' ')
      for i in range(0, len(generated_data)):
        if len(generated_solutions[i]) > 19:
          writer_one.writerow(generated_solutions[i])
          writer_two.writerow(generated_data[i])

# eliminate_too_few() -> only needed to be ran once

def eliminate_all_s():
  with open('src/data/out_solns.csv', 'w', newline = '') as res_one:
    with open('src/data/out_bees.csv', 'w', newline = '') as res_two:
      writer_one = csv.writer(res_one, delimiter = ' ')
      writer_two = csv.writer(res_two, delimiter = ' ')
      for i in range(0, len(generated_data)):
        if 's' not in generated_data[i]:
          writer_one.writerow(generated_solutions[i])
          writer_two.writerow(generated_data[i])

# eliminate_all_s()


# Point Analysis
# Distribution of Total Potential Points
def plot_pot_points_dist(inp_data, inp_solutions):
  num_games = len(inp_data)
  total_potential_points_dist = np.zeros(num_games)
  for i in range(0, num_games):
    total_potential_points_dist[i] = game.count_total_points(inp_solutions[i])
  plt.figure()
  plt.hist(total_potential_points_dist, bins = 'auto', edgecolor = 'black', alpha = 0.7)
  plt.title('Distribution of Total Potential Points')
  plt.xlabel('Total Potential Points')
  plt.ylabel('Frequency')
  plt.show()

# plot_pot_points_dist(generated_data, generated_solutions) # -> plot already generated and saved

def plot_avg_points_per_word_length(inp_data, inp_solutions):
  buckets = np.zeros(20)
  for i in inp_solutions:
    this_game_buckets = np.zeros(20)
    total_points = 0
    for word in i:
      idx = len(word)
      points = game.get_word_points(word)
      this_game_buckets[idx] += points
      total_points += points
    this_game_buckets = this_game_buckets / total_points
    buckets += this_game_buckets
  buckets = buckets / len(inp_data)
  x_axis = np.arange(0, 20)
  plt.figure()
  plt.bar(x_axis, buckets)
  plt.xticks(np.arange(0, 21, 1))
  plt.xlabel('Size of Word')
  plt.ylabel('Average Percent of Potential Points From Length')
  plt.title('Average Percent of Points Generated by Words of Each Length')
  plt.show()

# plot_avg_points_per_word_length(generated_data, generated_solutions) # -> plot already generated and saved

def plot_avg_points_per_word(inp_data, inp_solutions):
  buckets = np.zeros(20)
  for i in inp_solutions:
    this_game_points = np.zeros(20)
    this_game_nums = np.array([1] * 20)
    total_points  = 0
    for word in i:
      idx = len(word)
      points = game.get_word_points(word)
      this_game_points[idx] += points
      total_points += points
      this_game_nums[idx] += 1
    this_game_points = this_game_points / total_points 
    this_game_points = np.divide(this_game_points, this_game_nums)
    buckets += this_game_points
  buckets = buckets / len(inp_data)
  for i in range(0, 20):
    print("%i & %f \\" % (i, buckets[i]))
  x_axis = np.arange(0, 20)
  plt.figure()
  plt.bar(x_axis, buckets)
  plt.xticks(np.arange(0, 21, 1))
  plt.xlabel('Size of Word')
  plt.ylabel('Average Percent of Potential Points Per Word of Length n')
  plt.title('Average Percent of Points Generated by One Word of Each Length')
  plt.show()

plot_avg_points_per_word(generated_data, generated_solutions)








## ALL CODE BELOW IS FOR UNNECESSARY SECTION 3.2.1

# total_potential_points_dist = np.zeros(14)
# for i in range(0, 14):
#   total_potential_points_dist[i] = game.count_total_points(solutions[i])

# plt.figure()
# plt.hist(total_potential_points_dist, bins = 'auto', edgecolor = 'black', alpha = 0.7)
# plt.title('Distribution of Total Potential Points')
# plt.xlabel('Total Potential Points')
# plt.ylabel('Frequency')
# plt.show()




# freq_map = np.zeros(26)
# first_map = np.zeros(26)
# for i in range(0, 14):
#   for j in range(0, 7):
#     char = data[i][j]
#     idx = string.ascii_lowercase.index(char)
#     if j == 0:
#       first_map[idx] += 1
#     freq_map[idx] += 1

# x_axis = np.array(list(string.ascii_lowercase))
# total_letters = freq_map.sum()
# freq_map = freq_map / total_letters
# first_map = first_map / first_map.sum()
# real_values = [8.2, 1.5, 2.8, 4.3, 12.7, 2.2, 2.0, 6.1, 7.0, 0.15, 0.77, 4.0, 
#                         2.4, 6.7, 7.5, 1.9, 0.095, 6.0, 9.1, 
#                         2.8, 0.98, 2.4, 0.15, 2.0, 0.074]
# alphabet = list(string.ascii_lowercase)
# alphabet.remove('s')
# lst = freq_map.tolist()
# lst = lst[:18] + lst[19:]
# freq_alph_tuple = [(lst[i], alphabet[i]) for i in range(0, 25)]
# SEEN_sorted_by_freq = sorted(freq_alph_tuple, key = lambda x: x[0])

# value_alph_tuple = [(real_values[i], alphabet[i]) for i in range(0, 25)]
# REAL_sorted_by_freq = sorted(value_alph_tuple, key = lambda x:x[0])

# cmp_orders = [(REAL_sorted_by_freq[i][1], SEEN_sorted_by_freq[i][1]) for i in range(0, 25)]
# diff_order = []
# for i in range(0, 25):
#   real, seen = cmp_orders[i]
#   if real != seen:
#     diff_order.append((real, seen, i))

# print(diff_order)



# plt.bar(x_axis, freq_map, width = 0.8, color = 'b', label = 'Total Frequency')
# plt.bar(x_axis, first_map, width = 0.5, color = 'r', alpha = 0.5, 
#         label = 'Frequency being Center Character')
# # plt.bar(x_axis, real_values, width = 0.3, color = 'y', alpha = 0.3, label = 
# #         'Relative Frequency in Texts')


# plt.xlabel('Characters in data.csv')
# plt.ylabel('Frequencies')
# plt.title('Frequencies of Characters in data.csv')
# plt.legend()
# plt.show()

# h a g i l n t -> a, i
# i a d e h l p -> i, a, e
# f g i l n o r -> i, o
# n a e h p t y -> a, e, y
# t a b g l n o -> a, o
# v a d e n t u -> a, e
# m a c n o r y -> a, o, y
# w d h i l n o -> i, o
# t d e f o u x -> e, o, u
# f a e g i l n -> a, e, i
# a i m r t u y -> a, i, u
# l a c g i m y -> a, i
# v c e i n o t -> e, i, o
# l b g i m o r -> i, o

