import nltk
from nltk.corpus import wordnet as wn
import game
# Second: Dictionary Filtering, starting with the "entire" dictionary, and filtering
# words based on the rules of the game

def build_wordnet_dict():
  word_set = set()
  for syn in wn.all_synsets():
    for lemma in syn.lemma_names():
      if "_" in lemma:
        continue
      word = lemma.lower()
      if "-" in word or "'" in word:
        continue
      word_set.add(word)
  return word_set

def filter_words(word_set, chars):
  required = chars[0]
  allowed_letters = set(chars)
  valid_words = []
  for w in word_set:
    if not (4 <= len(w) <= 19):
      continue
    if required not in w:
      continue
    if not set(w).issubset(allowed_letters):
      continue
    valid_words.append(w)
  return valid_words

def filter_words_prime(word_set, soln):
  soln_set = set(soln)
  valid_words = []
  for w in word_set:
    if w in soln_set:
      valid_words.append(w)
  return valid_words

def dictionary_filter(chars, solns, goal_rank):
  total_possible_points = game.count_total_points(solns)
  each_rank_points = game.get_rank_points(total_possible_points)
  total_points = 0
  word_set = build_wordnet_dict()
  valid_words = filter_words(word_set, chars)
  soln_set = set(solns)
  solution_words = []
  for word in valid_words:
    if word in soln_set:
      total_points += game.get_word_points(word)
      solution_words.append(word)
      if(total_points >= each_rank_points[goal_rank]):
        break
  return solution_words, total_points


# The above solution is very slow- examining every word in the wordnet dataset
# is worse time with lower `n`, due to more restrictive dataset! 


# Trying different approach- restrict possibilities while building wordset
def build_minimal_wordnet(chars):
  allowed_letters = set(chars)
  required_letter = chars[0]
  word_set = set()
  for syn in wn.all_synsets():
    for lemma in syn.lemma_names():
      if "_" in lemma:
        continue
      word = lemma.lower()
      if "-" in word or "'" in word:
        continue
      if required_letter not in word:
        continue
      if not (4 <= len(word) <= 19):
        continue
      if not set(word).issubset(allowed_letters):
        continue
      word_set.add(word)
  return word_set

def dictionary_filter_prime(chars, solns, goal_rank):
  total_possible_points = game.count_total_points(solns)
  each_rank_points = game.get_rank_points(total_possible_points)
  total_points = 0
  valid_words = build_minimal_wordnet(chars)
  soln_set = set(solns)
  solution_words = []
  for word in valid_words:
    if word in soln_set:
      total_points += game.get_word_points(word)
      solution_words.append(word)
      if(total_points >= each_rank_points[goal_rank]):
        break
  return solution_words, total_points

# This is still extremely slow! Actually slower



# Third approach- stop building after meeting our heuristic of >= k% scored
def stop_at_success(soln, goal_rank):
  total_possible_points = game.count_total_points(soln)
  each_rank_points = game.get_rank_points(total_possible_points)
  total_points = 0
  soln_words = []
  soln_set = set(soln)
  for syn in wn.all_synsets():
    for lemma in syn.lemma_names():
      word = lemma.lower()
      if word in soln_set:
        total_points += game.get_word_points(word)
        soln_words.append(word)
      if total_points >= each_rank_points[goal_rank]:
        return soln_words, total_points
  return [], -1 #indicates we don't have the correct words in wordnet, unlikely



