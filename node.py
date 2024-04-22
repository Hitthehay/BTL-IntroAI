import copy
class Node:
   def __init__(self, matrix: list, size, previous: None) -> None:
      self.size = size
      self.matrix = copy.deepcopy(matrix)
      self.previous = previous
      if (self.previous == None):
         self.countCamp = 0
      else: 
         self.countCamp = self.previous.countCamp + 1
   