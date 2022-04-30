# import numpy as np

import matplotlib.pyplot as plt
import numpy as np

from pprint import pprint
from treelib import Tree


def label_tree(tree):
    # We number the leaves of the new graph T
    # according to their appearance in the pre-order traversal
    # starting from s.
    label = 1
    s_index = 0
    s_found = False
    for i, n in enumerate(tree.leaves()):
        if n.identifier == 's':
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
                if len(children) <= 2:
                    n.tag = str(max([int(c.tag) for c in children]))
                else:
                    n.tag = str(int(np.median([int(c.tag) for c in children])))


def rectilinear_embedding(tree):
    # The embedding works in the following way.
    # Put the vertex s at the coordinate (2n(s), 0).
    # Let v be any other vertex. Suppose the parent of v, say u,
    # has been placed at (Xu, Yu). We place v at (Xv, Yv), where
    # Xv = Xu + 2 (n(u) − n(v)), and Yv = Yu + 2 (N − |n(u) − n(v)|).
    embedding = dict()
    N = tree.size()
    n = tree.get_node('s')
    embedding[n.identifier] = np.array([2*int(n.tag), 0])
    segments_X = []
    segments_Y = []
    # The edges are mapped to paths parallel to axis.
    # We draw the edge between u and v as follows. Draw a
    # line of length (N − |n(u) − n(v)|) in the positive
    # NOTE: is this an error? Should not be 2*(N - |n(u) - n(v)|

    # Y direction from u and then a line of length 2|n(u)−n(v)|
    # in the positive/negative direction of X axis,
    # according to the positive/negative values of n(u) − n(v). By
    # construction this embedding is indeed a rectilinear embedding.
    for level in range(1, tree.depth() + 1):
        nodes = list(tree.filter_nodes(lambda x: tree.depth(x) == level))
        for n in nodes:
            parent_id = n.predecessor(tree.identifier)
            parent_node = tree.get_node(parent_id)
            X_u = embedding[parent_id][0]
            Y_u = embedding[parent_id][1]
            embedding[n.identifier] = np.array([
                X_u + 2*(int(parent_node.tag) - int(n.tag)),
                Y_u + 2*(N - abs(int(parent_node.tag) - int(n.tag)))
            ])
            for v in range(2*(N - abs(int(parent_node.tag) - int(n.tag)))):
                segments_X.append((
                    X_u, X_u
                ))
                segments_Y.append((
                    Y_u + v,
                    Y_u + v + 1
                ))
            for v in range(2*abs(int(parent_node.tag) - int(n.tag))):
                if int(parent_node.tag) - int(n.tag) > 0:
                    segments_X.append((
                        X_u + v,
                        X_u + v + 1
                    ))
                else:
                    segments_X.append((
                        X_u - v,
                        X_u - v - 1
                    ))
                segments_Y.append((
                    Y_u + 2*(N - abs(int(parent_node.tag) - int(n.tag))),
                    Y_u + 2*(N - abs(int(parent_node.tag) - int(n.tag)))
                ))
    plt.grid(color='b', linestyle='-', linewidth=0.5)
    plt.xticks([X[0] for X in segments_X])
    for X, Y in zip(segments_X, segments_Y):
        plt.plot(X, Y, 'ro-', markersize=3)
    print('EMBEDDING AS DICTIONARY:')
    pprint(embedding)
    for e in embedding:
        plt.text(embedding[e][0], embedding[e][1], e)
    plt.show()


tree = Tree()
tree.create_node('s', 's')
tree.create_node('r', 'r', parent='s')
tree.create_node('a', 'a', parent='r')
tree.create_node('b', 'b', parent='r')
tree.create_node('c', 'c', parent='a')
tree.create_node('d', 'd', parent='a')
tree.create_node('e', 'e', parent='a')
tree.create_node('f', 'f', parent='b')
tree.create_node('g', 'g', parent='b')
tree.create_node('h', 'h', parent='b')
tree.create_node('z', 'z', parent='r')
tree.create_node('x', 'x', parent='z')
tree.create_node('y', 'y', parent='z')

tree.show()
label_tree(tree)
tree.show()
rectilinear_embedding(tree)
