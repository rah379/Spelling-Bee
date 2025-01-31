import csv
import time
import TrieNode as tn
import greedy as g
import dictionary_filter as df
# data: 2D list of characters, s.t. data[i][0] = day i's center letter, and 
# data[i][1:7] = day i's outer letters
# data = list(csv.reader(open('src/data/letters.csv', newline = ''), delimiter = ' '))

# solutions: 2D list of words, s.t. solutions[i] = list of day i's solutions, with
# pangrams first (varying number of pangrams prevents generalization)
# solutions = list(csv.reader(open('src/data/solutions.csv', newline = ''), delimiter = ' '))



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

rank_percentages = [0, 0.02, 0.05, 0.08, 0.15, 0.25, 0.40, 0.50, 0.70, 1]


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

def get_all_rank_points(total_available):
  rank_points = [round(total_available * i) for i in rank_percentages]
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

def use_bf(bf_alg, chars, soln, rank, priority = None):
  total_possible = count_total_points(soln)
  rank_points = round(rank_percentages[rank] * total_possible)
  if priority is None:
    start = time.time()
    words, points = bf_alg(chars, soln, rank_points)
    end = time.time()
  else:
    start = time.time()
    words, points = bf_alg(chars, soln, rank_points, priority)
    end = time.time()
  return words, points, end - start

def use_df(df_alg, chars, soln, rank, precomputation, dict = None):
  total_possible = count_total_points(soln)
  rank_points = round(rank_percentages[rank] * total_possible)
  if dict is None:
    start = time.time()
    words, points = df_alg(chars, soln, rank_points, precomputation)
    end = time.time()
  else:
    start = time.time()
    words, points = df_alg(chars, soln, rank_points, precomputation, dict)
    end = time.time()
  return words, points, end - start











def get_alg_solutions(alg, chars, soln, max_rank, 
                      trie_alg = False, greedy = False, precompute = False, DFS = False):
  total_possible = count_total_points(soln)
  each_rank_points = get_all_rank_points(total_possible)
  words_result = [[]]
  points_result = [0]
  times = [0]
  for r in range(1, max_rank):
    if trie_alg == False and greedy == False:
      start = time.time()
      words, points = alg(chars, soln, each_rank_points[r])
      end = time.time()
      words_result.append(words)
      points_result.append(points)
      times.append(end - start)
    elif trie_alg == True and greedy == False:
      if precompute:
        trie = tn.build_trie_from_chars(chars)
      else:
        trie = None
      start = time.time()
      words, points = alg(chars, soln, each_rank_points[r], DFS, trie)
      end = time.time()
      words_result.append(words)
      points_result.append(points)
      times.append(end - start)
    else:
      if precompute: 
        valid_words = g.filter_dictionary(chars)
      else:
        valid_words = None
      start = time.time()
      words, points = alg(chars, soln, each_rank_points[r], valid_words)
      end = time.time()
      words_result.append(words)
      points_result.append(points)
      times.append(end - start)
  return words_result, points_result, times