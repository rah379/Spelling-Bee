import game
import re
# Second: Dictionary Filtering, starting with the "entire" dictionary, and filtering
# words based on the rules of the game

def generate_corpus(): # Call for Precompute level 0
  word_f = open('src/data/words.txt', 'r')
  big_data = set()
  for word in word_f:
    big_data.add(word)
  return big_data

def remove_non_alpha(set_of_words): # Precompute level 2
  out_set = set()
  for str in set_of_words:
    str_prime = re.sub(r'[^a-zA-Z]', '', str)
    out_set.add(str_prime)
  return out_set

def only_subset(set_of_words, chars): # Precompute level 3
  char_set = set(chars)
  out_words = set()
  for word in set_of_words:
    if set(word).issubset(char_set):
      out_words.add(word)
  return out_words

def only_required(set_of_words, required): # Precompute level 4
  out_words = set()
  for word in set_of_words:
    if required in set(word):
      out_words.add(word)
  return out_words

def build_dict(precomputation, chars):
  out_set = generate_corpus()
  if precomputation < 2:
    return out_set
  prec_two = remove_non_alpha(out_set)
  if precomputation == 2:
    return prec_two
  prec_three = only_subset(prec_two, chars)
  if precomputation == 3:
    return prec_three
  prec_four = only_required(prec_three, chars[0])
  return prec_four

def naive_df_prime(chars, soln, goal_points, precomputation, dict = None): # dict = None when precomputation = 0
  dict_four = set()
  if dict is None: #precomputation = 0
    dict_four = build_dict(4, chars)
  solution_set = set(soln)
  found_words = set()
  points_earned = 0
  if precomputation == 1:
    dict_two = remove_non_alpha(dict)
    dict_three = only_subset(dict_two, chars)
    required = chars[0]
    dict_four = only_required(dict_three, required)
  if precomputation == 2:
    required = chars[0]
    dict_three = only_subset(dict, chars)
    dict_four = only_required(dict_three, required)
  if precomputation == 3:
    required = chars[0]
    dict_four = only_required(dict, required)
  if precomputation == 4:
    dict_four = dict
  for word in dict_four:
    if (4 <= len(word) <= 19) and (word in solution_set):
      found_words.add(word)
      points_earned += game.get_word_points(word)
    if points_earned >= goal_points:
      found_words_lst = list(found_words)
      return (found_words_lst, points_earned)
  found_words_lst = list(found_words)
  return (found_words_lst, points_earned)