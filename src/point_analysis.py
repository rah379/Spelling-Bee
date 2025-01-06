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

# total_potential_points_dist = np.zeros(14)
# for i in range(0, 14):
#   total_potential_points_dist[i] = game.count_total_points(solutions[i])

# plt.figure()
# plt.hist(total_potential_points_dist, bins = 'auto', edgecolor = 'black', alpha = 0.7)
# plt.title('Distribution of Total Potential Points')
# plt.xlabel('Total Potential Points')
# plt.ylabel('Frequency')
# plt.show()

def generate_bees():
  letters = list(string.ascii_lowercase)
  for i, first_letter in enumerate(letters):
    others = letters[:i] + letters[i + 1:]
    for combo in itertools.combinations(others, 6):
      yield [first_letter] + sorted(combo)



freq_map = np.zeros(26)
first_map = np.zeros(26)
for i in range(0, 14):
  for j in range(0, 7):
    char = data[i][j]
    idx = string.ascii_lowercase.index(char)
    if j == 0:
      first_map[idx] += 1
    freq_map[idx] += 1

x_axis = np.array(list(string.ascii_lowercase))
total_letters = freq_map.sum()
freq_map = freq_map / total_letters
first_map = first_map / first_map.sum()
real_values = [8.2, 1.5, 2.8, 4.3, 12.7, 2.2, 2.0, 6.1, 7.0, 0.15, 0.77, 4.0, 
                        2.4, 6.7, 7.5, 1.9, 0.095, 6.0, 9.1, 
                        2.8, 0.98, 2.4, 0.15, 2.0, 0.074]
alphabet = list(string.ascii_lowercase)
alphabet.remove('s')
value_alph_tuple = [(real_values[i], alphabet[i]) for i in range(0, 25)]
sorted_by_freq = sorted(value_alph_tuple, key = lambda x:x[0])
print(sorted_by_freq)





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

