import csv
import matplotlib.pyplot as plt
import numpy as np
import string
import re
import random
import enchant
from obscure_words import load_obscure_words
from nltk.corpus import words

d = enchant.Dict("en_US")
d_2 = set(words.words())
obscure_dict = load_obscure_words()

data = list(csv.reader(open('src/data/letters.csv', newline = ''), delimiter = ' '))
solutions = list(csv.reader(open('src/data/solutions.csv', newline = ''), delimiter = ' '))


x_axis = np.linspace(0, 19, 20)
def generate_cur_corpus():
  word_f = open('src/data/words.txt', 'r')
  with open('src/data/words_cur.txt', 'w') as new:
    capital_ascii = (string.ascii_uppercase) # remove proper nouns
    for word in word_f:
      add_to_cur = True
      word_prime = re.sub(r'[^a-zA-Z]', '', word)
      word_len = len(word_prime) # remove too large of words
      char_set = set(word_prime)
      if word_len < 4 or word_len > 19:
        add_to_cur = False
      elif 's' in char_set: # remove words with s in them
        add_to_cur = False
      elif len(char_set) > 7: # remove words with more than seven characters
        add_to_cur = False
      else:
        for char in word_prime:
          if char in capital_ascii:
            add_to_cur = False
      if add_to_cur:
        new.write(word_prime + '\n')
      
# generate_cur_corpus() -> Generate Curated Corpus in src/data/words_cur.txt

curated_corpus = open('src/data/words_cur.txt', 'r')

def filter_pangrams(dict_set):
  remove_these = set()
  vowel_no_y = set(('a', 'e', 'i', 'o', 'u'))
  for i in dict_set:
    chars = set(i)
    if len(chars) == 7:
      if len(chars.intersection(vowel_no_y)) < 2 or len(chars.intersection(vowel_no_y.union(set('y')))) > 3:
        remove_these.add(i)
    else:
      num_chars = len(chars)
      num_v_noy = len(chars.intersection(vowel_no_y))
      num_v_y = len(chars.intersection(vowel_no_y.union(set('y'))))
      if num_v_y > 3:
        remove_these.add(i)
      elif num_chars == 6 and num_v_noy == 0:
        remove_these.add(i)
  return remove_these


def cur_corpus_further(corpus_file):
  too_big = set()
  remove_these = set()
  for i in corpus_file:
    too_big.add(i[:-1])
  data_set_list = []
  solutions_set_list = []
  required_list = []
  for i in range(0, len(data)):
    chars_set = set(data[i])
    filter = set(solutions[i])
    required = data[i][0]
    data_set_list.append(chars_set)
    solutions_set_list.append(filter)
    required_list.append(required)
  for word in too_big:
    word_set = set(word) 
    if word_set in data_set_list:
      game = data_set_list.index(word_set)
      need = required_list[game]
      if need in word_set:
        if word not in solutions_set_list[game]:
          remove_these.add(word) # Remove objectively obscure words
  bad_pangrams = filter_pangrams(too_big)
  for rmv in bad_pangrams:
    remove_these.add(rmv)
  obsc_pangram_set = set()
  obsc_others_set = set()
  for game in solutions:
    for word in game:
      if word in obscure_dict:
        if len(set(word)) == 7: # pangram
          obsc_pangram_set.add(word)
        else: # not a pangram
          obsc_others_set.add(word)
  all_obsc_pangrams = set()
  all_obsc_words = set()
  for obsc_word in obscure_dict:
    if len(set(obsc_word)) < 8: # valid solution word
      if len(set(obsc_word)) == 7: # pangram
        all_obsc_pangrams.add(obsc_word)
      else:
        all_obsc_words.add(obsc_word)
  pangram_rand_rat = len(obsc_pangram_set) / len(all_obsc_pangrams)
  others_rand_rat = len(obsc_others_set) / len(all_obsc_words)
  for elt in too_big:
    if elt in obscure_dict:
      rand = random.random()
      if len(set(elt)) == 7: # elt is a pangram
        if rand > pangram_rand_rat:
          remove_these.add(elt)
      else: 
        if rand > others_rand_rat:
          remove_these.add(elt)
  for elt in too_big:
    rand = random.random()
    if not d.check(elt) and elt not in d_2:
      if rand > (31/589):
        remove_these.add(elt)
    elif not d.check(elt):
      if rand > (40/589):
        remove_these.add(elt)
    elif elt not in d_2:
      if rand > (86/589):
        remove_these.add(elt)
  for elt in remove_these:
    too_big.remove(elt)
  with open('src/data/words_cur_further.txt', 'w') as new:
    for elt in too_big:
      new.write(elt + '\n')

# cur_corpus_further(curated_corpus)
further_cur_corpus = open('src/data/words_cur_further.txt', 'r')



def find_dists(words):
  len_dist = np.zeros(20)
  pg_dist = np.zeros(20)
  for line in words:
    word = line[:-1] # remove newline character
    len_dist[len(word)] += 1
    if len(set(word)) == 7:
      pg_dist[len(word)] += 1
  return len_dist, pg_dist


def plot_word_info(words):
  len_dist, pg_dist = find_dists(words)
  p_pangram_given_length = np.zeros(20)
  for i in range(0, 20):
    if pg_dist[i] != 0:
      p_pangram_given_length[i] = pg_dist[i] / len_dist[i]
  len_c = np.zeros(20)
  pg_c = np.zeros(20)
  for i in range(0, 20):
    len_c[i] += np.sum(len_dist[:i + 1])
    pg_c[i] += np.sum(pg_dist[:i + 1])
  
  total_len = np.sum(len_dist)

  non_pans = len_dist - pg_dist
  non_pans_c = len_c - pg_c

  len_probs = non_pans / total_len
  pg_probs = pg_dist / total_len
  len_cdf = non_pans_c / total_len
  pg_cdf = pg_c / total_len
  fig, ax = plt.subplots(2, sharex = True)
  fig.suptitle('PMF and CDF of Given Solutions by Length')
  ax[0].bar(x_axis, pg_probs, color = 'r', label = 'Pangrams')
  ax[0].bar(x_axis, len_probs, bottom = pg_probs, color = 'b', label = 'Non-Pangrams')
  ax[0].legend()
  ax[0].set_ylabel('P[Length = X]')

  ax[1].bar(x_axis, pg_cdf, color = 'r', label = 'Pangrams')
  ax[1].bar(x_axis, len_cdf, bottom = pg_cdf, color = 'b', label = 'Non-Pangrams')
  ax[1].legend()
  ax[1].set_xlabel('Word Length')
  ax[1].set_ylabel('P[Length <= X]')
  ax[1].set_xticks(np.arange(0, 21, 1))

  plt.show()



# Plotting Stuff, all completed and saved


# given_solns = set()
# for i in solutions:
#   for j in i:
#     given_solns.add(j + '\n')
# plot_word_info(given_solns) -> Already Plotted and Saved
# plot_word_info(curated_corpus) -> Already Plotted and Saved
# plot_word_info(further_cur_corpus)