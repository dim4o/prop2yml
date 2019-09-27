import unittest
import prop2yml


class TestPropertiesTrie(unittest.TestCase):
    class _Trie(prop2yml.PropertiesTrie):
        def _search_word(self, word):
            """ Searches for a hole word. For test purposes only."""
            return self._search(word, hole_word=True)

        def _search_prefix(self, prefix):
            """ Searches for a prefix. For test purposes only."""
            return self._search(prefix)

        def _search(self, prop_key, hole_word=False):
            """ Searches for word or prefix. For test purposes only """
            curr_node = self.root
            for i in range(len(prop_key)):
                curr_node = curr_node.children.get(prop_key[i], None)
                if not curr_node:
                    return False

            # equivalent to XNOR operator
            # True, True -> True
            # True, False -> False
            # False, False -> False
            end_of_word = False if curr_node.value is None else True
            result = not (end_of_word ^ hole_word)
            return result

    insert_words = ["abc", "abgl", "cdf", "abcd", "lmn", "abcdefghijklmn"]
    error_true = "Should be True."
    error_false = "Should be False."

    def test_insert_and_contains(self):
        t = self._Trie()
        contains_words_false = ["ab", "a", "sdf", "lmnopq", "lm", "b", "m", "abcdefghijk"]
        contains_words_true = ["abc", "abgl", "cdf", "abcd", "lmn", "abcdefghijklmn"]
        contains_prefix_true = ["ab", "abg", "c", "cd", "l", "lm", "abcdefghijk", "abcdef"]
        contains_prefix_false = ["abd", "abl", "q", "cdff", "abcc", "lmo", "abcdeZghijk", "abcdeZ"]

        dummy_value = 42
        for w in self.insert_words:
            t.insert(prop_key=w, prop_value=dummy_value)

        for w in self.insert_words:
            curr_result = t._search_word(w)
            self.assertEqual(curr_result, True, self.error_true)

        for w in contains_words_false:
            self.assertEqual(t._search_word(w), False, self.error_false)

        for w in contains_words_true:
            self.assertEqual(t._search_word(w), True, self.error_true)

        for w in contains_prefix_true:
            self.assertEqual(t._search_prefix(w), True, self.error_true)

        for w in contains_prefix_false:
            self.assertEqual(t._search_prefix(w), False, self.error_false)

    def test_search_empty_trie(self):
        t = self._Trie()

        for w in self.insert_words:
            self.assertEqual(t._search_word(w), False, self.error_false)
            self.assertEqual(t._search_prefix(w), False, self.error_false)


if __name__ == "__main__":
    unittest.main()