import csv
import matplotlib.pyplot as plt
import numpy as np
import string
import re

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

  print(len_probs, pg_probs)
  for i in range(0, 20):
    print("%i & %f & %f & %f \\\\" %(i, len_probs[i] + pg_probs[i], 
                                     len_cdf[i] + pg_cdf[i], p_pangram_given_length[i]))

  plt.show()


# given_solns = set()
# for i in solutions:
#   for j in i:
#     given_solns.add(j + '\n')
# plot_word_info(given_solns) -> Already Plotted and Saved
# plot_word_info(curated_corpus) -> Already Plotted and Saved


"""
y_axis =  find_total_dist()
total_potential_words = np.sum(y_axis)
probabilities = np.zeros(20)
for i in range(0, 20):
  probabilities[i] = y_axis[0:i+ 1].sum(axis = 0)
probabilities = probabilities / total_potential_words
y_prime_axis = y_axis / total_potential_words
plt.bar(x_axis, y_prime_axis)               
plt.xticks(np.arange(0, 21, 1)) 
plt.xlabel('Number of Characters')
plt.ylabel('Probability of Potential Solution Words Being Length x')
plt.title('Probability of Potential Solution Words by Length')
plt.show()
"""