# import numpy as np

import numpy as np

from treelib import Tree


def label_tree(tree):
    # We number the leaves of the new graph T
    # according to their appearance in the pre-order traversal
    # starting from s.
    label = 1
    s_index = 0
    s_found = False
    for i, n in enumerate(tree.leaves()):
        if n.identifier == "s":
            s_found = True
        if s_found:
            n.tag = str(label)
            label += 1
        else:
            s_index += 1
    for i, n in enumerate(tree.leaves()[:s_index]):
        n.tag = str(label)
        label += 1

    # Then, for each non-leaf vertex, number it with the median
    # of the numbers corresponding to
    # its children. If any of them is having two children,
    # then number it with the maximum number belonging to
    # its children. We denote the number corresponding
    # to the vertex v after numbering in this fashion by n(v).
    tree.show()
    for level in range(tree.depth()-1, -1, -1):
        nodes = list(tree.filter_nodes(lambda x: tree.depth(x) == level))
        for n in nodes:
            children = tree.children(n.identifier)
            if len(children) > 0:
                print(children)
                if len(children) <= 2:
                    n.tag = str(max([int(c.tag) for c in children]))
                else:
                    n.tag = str(int(np.median([int(c.tag) for c in children])))


tree = Tree()

tree.create_node("r", "r")
tree.create_node("a", "a", parent="r")
tree.create_node("b", "b", parent="r")
tree.create_node("c", "c", parent="a")
tree.create_node("d", "d", parent="a")
tree.create_node("e", "e", parent="a")
tree.create_node("s", "s", parent="r")
tree.create_node("f", "f", parent="b")
tree.create_node("g", "g", parent="b")
tree.create_node("h", "h", parent="b")
tree.create_node("z", "z", parent="r")
tree.create_node("x", "x", parent="z")
tree.create_node("y", "y", parent="z")

tree.show()
label_tree(tree)
tree.show()
