import itertools
import game
# First: Naive Brute Force, cycling through every possibility. 
# For word length n, we have 7^{n - 1} possibilities. Since n <= 19, the total
# number of options is \sum_{i = 3}^{18} 7^i  
# Note this could be done with matrix multiplication
# Testing a few variations, for best time performance on a standardized dataset

def get_all(l, n):
  yield from itertools.product(*([l] * n))

def brute_force(chars, solutions, goal_rank):
  total_possible_points = game.count_total_points(solutions)
  each_rank_points = game.get_rank_points(total_possible_points)
  solution_words = []
  total_points = 0
  string_of_chars = ''.join(chars)
  for n in range(4, 20):
    for comb in get_all(string_of_chars, n):
      word = ''.join(comb)
      if word in solutions:
        total_points += game.get_word_points(word)
        solution_words.append(word)
      if(total_points > each_rank_points[goal_rank]):
        break
  return solution_words, total_points


# this is faster! 
def brute_force_prime(chars, solutions, goal_rank):
  total_possible_points = game.count_total_points(solutions)
  each_rank_points = game.get_rank_points(total_possible_points)
  solution_words = []
  total_points = 0
  string_of_chars = ''.join(chars)
  for n in range(4, 20):
    for comb in get_all(string_of_chars, n):
      word = ''.join(comb)
      if chars[0] in word:
        if word in solutions:
          total_points += game.get_word_points(word)
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

def brute_force_dprime(chars, solutions, goal_points):
  solution_words = []
  total_points = 0
  sol_set = set(solutions)
  for n in range(4, 20):
    for word in valid_combinations(chars, n):
      if word in sol_set:
        total_points += game.get_word_points(word)
        solution_words.append(word)
      if(total_points >= goal_points):
        break
  return solution_words, total_points


# Brute force is still prohibitively slow to achieve "genius", our win condition

