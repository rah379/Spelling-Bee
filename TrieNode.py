import nltk
from nltk.corpus import wordnet
import collections


class TrieNode:
  def __init__(self):
    self.children = collections.defaultdict(TrieNode)
    self.end_of_word = False

class Trie:

  def __init__(self):
    self.root = TrieNode()

  def insert(self, word : str) -> None:
    current = self.root
    for ch in word:
      current = current.children[ch]
    current.end_of_word = True
  
  def search(self, word : str) -> bool:
    current = self.root
    for ch in word:
      current = current.children.get(ch)
      if current is None:
        return False
    return current.is_end

# This is precomputed, to reduce runtime
def build_trie_from_chars(chars):
  char_set = set(chars)
  trie = Trie()
  word_set = set()
  for syn in wordnet.all_synsets():
    for lemma in syn.lemma_names():
      word = lemma.lower()
      if chars[0] not in word:
        continue
      if "_" in word:
        continue
      if "-" in word or "'" in word:
        continue
      if (4 > len(word) or len(word) > 19):
        continue
      if not (set(word).issubset(char_set)):
        continue
      if word not in word_set:
        word_set.add(word)
        trie.insert(word)
  return trie

def find_all_words(node, trie, chars, current_word, results):
  if node.end_of_word:
    results.append(current_word)
  for ch in chars:
    if ch in node.children:
      find_all_words(
        node = node.children[ch],
        trie = trie,
        chars = chars,
        current_word = current_word + ch,
        results = results
      )

def search(trie, chars):
  char_set = set(chars)
  results = []
  find_all_words(
    node = trie.root,
    trie = trie,
    chars = char_set,
    current_word = "",
    results = results
  )
  return results
