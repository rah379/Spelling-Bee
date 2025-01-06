import nltk
from nltk.corpus import wordnet
import game


# Basic loading of dictionary (not filtering yet)
def load_wordnet_words():
  word_set = set()
  for syn in wordnet.all_synsets():
    for lemma in syn.lemma_names():
      word = lemma.lower()
      if "_" in word:
        continue
      if "-" in word or "'" in word:
        continue
      word_set.add(word)
  return word_set

def filter_dictionary(chars):
  dictionary = load_wordnet_words()
  required = chars[0]
  allowed = set(chars)
  valid_words = []
  for w in dictionary:
    if not (4 <= len(w) <= 19):
      continue
    if required not in w:
      continue
    if set(w).issubset(allowed):
      valid_words.append(w)
  return valid_words

def word_score_pairs(valid_words):
  result = []
  for i in valid_words:
    result.append((i, game.get_word_points(i)))
  return result

def greedy_alg(chars, soln, goal_points, valid_words = None):
  if valid_words is None:
    valid_words = filter_dictionary(chars)
  pairs = word_score_pairs(valid_words)
  pairs.sort(key = lambda x: x[1], reverse = True)
  chosen_words = []
  points_sofar = 0
  for word, pt in pairs:
    if word in soln:
      chosen_words.append(word)
      points_sofar += pt
      if points_sofar >= goal_points:
        break
  return chosen_words, points_sofar