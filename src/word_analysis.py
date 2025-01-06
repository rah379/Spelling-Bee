import csv
import nltk
from nltk.corpus import wordnet as wn
import matplotlib.pyplot as plt
import numpy as np

data = list(csv.reader(open('src/data/letters.csv', newline = ''), delimiter = ' '))

# solutions: 2D list of words, s.t. solutions[i] = list of day i's solutions, with
# pangrams first (varying number of pangrams prevents generalization)
solutions = list(csv.reader(open('src/data/solutions.csv', newline = ''), delimiter = ' '))

x_axis = np.linspace(0, 19, 20)


def find_total_dist():
  y_axis = np.zeros(20)
  for syn in wn.all_synsets():
    for lemma in syn.lemma_names():
      if "_" in lemma:
        continue
      word = lemma.lower()
      if "-" in word or "'" in word:
        continue
      if not (4 <= len(word) <= 19):
        continue
      no_rep = ''.join(set(word))
      if len(no_rep) > 7:
        continue
      y_axis[len(word)] += 1
  return y_axis

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