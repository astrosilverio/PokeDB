'''
This test suite can be run via: $ python3 -m unittest test_btree
Individual tests can also be specified. Eg:
  $ python3 -m unittest test_btree.TestBTree.test_leaf

'''

import unittest
import btree

class TestBTree(unittest.TestCase):

    def test_leaf(self):
        bt = btree.BTree()
        bt.insert(1, 'one')
        self.assertEqual(str(bt), "Leaf[(1, 'one')]")
        bt.insert(2, 'two')
        self.assertEqual(str(bt), "Leaf[(1, 'one'), (2, 'two')]")

    def test_split_leaf(self):
        bt = btree.BTree()
        bt.insert(1, 'one')
        bt.insert(2, 'two')
        bt.insert(3, 'three')
        self.assertEqual(str(bt), ("[2]"
                                   "\n--Leaf[(1, 'one'), (2, 'two')]"
                                   "\n--Leaf[(3, 'three')]"))

    def test_bubble_up_right_leaf(self):
        bt = btree.BTree()
        bt.insert(1, 'one')
        bt.insert(2, 'two')
        bt.insert(3, 'three')
        bt.insert(4, 'four')
        bt.insert(5, 'five')
        self.assertEqual(str(bt), ("[2, 4]"
                                   "\n--Leaf[(1, 'one'), (2, 'two')]"
                                   "\n--Leaf[(3, 'three'), (4, 'four')]"
                                   "\n--Leaf[(5, 'five')]"))

    def test_bubble_up_left_leaf(self):
        bt = btree.BTree()
        bt.insert(1, 'one')
        bt.insert(2, 'two')
        bt.insert(3, 'three')
        bt.insert(1.5, 'onehalf')
        self.assertEqual(str(bt), ("[1.5, 2]"
                                   "\n--Leaf[(1, 'one'), (1.5, 'onehalf')]"
                                   "\n--Leaf[(2, 'two')]"
                                   "\n--Leaf[(3, 'three')]"))

    def test_bubble_up_node(self):
        bt = btree.BTree()
        bt.insert(1, 'one')
        bt.insert(2, 'two')
        bt.insert(3, 'three')
        bt.insert(1.5, 'onehalf')
        bt.insert(1.25, 'onequarter')
        self.assertEqual(str(bt), ("[1.5]"
                                   "\n--[1.25]"
                                   "\n----Leaf[(1, 'one'), (1.25, 'onequarter')]"
                                   "\n----Leaf[(1.5, 'onehalf')]"
                                   "\n--[2]"
                                   "\n----Leaf[(2, 'two')]"
                                   "\n----Leaf[(3, 'three')]"))

    def test_bubble_up_node_2(self):
        bt = btree.BTree()
        bt.insert(1, 'one')
        bt.insert(2, 'two')
        bt.insert(3, 'three')
        bt.insert(1.5, 'onehalf')
        bt.insert(1.25, 'onequarter')
        bt.insert(1.75, 'onethreequarter')
        self.assertEqual(str(bt), ("[1.5]"
                                   "\n--[1.25]"
                                   "\n----Leaf[(1, 'one'), (1.25, 'onequarter')]"
                                   "\n----Leaf[(1.5, 'onehalf')]"
                                   "\n--[2]"
                                   "\n----Leaf[(1.75, 'onethreequarter'), (2, 'two')]"
                                   "\n----Leaf[(3, 'three')]"))

    def test_search_success(self):
        bt = btree.BTree()
        bt.insert(1, 'one')
        bt.insert(2, 'two')
        bt.insert(3, 'three')
        bt.insert(1.5, 'onehalf')
        bt.insert(1.25, 'onequarter')
        bt.insert(1.75, 'onethreequarter')
        self.assertEqual(bt.search(1.75), 'onethreequarter')

    def test_search_fail(self):
        bt = btree.BTree()
        bt.insert(1, 'one')
        bt.insert(2, 'two')
        bt.insert(3, 'three')
        bt.insert(1.5, 'onehalf')
        bt.insert(1.25, 'onequarter')
        self.assertEqual(bt.search(5), None)

    def test_delete_leaf(self):
        bt = btree.BTree()
        bt.insert(1, 'one')
        bt.insert(2, 'two')
        bt.delete(1)
        self.assertEqual(str(bt), "Leaf[(2, 'two')]")

    def test_delete_no_merge(self):
        bt = btree.BTree()
        bt.insert(1, 'one')
        bt.insert(2, 'two')
        bt.insert(3, 'three')
        bt.insert(4, 'four')
        bt.insert(5, 'five')
        bt.delete(2)
        self.assertEqual(str(bt), ("[3, 4]"
                                   "\n--Leaf[(1, 'one'), (3, 'three')]"
                                   "\n--Leaf[(4, 'four')]"
                                   "\n--Leaf[(5, 'five')]"))

    def test_delete_merge_to_head(self):
        bt = btree.BTree()
        bt.insert(1, 'one')
        bt.insert(2, 'two')
        bt.insert(3, 'three')
        bt.delete(2)
        self.assertEqual(str(bt), ("Leaf[(1, 'one'), (3, 'three')]"))

    def test_delete_merge(self):
        bt = btree.BTree()
        bt.insert(1, 'one')
        bt.insert(2, 'two')
        bt.insert(3, 'three')
        bt.insert(1.5, 'onehalf')
        bt.insert(1.25, 'onequarter')
        bt.delete(1.25)
        self.assertEqual(str(bt), ("[1.5]"
                                   "\n--[1.25]"
                                   "\n----Leaf[(1, 'one'), (1.25, 'onequarter')]"
                                   "\n----Leaf[(1.5, 'onehalf')]"
                                   "\n--[2]"
                                   "\n----Leaf[(2, 'two')]"
                                   "\n----Leaf[(3, 'three')]"))

if __name__ == '__main__':
    unittest.main()
