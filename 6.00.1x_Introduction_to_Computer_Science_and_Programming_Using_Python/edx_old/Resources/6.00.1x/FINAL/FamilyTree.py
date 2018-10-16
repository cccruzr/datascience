class Member(object):
    def __init__(self, founder):
        """ 
        founder: string
        Initializes a member. 
        Name is the string of name of this node,
        parent is None, and no children
        """        
        self.name = founder
        self.parent = None         
        self.children = []    

    def __str__(self):
        return self.name    

    def add_parent(self, mother):
        """
        mother: Member
        Sets the parent of this node to the `mother` Member node
        """
        self.parent = mother   

    def get_parent(self):
        """
        Returns the parent Member node of this Member
        """
        return self.parent 

    def is_parent(self, mother):
        """
        mother: Member
        Returns: Boolean, whether or not `mother` is the 
        parent of this Member
        """
        return self.parent == mother  

    def add_child(self, child):
        """
        child: Member
        Adds another child Member node to this Member
        """
        self.children.append(child)   

    def is_child(self, child):
        """
        child: Member
        Returns: Boolean, whether or not `child` is a
        child of this Member
        """
        return child in self.children 


class Family(object):
    def __init__(self, founder):
        """ 
        Initialize with string of name of oldest ancestor

        Keyword arguments:
        founder -- string of name of oldest ancestor
        """

        self.names_to_nodes = {}
        self.root = Member(founder)    
        self.names_to_nodes[founder] = self.root   

    def set_children(self, mother, list_of_children):
        """
        Set all children of the mother. 

        Keyword arguments: 
        mother -- mother's name as a string
        list_of_children -- children names as strings
        """
        # convert name to Member node (should check for validity)
        mom_node = self.names_to_nodes[mother]   
        # add each child
        for c in list_of_children:           
            # create Member node for a child   
            c_member = Member(c)               
            # remember its name to node mapping
            self.names_to_nodes[c] = c_member    
            # set child's parent
            c_member.add_parent(mom_node)        
            # set the parent's child
            mom_node.add_child(c_member)         
    
    def is_parent(self, mother, kid):
        """
        Returns True or False whether mother is parent of kid. 

        Keyword arguments: 
        mother -- string of mother's name
        kid -- string of kid's name
        """
        mom_node = self.names_to_nodes[mother]
        child_node = self.names_to_nodes[kid]
        return child_node.is_parent(mom_node)   

    def is_child(self, kid, mother):
        """
        Returns True or False whether kid is child of mother. 

        Keyword arguments: 
        kid -- string of kid's name
        mother -- string of mother's name
        """        
        mom_node = self.names_to_nodes[mother]   
        child_node = self.names_to_nodes[kid]
        return mom_node.is_child(child_node)

    def is_descendent(self,b,a):
        
        if b == self.root.name:
            return False
        if self.is_parent(a,b):
            return True
        
        else:
            return self.is_descendent(self.names_to_nodes[b].parent.name,a)
      
    def distance_to_root(self,a):
        
        if a == self.root.name:
            return -1
        if self.names_to_nodes[a].parent.name == self.root.name:
            return 0
        else:
            return 1 + self.distance_to_root(self.names_to_nodes[a].parent.name)
        
    def common_ancestor(self,a,b):
        
        if self.names_to_nodes[a] == self.names_to_nodes[b]:
            
            return a
        
        if self.names_to_nodes[a].parent == self.names_to_nodes[b].parent:
            return self.names_to_nodes[a].parent.name
        
        else:
            if self.distance_to_root(a) < self.distance_to_root(b):
                return self.common_ancestor(a,self.names_to_nodes[b].parent.name)
            else:
                return self.common_ancestor(self.names_to_nodes[a].parent.name,b)
                 
    
    
    def cousin(self, a, b):
        """
        Returns a tuple of (the cousin type, degree removed) 

        cousin type is an integer that is -1 if a and b
        are the same node or if one is the direct descendent 
        of the other.  Otherwise, cousin type is 0 or greater,
        representing the shorter distance to their common 
        ancestor as described in the exercises above.

        degree removed is the distance to the common ancestor

        Keyword arguments: 
        a -- string that is the name of a
        b -- string that is the name of b
        """
        
        
        if self.names_to_nodes[a] == self.names_to_nodes[b] or self.is_descendent(a,b) or self.is_descendent(b,a):
            cousinType = -1
            
            degreeRemoved = max([self.distance_to_root(a),self.distance_to_root(b)])-min([self.distance_to_root(a),self.distance_to_root(b)])
        
        else:
            
            if self.distance_to_root(a) < self.distance_to_root(b):
                
                cousinType = self.distance_to_root(a) - (1 + self.distance_to_root(self.common_ancestor(a,b)))
                degreeRemoved = self.distance_to_root(b) - self.distance_to_root(a)
            else:
                cousinType = self.distance_to_root(b) - (1 + self.distance_to_root(self.common_ancestor(a,b)))
                degreeRemoved = self.distance_to_root(a)- self.distance_to_root(b)
            
        
        return (cousinType, degreeRemoved)


f = Family("a")
f.set_children("a", ["b", "c"])
f.set_children("b", ["d", "e"])
f.set_children("c", ["f", "g"])

f.set_children("d", ["h", "i"])
f.set_children("e", ["j", "k"])
f.set_children("f", ["l", "m"])
f.set_children("g", ["n", "o", "p", "q"])

words = ["zeroth", "first", "second", "third", "fourth", "fifth", "non"]

## These are your test cases. 

## The first test case should print out:
## 'b' is a zeroth cousin 0 removed from 'c'
t, r = f.cousin("b", "c")
print "'b' is a", words[t],"cousin", r, "removed from 'c'"

## For the remaining test cases, use the graph to figure out what should 
## be printed, and make sure that your code prints out the appropriate values.

t, r = f.cousin("d", "f")
print "'d' is a", words[t],"cousin", r, "removed from 'f'"

t, r = f.cousin("i", "n")
print "'i' is a", words[t],"cousin", r, "removed from 'n'"

t, r = f.cousin("q", "e")
print "'q' is a", words[t], "cousin", r, "removed from 'e'"

t, r = f.cousin("h", "c")
print "'h' is a", words[t], "cousin", r, "removed from 'c'"

t, r = f.cousin("h", "a")
print "'h' is a", words[t], "cousin", r, "removed from 'a'"

t, r = f.cousin("h", "h")
print "'h' is a", words[t], "cousin", r, "removed from 'h'"

t, r = f.cousin("a", "a")
print "'a' is a", words[t], "cousin", r, "removed from 'a'"

t, r = f.cousin("a", "h")
print "'a' is a", words[t], "cousin", r, "removed from 'h'"