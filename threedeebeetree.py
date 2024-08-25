from __future__ import annotations
from typing import Generic, TypeVar, Tuple
from dataclasses import dataclass, field

I = TypeVar('I')
Point = Tuple[int, int, int]

@dataclass
class BeeNode:
    """
    Octants are numbered based on binary ordering (> for 0, < for 1)
    octant1: a > x, b > y, c > z
    octant2: a < x, b > y, c > z
    octant3: a > x, b < y, c > z
    octant4: a < x, b < y, c > z
    octant5: a > x, b > y, c < z
    octant6: a < x, b > y, c < z
    octant7: a > x, b < y, c < z
    octant8: a < x, b < y, c < z
    """

    key: Point
    item: I
    subtree_size: int = 1

    def __post_init__(self):
        self.octants = []
        for i in range(8):
            self.octants.append(None)

    def get_child_for_key(self, point: Point) -> BeeNode | None:
        """
        Time complexity:
        Best case: O(1)
        Worst case: O(1)
        """
        if self is None:
            return None
        else:
            return self.octants[self.get_octant(point, self.key)]
    
    def get_octant(self, key, other_key):
        """
        Gets the corresponding octant of a point based on its position relative to another point.

        Time complexity:
        - Best case: O(1)
        - Worst case: O(1)
        """
        octant = 7
        if key[0] > other_key[0]:
            octant -= 1
        if key[1] > other_key[1]:
            octant -= 2
        if key[2] > other_key[2]:
            octant -= 4
        return octant

class ThreeDeeBeeTree(Generic[I]):

    def __init__(self) -> None:
        """
            Initialises an empty 3DBT
        """
        self.root = None
        self.length = 0

    def is_empty(self) -> bool:
        """
            Checks to see if the 3DBT is empty
        """
        return len(self) == 0

    def __len__(self) -> int:
        """ Returns the number of nodes in the tree. """

        return self.length

    def __contains__(self, key: Point) -> bool:
        """
            Checks to see if the key is in the 3DBT
        """
        try:
            self.get_tree_node_by_key(key)
            return True
        except KeyError:
            return False

    def __getitem__(self, key: Point) -> I:
        """
            Attempts to get an item in the tree, it uses the Key to attempt to find it
        """
        node = self.get_tree_node_by_key(key)
        return node.item

    def get_tree_node_by_key(self, key: Point) -> BeeNode:
        """
        Time complexity:
        Best case: O(1) if the key is located at the root node
        Worst case: O(N) where N is the depth of the tree
        """
        return self.get_tree_node_by_key_aux(self.root, key)
    
    def get_tree_node_by_key_aux(self, current: BeeNode, key: Point) -> BeeNode:
        if current is None:
            raise KeyError(key)
        elif current.key == key:
            return current
        else:
            return self.get_tree_node_by_key_aux(current.octants[self.get_octant(key, current.key)], key)

    def __setitem__(self, key: Point, item: I) -> None:
        self.root = self.insert_aux(self.root, key, item)

    def insert_aux(self, current: BeeNode, key: Point, item: I) -> BeeNode:
        """
            Attempts to insert an item into the tree, it uses the Key to insert it

            Time complexity:
            Best case: O(N) where N is the depth of the tree
            Worst case: O(N) 
        """
        if current is None:
            current = BeeNode(key=key, item=item)
            self.length += 1
        elif key != current.key: 
            current.subtree_size += 1
            current.octants[self.get_octant(key, current.key)] = self.insert_aux(current.octants[self.get_octant(key, current.key)], key, item)
        else:
            raise ValueError('Inserting duplicate item')
        return current

    def is_leaf(self, current: BeeNode) -> bool:
        """
        Simple check whether or not the node is a leaf.
        
        Time complexity:
        Best case: O(1)
        Worst case: O(1)
        """
        for i in range(8):
            if current.octants[i] is None:
                continue
            else:
                return False
        return True

    def get_octant(self, key, other_key):
        """
        Gets the corresponding octant of a point based on its position relative to another point.

        Time complexity:
        - Best case: O(1)
        - Worst case: O(1)
        """
        octant = 7
        if key[0] > other_key[0]:
            octant -= 1
        if key[1] > other_key[1]:
            octant -= 2
        if key[2] > other_key[2]:
            octant -= 4
        return octant

if __name__ == "__main__":
    tdbt = ThreeDeeBeeTree()
    tdbt[(3, 3, 3)] = "A"
    tdbt[(1, 5, 2)] = "B"
    tdbt[(4, 3, 1)] = "C"
    tdbt[(5, 4, 0)] = "D"
    print(tdbt.root.get_child_for_key((4, 3, 1)).subtree_size) # 2