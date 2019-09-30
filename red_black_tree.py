#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 15:47:14 2019

@author: songhaoli
"""

"""
Red-Black Tree

A Red-Black Tree is a type of self-balancing binary search tree.
For more details, see https://en.wikipedia.org/wiki/Red–black_tree

We provide an implementation of Red-Balck Tree in Python.
"""

class node:
    def __init__(self, x, c=True):
        self.val = x
        self.red = c
        self.left = None
        self.right = None
        self.parent = None

class RBTree:
    def __init__(self, r=None):
        self.root = r
    
    '''
    Search and return the node that has the value x.
    Return None if x cannot be found.
    '''
    def search(self, x):
        n = self.root
        while n != None and n.val != None and n.val != x:
            if x < n.val:
                n = n.left
            else:
                n = n.right
        if n.val == x:
            return n
        else:
            return None
    
    '''
    Insert the value x.
    '''
    def insert(self, x):
        n = node(x)
        n.left, n.right = node(None, False), node(None, False)
        n.left.parent, n.right.parent = n, n
        # Case 0. The tree is empty
        if self.root == None or self.root.val == None:
            n.red = False
            self.root = n
            return
        # find the correct place of the node, c, in the tree
        c = self.root
        p = None
        while c.val != None:
            p = c
            if n.val < c.val:
                c = c.left
            elif n.val > c.val:
                c = c.right
            else: # x is already in the tree. Do nothing!
                return
        # c.val is None, replace c by n
        n.parent = p
        if n.val < p.val:
            p.left = n
        else:
            p.right = n
        self.insert_fix(n)
    
    '''
    Helper function that fixes the tree at the node n after insertion.
    
    Recall that n is initialized to be red by default.
    n: n
    p: n's parent
    g: n's grandparent
    u: n's uncle
    
    We consider 4 cases:
    
    Case 0.
    'n' is the root. We change the colour of 'n' to black.
    This is taken care of in the method insert(self, x).
    
    Case 1.
    'p' is black. Nothing to do.
    
    Case 2.
    'p' is red, and 'u' is also red.
    Change 'p' and 'u' to be black, and change G to be red.
    Set 'n' = 'g', and repeat if necessary.
    
    Case 3.
    'p' is red, 'u' is black, and 'n' is between 'p' and 'g'.
    'n' to 'g', convert to Case 4.
    
    Case 4.
    'p' is red, 'u' is black, and 'p' is between 'n' and 'g'.
    Rotate 'p' to 'g'.
    '''
    def insert_fix(self, n):
        while n.parent.red == True and n != self.root:
            p = n.parent
            g = p.parent
            if p == g.left:
                uncle = g.right
            else:
                uncle = g.left
            
            if uncle.red:
                '''
                This is Case 2
                     gB                   gR
                    /  \                 /  \
                  pR   uR     =>        pB   uB
                 /  \                  /  \
                nR                    nR
                '''
                p.red = False
                uncle.red = False
                g.red = True
                n = g
            else:
                if (p == g.left and n == p.right) or (p == g.right and n == p.left):
                    '''
                    This is Case 3
                           gg                   gg
                          /                    / 
                         gB                   nB
                        /  \                 /  \
                       pR   uB     =>       pR  gR
                      /  \                 /      \
                         nR                       uB
                    '''
                    n.red = False
                    g.red = True
                    if g == self.root:
                        self.root = n
                    else:
                        gg = g.parent
                        if g == gg.left:
                            gg.left = n
                        else:
                            gg.right = n
                        n.parent = gg
                    if p == g.left and n == p.right: # As shown above
                        n.left, n.right, g.left, p.right = p, g, node(None, False), node(None, False)
                    else: # p == g.right and n == p.left, mirror reflection
                        n.left, n.right, g.right, p.left = g, p, node(None, False), node(None, False)
                    p.parent, g.parent = n, n
                else:
                    '''
                    This is Case 4
                             gg                   gg
                            /                    / 
                          gB                   pB
                         /  \                 /  \
                       pR   uB     =>        nR   gR
                      /  \                     \    \
                     nR  t1                    t1   uB
                    '''
                    g.red = True
                    p.red = False
                    if g == self.root:
                        self.root = p
                    else:
                        gg = g.parent
                        if g == gg.left:
                            gg.left = p
                        else:
                            gg.right = p
                        p.parent = gg
                    if p == g.left and n == p.left: # As shown above
                        t1 = p.right
                        p.left, p.right, n.left, n.right, g.left= n, g, node(None, False), t1, node(None, False)
                    else: # p == g.right and n == p.right, mirror reflection
                        t1 = p.left
                        p.left, p.right, n.left, n.right, g.right= g, n, t1, node(None, False), node(None, False)
                    n.parent, g.parent, t1.parent = p, p, n
        self.root.red = False
    
    '''
    delete the value x, if exists
    '''
    def delete(self, x):
        if (self.root is None) or (x is None): # Nothing to delete
            return
        p, s = None, self.root
        while s.val != x:
            if s.val is None: # We have reached a leaf. We cannot find x in the tree.
                return
            if x > s.val:
                p, s = s, s.right
            elif x < s.val:
                p, s = s, s.left
            else: # s.val == x
                break
        # Now we have s.val == x
        
        # We prepare to remove s.
        if (s.left.val is None) and (s.right.val is None):
            # if both s.left.val and s.right.val are None, replace s with s.left by a random choice
            remove = s
            child = s.left
        elif (s.left.val is None) and (s.right.val is not None): # if s.left.val is None, replace s with s.right
            remove = s
            child = s.right
        elif (s.right.val is None) and (s.left.val is not None): # if s.left.val is None, replace s with s.left
            remove = s
            child = s.left
        else: # if s.left.val and s.right.val:
            # if s has both children, we replace s with n, which is the min of right subtree of s.
            n = s.right
            while n.left.val is not None:
                n = n.left
        
            # Make a copy of n with the color of s
            new = node(n.val, s.red)
            new.left, new.right = s.left, s.right
            s.left.parent, s.right.parent = new, new
            
            if s == self.root: # s is the root, replace self.root with the copy of m.
                self.root = new
            elif (p.left is not None) and (p.left.val == x): # If p.left == s, replace p.left with the copy of m
                p.left = new
            else: # If p.right == s, replace p.right with the copy of m
                p.right = new
            new.parent = p
            remove, child = n, n.right
        
        parent = remove.parent
        '''
        At this point, we have:
        -- remove:
            The node to be removed
        -- child:
            At most one of the two children of 'remove' is not a leaf, 'child' is this child if it exists.
            If both chilren of 'remove' are leaves, 'child' is either of the leaves.
        -- parent:
            The parent of 'remove', which could be None if 'remove' is the root.
        '''
        
        '''
        First, we replace 'remove' by 'child'.
                     parent                         parent
                    /                              /
                 remove              =>         child
                 /    \                             \
              child   t1                            t1
        '''
        if child == remove.left:
            child.right = remove.right
        else:
            child.left = remove.left
        if remove == self.root:
            self.root = child
        elif parent.left == remove: # If parent.left == remove, replace parent.left with 'child'
            parent.left = child
        else: # If parent.right == remove, replace parent.right with 'child'
            parent.right = child
        child.parent = parent
        
        # If child is already a leaf, clear its children.
        if child.val == None:
            child.left, child.right = None, None
        
        if remove.red:
            '''
            If 'remove' is red, nothing more needs to be done.
                     parent                         parent
                    /                              /
                 removeR             =>         child
                 /    \                             \
              child   t1                            t1
            '''
            return
        if remove.red == False and child.red:
            '''
            If 'remove' is black and 'child' is red, change the color of 'child' to black.
                     parent                         parent
                    /                              /
                 removeB             =>         childB
                 /    \                             \
              childR  t1                            t1
            '''
            child.red = False
            return
        '''
        Now we have the difficult case where 'remove' is black and 'child' is black.
        We change the color of 'child' to 'db' and pass it to delete_fix
                     parent                         parent
                    /                              /
                 remove              =>         child,db
                 /    \                             \
              child   t1                            t1
        '''
        child.red = 'db'
        self.delete_fix(child)
        return
    
    '''
    Helper function that fixes the tree after deletion.
    '''
    def delete_fix(self, db):
        while db.red == 'db':
            '''
            Case 1: db is the root.
            Change its color from 'db' to black.
            '''
            if db == self.root:
                db.red = False
                return
            
            '''
            Assign names to the nodes:
                        p
                       / \
                      db  s
                         / \
                        x   y
            '''
            p = db.parent
            if db == p.left:
                s = p.right
                x, y = s.left, s.right
            else:
                s = p.left
                x, y = s.right, s.left
            
            if s.red == False and y.red == True:
                '''
                Case 6: C and D can be either red or black.
                        pC                    sC
                       /  \                  /  \
                      db  sR        =>      pB  yB
                         /  \              /  \
                        xD   yR           dB  xD
                '''
                p.red, s.red, y.red, db.red = False, p.red, False, False
                if p == self.root:
                    self.root = s
                else:
                    g = p.parent
                    if p == g.left:
                        g.left = s 
                    else:
                        g.right = s
                    s.parent = g
                if db == p.left: # as shown above
                    s.left, s.right, p.right = p, y, x
                else: # mirror reflection
                    s.left, s.right, p.left = y, p, x
                p.parent, y.parent, x.parent = s, s, p
                return
            if p.red == True:
                '''
                Case 4:
                     pR                    pB
                    /  \                  /  \
                   db  sB                dB  sR
                '''
                p.red = False
                s.red = True
                db.red = False
                return
            
            else: # p.red == False:
                if s.red == True:
                    '''
                    Case 2: We convert case 2 to case 4, see above
                            pB                    sB
                           /  \                  /  \
                          db  sR        =>      pR  yB
                             /  \              /  \
                            xB   yB           db  xB
                    '''
                    p.red, s.red = True, False
                    if p == self.root:
                        self.root = s
                    else:
                        g = p.parent
                        if p == g.left:
                            g.left = s 
                        else:
                            g.right = s
                        s.parent = g
                    if db == p.left: # as shown above
                        s.left, s.right, s.left.left, s.left.right = p, y, db, x
                    else: # mirror image of the above
                        s.left, s.right, s.right.left, s.right.right = y, p, x, db
                    p.parent, y.parent, db.parent, x.parent = s, s, p, p
                
                elif x.red == False and y.red == False:
                    '''
                    Case 3: 'p' is the new 'db'.
                            pB                    p(db)
                           /  \                  /  \
                          db  sB        =>      dB  sR
                             /  \                  /  \
                            xB   yB               xB  yB
                    '''
                    p.red, db.red, s.red = 'db', False, True
                    db = p
                elif x.red == True and y.red == False:
                    '''
                    Case 5:
                            pB                    pB
                           /  \                  /  \
                          db  sB                dB  xB
                             /  \       =>            \
                            xR   yB                   sR
                              \                      /  \
                              t1                    t1  yB
                    '''
                    s.red, x.red = True, False
                    if db == p.left: # as shown above
                        t1 = x.right
                        p.right, x.right, s.left = x, s, t1
                    else: # mirro reflection
                        t1 = x.left
                        p.left, x.left, s.right = x, s, t1
                    x.parent, s.parent, t1.parent = p, x, s
    
    '''
    check if the binary tree is a binary search tree.
    '''
    def isBST(self):
        def helper(node, l = float('-inf'), u = float('inf')):
            if not node or node.val is None:
                return True
            x = node.val
            if x <= l or x >= u:
                return False

            if not helper(node.right, x, u):
                return False
            if not helper(node.left, l, x):
                return False
            return True
        return helper(self.root)
    
    '''
    check color consistency of leaves
    '''
    def checkLeaves(self):
        def helper(node):
            if not node:
                return True
            if (node.red != True) and (node.red != False):
                # Check if color is red or black.
                return False
            if (node.left or node.right) and node.val is None:
                # Check if a non-leaf node has the value None.
                return False
            if node.val is None and node.red == True:
                # Leaf nodes must be black.
                return False
            if node.red == True and (node.left.red == True or node.right.red == True):
                # The children of a red node must be black.
                return False
            if node.left and node.left.parent != node:
                # The left child's parent must be the node itself.
                return False
            if node.right and node.right.parent != node:
                # The right child's parent must be the node itself.
                return False
            if not helper(node.left):
                return False
            if not helper(node.right):
                return False
            return True
        return helper(self.root)
    
    '''
    Check if the black depth is consitent.
    Return True if every path from the root to a leaf contain the same number of black nodes.
    '''
    def checkBlackDepth(self):
        def helper(node):
            if node is None:
                return 0
            
            left_depth = helper(node.left)
            right_depth = helper(node.right)
            if node.red == True:
                increment = 0
            else:
                increment = 1
            
            if left_depth == -1 or right_depth == -1 or left_depth != right_depth:
                return -1
            else:
                return left_depth + increment
        
        depth = helper(self.root)
        if depth == -1:
            return False
        else:
            return True
    
    '''
    check if the binary tree is a Red-Black Tree.
    '''
    def isRBT(self):
        if not self.isBST():
            return False
        if not self.checkLeaves():
            return False
        if not self.checkBlackDepth():
            return False
        return True
        # return self.isBST() and self.checkLeaves() and self.checkBlackDepth()

'''
Convert a red-black tree to a list.
'''
def RBTToList(n) -> list:
    if n is None or n.val is None:
        return []
    return RBTToList(n.left) + [n.val] + RBTToList(n.right)

'''
Provide a quick way to initialize a red-black tree.
Note: This function does not check the validity.

False = Black
True = Red
[(3,False),(1,False),(5,True),(None,False),(None,False),(4,False),(6,False)] will initialize to the binary tree of depth 3:
      3B
    _/  \__
  1B        5R
 /  \     _/  \_
NB  NB  4B      6B
       /  \    /  \
      NB  NB  NB  NB
'''
def ListToBST(rbt_list: list) -> RBTree:
    
    # The list is empty
    if len(rbt_list) == 0:
        return RBTree(node(None, False))
    
    # There is only 1 element.
    if len(rbt_list) == 1:
        n = node(rbt_list[0][0], rbt_list[0][1])
        n.left, n.right = node(None, False), node(None, False)
        n.left.parent, n.right.parent = n, n
        return RBTree(n)
    
    # There are at least 2 elements.
    n_list = [None]*len(rbt_list)
    for i, x in enumerate(rbt_list):
        if x is not None:
            n_list[i] = node(x[0],x[1])
    
    # last_level is the index for last node in the second last row
    last_level = int(bin(len(n_list))[3:], 2)
    for i, n in enumerate(rbt_list[:last_level]):
        n_list[i].left = n_list[i*2+1]
        n_list[i*2+1].parent = n_list[i]
        n_list[i].right = n_list[i*2+2]
        n_list[i*2+2].parent = n_list[i]
    
    # Assign the leaves to be None with colour Black
    for n in n_list[last_level:]:
        if n.val != None:
            if n.left == None:
                n.left = node(None, False)
                n.left.parent = n
            if n.right == None:
                n.right = node(None, False)
                n.right.parent = n
    
    return RBTree(n_list[0])