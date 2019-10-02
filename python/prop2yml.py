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
        curr_node = self.root
        for char in prop_key:
            if char not in curr_node.children:
                curr_node.children[char] = self._PropertiesNode()
            curr_node = curr_node.children[char]
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


def convert_properties_to_yml(in_file_path, out_file_path=None, remove_source=False):
    """ Converts properties file to yml file
    :param in_file_path: the path to the file.properties source
    :param out_file_path: the path to the output yml file
    :param remove_source: whether to remove the properties file source after converting
    """
    if not out_file_path:
        out_file_path = os.getcwd() + "/" + os.path.splitext(in_file_path)[0] + ".yml"
    print('Converting: source="{}", destination="{}"'.format(in_file_path, out_file_path))

    trie = PropertiesTrie()
    with open(in_file_path, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split("=", 1)
                trie.insert(key.split("."), value)
    with open(out_file_path, 'w') as file:
        file.write(trie.to_yml())

    if remove_source:
        os.remove(in_file_path)


if __name__ == "__main__":
    import os
    import glob
    import argparse

    parser = argparse.ArgumentParser(description=".properties to .yml")
    parser.add_argument("prop_path", help="Path to the properties file.", type=str)
    parser.add_argument("yml_path", nargs='?', help="Path to the yml file.", type=str, default=None)
    parser.add_argument("-rm", help="Whether to remove the source file.", action='store_true')
    args = parser.parse_args()
    # print(args)
    if not args.yml_path and os.path.isdir(args.prop_path):
        os.chdir(args.prop_path)
        for prop_file in glob.glob("**/*.properties", recursive=True):
            convert_properties_to_yml(prop_file, remove_source=args.rm)
    else:
        convert_properties_to_yml(in_file_path=args.prop_path, out_file_path=args.yml_path, remove_source=args.rm)
