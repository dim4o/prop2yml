import unittest


class PropertiesTrie(object):
    class _PropertiesNode:
        def __init__(self, node_value=None):
            self.value = node_value
            self.children = {}  # map: character -> _TrieNode

    def __init__(self):
        self.root = self._PropertiesNode()

    def insert(self, prop_key, prop_value):
        """ Inserts a word into the trie.
        :param prop_key: List
        :param prop_value: str
        """
        word_len = len(prop_key)
        curr_node = self.root
        for i in range(word_len):
            if prop_key[i] not in curr_node.children:
                curr_node.children[prop_key[i]] = self._PropertiesNode()

            curr_node = curr_node.children[prop_key[i]]

            if i == word_len - 1:
                curr_node.value = prop_value

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

    def to_yml(self):
        """ Converts the properties tree to yml format
        :return: yml format as a string
        """
        def helper(start_node, start_key, depth=-1):
            yml = ""
            if start_key:
                val = "" if not start_node.value else " " + str(start_node.value)
                yml = "\t" * depth + start_key + ":" + val + "\n"

            for start_key, _ in start_node.children.items():
                yml += helper(start_node.children[start_key], start_key, depth + 1)
            return yml

        return helper(start_node=self.root, start_key=None) + "\n\n"


def convert_properties_to_yml_file(in_file_path, out_file_path):
    """ Converts properties file to yml file """
    trie = PropertiesTrie()
    with open(in_file_path, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split("=", 1)
                trie.insert(key.split("."), value)
    with open(out_file_path, 'w') as file:
        file.write(trie.to_yml())


prop_pref = './python/resources/properties/'
yml_pref = './python/resources/yml/'
convert_properties_to_yml_file(prop_pref + 'application_1.properties', yml_pref + "test.yml")


class TestPropertiesTrie(unittest.TestCase):
    insert_words = ["abc", "abgl", "cdf", "abcd", "lmn", "abcdefghijklmn"]
    error_true = "Should be True."
    error_false = "Should be False."

    def test_insert_and_contains(self):
        t = PropertiesTrie()
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
        t = PropertiesTrie()

        for w in self.insert_words:
            self.assertEqual(t._search_word(w), False, self.error_false)
            self.assertEqual(t._search_prefix(w), False, self.error_false)


if __name__ == "__main__":
    unittest.main()
