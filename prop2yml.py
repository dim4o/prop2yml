import unittest


class Trie(object):
    class _TrieNode:
        def __init__(self):
            self.children = {}  # map: character -> _TrieNode
            self.end_of_word = False

    def __init__(self):
        self.root = self._TrieNode()

    def insert(self, word):
        """ Inserts a word into the trie.
        :param word: str
        """
        word_len = len(word)
        curr_node = self.root
        for i in range(word_len):
            if word[i] not in curr_node.children:
                new_node = self._TrieNode()
                curr_node.children[word[i]] = new_node
                if i == word_len - 1:
                    new_node.end_of_word = True

            curr_node = curr_node.children[word[i]]

    def startsWith(self, prefix):
        """ Returns all words in the trie that starts with the given prefix.
        :type prefix: str
        :return: List of words with the given prefix
        """
        # finds the first node after the prefix
        curr_node = self.root
        for ch in prefix:
            curr_node = curr_node.children.get(ch, None)
            if not curr_node:
                return []

        # appends all suffixes to the prefix recursively
        def find_paths(start_node, curr_word, paths):
            if not start_node.children or start_node.end_of_word:
                paths.append(curr_word)

            for key, val in start_node.children.items():
                find_paths(start_node=val, curr_word=curr_word + key, paths=paths)

        all_paths = []
        find_paths(start_node=curr_node, curr_word=prefix, paths=all_paths)

        # print(all_paths)
        return all_paths

    def _search_word(self, word):
        """ Searches for a hole word. For test purposes only."""
        return self._search(word, hole_word=True)

    def _search_prefix(self, prefix):
        """ Searches for a prefix. For test purposes only."""
        return self._search(prefix)

    def _search(self, value, hole_word=False):
        """ Searches for word or prefix. For test purposes only """
        curr_node = self.root
        for i in range(len(value)):
            curr_node = curr_node.children.get(value[i], None)
            if not curr_node:
                return False

        # equivalent to XNOR operator
        # True, True -> True
        # True, False -> False
        # False, False -> False
        return not (curr_node.end_of_word ^ hole_word)


trie = Trie()

trie.insert('abc')
trie.insert('abgl')
trie.insert('cdf')
trie.insert('abcd')
trie.insert('lmn')

print(trie.startsWith('a'))
print(trie.startsWith('ab'))
print(trie.startsWith('abc'))
print(trie.startsWith('l'))
print(trie.startsWith('c'))
print(trie.startsWith('lmn'))
print(trie.startsWith('z'))

print()

print(trie._search('abc', hole_word=True))
print(trie._search('ab', hole_word=True))
print(trie._search('ab', hole_word=False))

print()


class TestTrie(unittest.TestCase):
    insert_words = ["abc", "abgl", "cdf", "abcd", "lmn", "abcdefghijklmn"]
    error_true = "Should be True."
    error_false = "Should be False."

    def test_insert_and_contains(self):
        t = Trie()
        contains_words_false = ["ab", "a", "sdf", "lmnopq", "lm", "b", "m", "abcdefghijk"]
        contains_words_true = ["abc", "abgl", "cdf", "abcd", "lmn", "abcdefghijklmn"]
        contains_prefix_true = ["ab", "abg", "c", "cd", "l", "lm", "abcdefghijk", "abcdef"]
        contains_prefix_false = ["abd", "abl", "q", "cdff", "abcc", "lmo", "abcdeZghijk", "abcdeZ"]

        for w in self.insert_words:
            t.insert(word=w)

        for w in self.insert_words:
            self.assertEqual(t._search_word(w), True, self.error_true)

        for w in contains_words_false:
            self.assertEqual(t._search_word(w), False, self.error_false)

        for w in contains_words_true:
            self.assertEqual(t._search_word(w), True, self.error_true)

        for w in contains_prefix_true:
            self.assertEqual(t._search_prefix(w), True, self.error_true)

        for w in contains_prefix_false:
            self.assertEqual(t._search_prefix(w), False, self.error_false)

    def test_search_empty_trie(self):
        t = Trie()

        for w in self.insert_words:
            self.assertEqual(t._search_word(w), False, self.error_false)
            self.assertEqual(t._search_prefix(w), False, self.error_false)


if __name__ == "__main__":
    unittest.main()
