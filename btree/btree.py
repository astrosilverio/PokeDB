from math import ceil

class BTree:
    """Wrapper for BTree data structure.

    Basically just a pointer to the head node of the tree.
    """
    def __init__(self):
        self.head = None

    def __str__(self):
        return str(self.head) if self.head else "Empty Tree"

    def insert(self, k, v):
        if self.head is None:
            self.head = BTreeLeaf(parent=self, keys=[k], data={k: v})
        else:
            self.head.insert(k, v)

    def search(self, k):
        '''Returns value associated with key, or None if key not found.'''
        return self.head.search(k)

    def delete(self, k):
        '''Returns none if record not in tree, else if successfully deleted, returns record.'''
        return self.head.delete(k)


class BTreeNode:
    """2-3 Tree Node."""
    bfactor = 2

    def __init__(self, parent, keys, pointers=[], *args, **kwargs):
        self.parent = parent
        self.keys = keys
        self.pointers = pointers

    def __str__(self, level=1):
        res = str(self.keys)
        return res + ''.join(['\n' + level * '--' + pointer.__str__(level=level+1) for pointer in self.pointers])

    def is_head(self):
        return isinstance(self.parent, BTree)

    def has_overflowed(self):
        return len(self.keys) > self.bfactor

    def _split(self):
        half = ceil(len(self.keys)/2.0)
        left_keys, right_keys = self.keys[:half-1], self.keys[half:]
        # Left stops 1 short because in internal nodes, median is promoted.
        left = BTreeNode(parent=self, keys=left_keys,
                         pointers=self.pointers[:half])
        for pointers in left.pointers:
            pointers.parent = left
        right = BTreeNode(parent=self, keys=right_keys,
                         pointers=self.pointers[half:])
        for pointers in right.pointers:
            pointers.parent = right
        self.keys = [self.keys[half-1]]  # Promotion happens here.
        self.pointers = [left, right]

    def _get_insertion_position(self, k):
        # Can be improved via binary search.
        pos = 0
        while pos < len(self.keys) and k > self.keys[pos]:
            pos += 1
        return pos

    def bubble_up(self, child):
        '''Merge child node/leaf into self, and bubble up further if necessary.'''
        for pointer in child.pointers:
            pointer.parent = self

        pos = self._get_insertion_position(child.keys[0])
        self.keys = self.keys[:pos] + child.keys + self.keys[pos:]
        self.pointers = self.pointers[:pos] + child.pointers + self.pointers[pos + 1:]
        # We skip one pointer here, because that's the one that is bubbling up from.

        if self.has_overflowed():
            self._split()
            if not self.is_head():
                self.parent.bubble_up(self)

    def insert(self, k, v):
        assert k not in self.keys, f"Duplicate key not allowed: {k}"
        pos = self._get_insertion_position(k)
        self.pointers[pos].insert(k, v)

    def search(self, k):
        pos = self._get_insertion_position(k)
        return self.pointers[pos].search(k)

    def delete(self, k):
        pos = self._get_insertion_position(k)
        return self.pointers[pos].delete(k)


class BTreeLeaf(BTreeNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = kwargs.pop('data', None)

    def __str__(self, level=0):
        return "Leaf" + str([(key, self.data[key]) for key in self.keys])

    def insert(self, k, v):
        assert k not in self.keys, f"Duplicate key not allowed: {k}"
        self.data[k] = v
        self.keys.append(k)
        self.keys.sort()
        if self.has_overflowed():
            half = ceil(len(self.keys)/2.0)
            left_keys, right_keys = self.keys[:half], self.keys[half:]
            new_node = BTreeNode(parent=self.parent, keys=[left_keys[-1]])
            # new_node's parent irrelevant if it gets bubbled up since
            # its parent will just co-opt the keys and pointers and dump new_node.
            # But if it might need to become the new head, in which case it needs
            # to inherit None as a parent.
            left = BTreeLeaf(parent=new_node, keys=left_keys,
                             data={k: self.data[k] for k in left_keys})
            right = BTreeLeaf(parent=new_node, keys=right_keys,
                              data={k: self.data[k] for k in right_keys})
            new_node.pointers=[left, right]
            if not self.is_head():
                self.parent.bubble_up(new_node)
            else:
                self.parent.head = new_node

    def search(self, k):
        return self.data.get(k, None)

    def delete(self, k):
        if k not in self.keys:
            return None

        del self.data[k]
        self.keys.remove(k)

        if self.is_head():
            return k

        pos = self.parent._get_insertion_position(k)
        peer_leaf = self.parent.pointers[pos + 1]
        # The peer leaf will be used to decide if deleting causes a merge.
        # Since the data for an internal node is stored in the left leaf,
        # its peer leaf is to the right, ie pos + 1.

        # Deletions from the right most leaf will never require merging.
        if pos == self.bfactor:
            return k

        del self.parent.keys[pos]
        del self.parent.pointers[pos + 1]

        # Make a huge leaf from the original leaf and its peer
        self.keys += peer_leaf.keys
        self.data.update(peer_leaf.data)

        # If huge leaf overflows, split and bubble up new node.
        if self.has_overflowed():
            half = ceil(len(self.keys)/2.0)
            left_keys, right_keys = self.keys[:half], self.keys[half:]
            new_node = BTreeNode(parent=self.parent, keys=[left_keys[-1]])
            left = BTreeLeaf(parent=new_node, keys=left_keys,
                             data={k: self.data[k] for k in left_keys})
            right = BTreeLeaf(parent=new_node, keys=right_keys,
                              data={k: self.data[k] for k in right_keys})
            new_node.pointers=[left, right]
            if not self.is_head():
                self.parent.bubble_up(new_node)
            else:
                self.parent.head = new_node

        # else we have one large merged leaf.
        else:
            # when the merge removes the head node, reattach leaf at the head.
            if self.parent.is_head() and len(self.parent.keys) == 0:
                self.parent.parent.head = self
            else:  # merge leaf into parent
                self.parent.pointers[pos] = self
        return k
