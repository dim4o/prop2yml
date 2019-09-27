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


if __name__ == "__main__":
    import os
    import argparse

    parser = argparse.ArgumentParser(description=".properties to .yml")
    parser.add_argument("prop_path", help="Path to the properties file.", type=str)
    parser.add_argument("yml_path", nargs='?', help="Path to the yml file.", type=str, default=None)
    args = parser.parse_args()

    yml_path = args.yml_path
    if not yml_path:
        yml_path = os.getcwd() + "/" + os.path.splitext(args.prop_path)[0] + ".yml"
    print('Converting: source="{}", destination="{}"'.format(args.prop_path, yml_path))
    convert_properties_to_yml_file(in_file_path=args.prop_path, out_file_path=yml_path)
