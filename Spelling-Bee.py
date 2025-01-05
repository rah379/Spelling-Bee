import csv
import itertools
import time
# data: 2D list of characters, s.t. data[i][0] = day i's center letter, and 
# data[i][1:7] = day i's outer letters
data = list(csv.reader(open('data/letters.csv', newline = ''), delimiter = ' '))

# solutions: 2D list of words, s.t. solutions[i] = list of day i's solutions, with
# pangrams first (varying number of pangrams prevents generalization)
solutions = list(csv.reader(open('data/solutions.csv', newline = ''), delimiter = ' '))


# Rules: 
# 1. Word length n: 4 <= n <= 19
# 2. Must include "center letter"
# 3. No "obscure, hyphenated, or proper noun" words, or cursing
# 4. Letters can be used more than once
# Scoring: 
# 1. 4-letter words are worth 1 point each
# 2. Longer words earn 1 point per letter
#   i.e. 'halt' = +1 point, but 'thing' = +5 points
# 3. >= 1 pangram, which uses every letter and is worth 7 extra points
#   i.e. pangram of length n is worth n + 7 points
# Ranks: 
# 1. Listed as "based on a percentage of possible points in a puzzle"
#   - Ranks, in terms of percent of maximum total points: 
#         Beginner: 0% -> discrete
#         Good Start: 2% -> rounded UP
#         Moving up: 5% -> rounded DOWN
#         Good: 8% -> discrete
#         Solid: 15% -> rounded UP 
#         Nice: 25% -> rounded DOWN
#         Great: 40% -> discrete
#         Amazing: 50% -> rounded UP 
#         Genius: 70% -> rounded DOWN (for some reason?)
#         Queen Bee: 100%
# 2. These percentages are rounded, with some massaging (we'll just round)
# 3. Generally, the human "win condition" is getting the Genius rank


def count_total_points(sol_list):
  possible_points = 0
  for i in sol_list:
    length = len(i)
    if length == 4:
      possible_points += 1
    else:
      possible_points += length
    no_rep = ''.join(set(i))
    if len(no_rep) == 7:
      possible_points += 7
  return possible_points

def get_rank_points(total_available):
  rank_points = []
  rank_percentages = [0, 0.02, 0.05, 0.08, 0.15, 0.25, 0.40, 0.50, 0.70, 1]
  for i in rank_percentages:
    rank_points.append(round(total_available * i))
  return rank_points

def get_word_points(word):
  points = 0
  length = len(word)
  no_rep = ''.join(set(word))
  if length == 4:
    points += 1
  else:
    points += length
  if len(no_rep) == 7:
    points += 7
  return points

def get_alg_solutions(alg, chars, soln, max_rank):
  vals = [([], 0, 0)]
  for r in range(1, max_rank):
    start = time.time()
    words, points = alg(chars, soln, r)
    end = time.time()
    vals.append((words, points, end - start))
  return vals




# First: Naive Brute Force, cycling through every possibility. 
# For word length n, we have 7^{n - 1} possibilities. Since n <= 19, the total
# number of options is \sum_{i = 3}^{18} 7^i  
# Note this could be done with matrix multiplication
# Testing a few variations, for best time performance on a standardized dataset

def get_all(l, n):
  yield from itertools.product(*([l] * n))

def brute_force(chars, solutions, goal_rank):
  total_possible_points = count_total_points(solutions)
  each_rank_points = get_rank_points(total_possible_points)
  solution_words = []
  total_points = 0
  string_of_chars = ''.join(chars)
  for n in range(4, 20):
    for comb in get_all(string_of_chars, n):
      word = ''.join(comb)
      if word in solutions:
        total_points += get_word_points(word)
        solution_words.append(word)
      if(total_points > each_rank_points[goal_rank]):
        break
  return solution_words, total_points


# this is faster! 
def brute_force_prime(chars, solutions, goal_rank):
  total_possible_points = count_total_points(solutions)
  each_rank_points = get_rank_points(total_possible_points)
  solution_words = []
  total_points = 0
  string_of_chars = ''.join(chars)
  for n in range(4, 20):
    for comb in get_all(string_of_chars, n):
      word = ''.join(comb)
      if chars[0] in word:
        if word in solutions:
          total_points += get_word_points(word)
          solution_words.append(word)
        if(total_points > each_rank_points[goal_rank]):
          break
  return solution_words, total_points

# this is fastest, on average! 
def valid_combinations(chars, n):
  required = chars[0]
  for combo in itertools.product(chars, repeat = n):
    if required in combo:
      yield ''.join(combo)


def brute_force_dprime(chars, solutions, goal_rank):
  total_possible_points = count_total_points(solutions)
  each_rank_points = get_rank_points(total_possible_points)
  solution_words = []
  total_points = 0
  string_of_chars = ''.join(chars)
  for n in range(4, 20):
    for word in valid_combinations(chars, n):
      if word in solutions:
        total_points += get_word_points(word)
        solution_words.append(word)
      if(total_points > each_rank_points[goal_rank]):
        break
  return solution_words, total_points
