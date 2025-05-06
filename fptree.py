# Sample transactions
transactions = [
    ['bread', 'milk'],
    ['bread', 'diaper', 'beer', 'egg'],
    ['milk', 'diaper', 'beer', 'coke'],
    ['bread', 'milk', 'diaper', 'beer'],
    ['bread', 'milk', 'diaper', 'coke']
]

min_support = 2

# Count frequency of each item
def count_items(transactions):
    counts = {}
    for t in transactions:
        for item in t:
            counts[item] = counts.get(item, 0) + 1
    return {item: count for item, count in counts.items() if count >= min_support}

# Sort items in transactions by frequency
def sort_items(transactions, freq):
    sorted_trans = []
    for t in transactions:
        sorted_t = [item for item in t if item in freq]
        sorted_t.sort(key=lambda x: -freq[x])
        if sorted_t:
            sorted_trans.append(sorted_t)
    return sorted_trans

# Simple FP-tree node
class Node:
    def __init__(self, item):
        self.item = item
        self.count = 1
        self.children = {}

# Build FP-tree
def build_tree(transactions):
    root = Node(None)
    for t in transactions:
        current = root
        for item in t:
            if item not in current.children:
                current.children[item] = Node(item)
            else:
                current.children[item].count += 1
            current = current.children[item]
    return root

# Recursively find prefix paths
def find_paths(tree, path):
    if not tree.children:
        return [path] * tree.count
    paths = []
    for child in tree.children.values():
        paths += find_paths(child, path + [child.item])
    return paths

# Mine frequent patterns
def mine(tree, prefix, patterns):
    for item, node in tree.children.items():
        new_prefix = prefix + [item]
        patterns.append((new_prefix, node.count))
        mine(node, new_prefix, patterns)

# FP-Growth main function
def fp_growth(transactions):
    freq = count_items(transactions)
    sorted_trans = sort_items(transactions, freq)
    tree = build_tree(sorted_trans)
    patterns = []
    mine(tree, [], patterns)
    return patterns

# Run and print
patterns = fp_growth(transactions)
for pattern, count in patterns:
    print(f"{pattern}: {count}")