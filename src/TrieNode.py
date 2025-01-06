import nltk
from nltk.corpus import wordnet
import collections
from collections import deque
import game

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

# Potentially precomputed, to reduce runtime
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

def dfs(node, trie, chars, soln, current_word, output, goal_points):
  (words, curr_score) = output
  if node.end_of_word:
    if current_word in soln and current_word not in words:
      words.append(current_word)
      up_score = curr_score + game.get_word_points(current_word)
      output = (words, up_score)
      if up_score >= goal_points:
        return (words, up_score)
  for ch in chars:
    if ch in node.children:
      updated_output = (words, curr_score)
      result = dfs(
        node = node.children[ch],
        trie = trie,
        chars = chars,
        soln = soln,
        current_word = current_word + ch,
        output = updated_output,
        goal_points = goal_points
      )
      if result is not None:
        return result
  return (words, curr_score)

def bfs(trie, chars, soln, output, goal_points):
  out_words, out_points = output
  queue = deque()
  queue.append((trie.root, ""))
  while queue and out_points < goal_points:
    node, prefix = queue.popleft()
    if node.end_of_word:
      if prefix not in out_words and prefix in soln:
        out_words.append(prefix)
        out_points += game.get_word_points(prefix)
        if out_points >= goal_points:
          break
    for ch, child_node in node.children.items():
      if ch in chars:
        queue.append((child_node, prefix + ch))
  return output




def trieAlg(chars, solns, goal_points, DFS, trie):
  # DFS is a flag for DFS (True) or BFS (False)
  if trie is None:
    trie = build_trie_from_chars(chars)
  if DFS:
    words, points = dfs(
      node = trie.root,
      trie = trie,
      chars = chars,
      soln = solns,
      current_word = "",
      output = ([], 0),
      goal_points = goal_points
    )
  else:
    words, points = bfs(
      trie = trie,
      chars = chars,
      soln = solns,
      output = ([], 0),
      goal_points = goal_points
    )
  return words, points


