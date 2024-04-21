from tracemalloc import start
from node import Node
from testcase import data
import time
import copy
def getAllPossiblePosition(posible: list, size):
   ans = []
   if posible[0] + 1 < size:
      ans.append([posible[0]+ 1, posible[1]])
      if posible[1] + 1 < size:
         ans.append([posible[0] + 1, posible[1] + 1])
      if posible[1] - 1 >= 0:
         ans.append([posible[0] + 1, posible[1] - 1])
   if posible[0] - 1 >= 0:
      ans.append([posible[0] -1, posible[1]])
      if posible[1] + 1 < size: 
         ans.append([posible[0] - 1, posible[1] + 1])
      if posible[1] - 1 >= 0:
         ans.append([posible[0] - 1, posible[1] - 1])
   if posible[1] + 1 < size:
      ans.append([posible[0], posible[1] + 1])
   if posible[1] - 1 >= 0:
      ans.append([posible[0], posible[1] - 1])
   return ans

def getHorAndVerPosition(posible: list, size):
   ans = []
   if posible[0] + 1 < size: 
      ans.append([posible[0]+ 1, posible[1]])
   if posible[0] - 1 >= 0:
       ans.append([posible[0] -1, posible[1]])
   if posible[1] + 1 < size:
      ans.append([posible[0], posible[1] + 1])
   if posible[1] - 1 >= 0:
      ans.append([posible[0], posible[1] - 1])
   return ans 

def checkValidPosition(temp: Node, position: list)->bool:
   '''
   Check 
   '''
   i = position[0]
   j = position[1]
   if temp.matrix[i][j] == 2:
      return False
   list1 = getAllPossiblePosition(position, temp.size)
   for item in list1:
      if temp.matrix[item[0]][item[1]] == 2:
          return False
   list2 = getHorAndVerPosition(position, temp.size)
   for item in list2:
      if temp.matrix[item[0]][item[1]] == 1:
         return True

   return  False

def canAssign(temp: Node, row: list, col: list, position: list)->bool:
   #if not(checkValidPosition(temp, position)):
   #   return False
   count = 1
   for i in range(temp.size):
      if temp.matrix[position[0]][i] == 2:
         count += 1
      if count > row[position[0]]:
         return False
   count = 1
   for i in range(temp.size):
      if temp.matrix[i][position[1]] == 2:
         count += 1  
      if count > col[position[1]]:
         return False
   return True

def isGoalState(node: Node, row_req: list, col_req: list) -> bool:
    row_tents = [0] * node.size
    col_tents = [0] * node.size

    # Count the number of tents in each row and column
    for i in range(node.size):
        for j in range(node.size):
            if node.matrix[i][j] == 2:
                row_tents[i] += 1
                col_tents[j] += 1

    # Check if each row has the correct number of tents
    if any(row_tents[i] != row_req[i] for i in range(node.size)):
        return False
   
    # Check if each column has the correct number of tents
    if any(col_tents[i] != col_req[i] for i in range(node.size)):
        return False

    return True


def AstarFunction(node: Node, row_req: list, col_req: list) -> int:
    # Calculate the difference between required tents and actual tents in rows and columns
    row_tents = [0] * node.size
    col_tents = [0] * node.size

    for i in range(node.size):
        for j in range(node.size):
            if node.matrix[i][j] == 2:  # Count tents in rows and columns
                row_tents[i] += 1
                col_tents[j] += 1

    row_penalty = sum(abs(row_req[i] - row_tents[i]) for i in range(node.size))
    col_penalty = sum(abs(col_req[i] - col_tents[i]) for i in range(node.size))
    
    # Additional cost for each step to encourage solution with fewer moves
    return row_penalty + col_penalty + node.step


   
def generateNode(current: Node, row: list, col: list)->list:
   ans = []
   for i in range(current.size):
      for j in range(current.size):
            if current.matrix[i][j] == 0 and canAssign(current, row, col, [i,j]) and checkValidPosition(current, [i,j]):
               temp = Node(copy.deepcopy(current.matrix), current.size, current)
               temp.matrix[i][j] = 2
               temp.countCamp = current.countCamp + 1
               ans.append(temp)
   return ans
class Searching:
   def __init__(self) -> None:
      self.size = int(input("Choose size: "))

      temp = input("Choose testcase: ")
      self.inputTESTCASE = data["size" + str(self.size)]["testcase" +str(temp)]
      
      self.initNode = Node(self.inputTESTCASE["matrix"],self.size,  None)
      self.row = self.inputTESTCASE["idxRow"]
      self.col = self.inputTESTCASE["idxCol"]
      self.path = []
   def getPath(self, endNode: Node)->list:
      ans = []
      temp = endNode
      while temp != None:
         ans.insert(0,temp)
         temp = temp.previous
      return ans
   def bfs(self):
      startTime = time.time()
      queue = [self.initNode]
      visited = [self.initNode]
      while queue:
         currentNode = queue.pop(0)
         
         if isGoalState(currentNode, self.row, self.col):
            self.path = self.getPath(currentNode)

            executeTime = time.time() - startTime
            print("Time for searching: ", str(round(executeTime, 4)))
            print("Total node generated: ", len(visited) + len(queue))
            return
         
         generateNodeList = generateNode(currentNode, self.row, self.col)
         for item in generateNodeList:
            if item not in visited:
               queue.append(item)  
               visited.append(item)             


   def dfs(self):
      startTime = time.time()
      stack = []
      stack.append(self.initNode)
      visited = []
      while len(stack) != 0:
         currentNode = stack.pop(len(stack) - 1)
         visited.append(currentNode)
         if isGoalState(currentNode, self.row, self.col):
            self.path = self.getPath(currentNode)
            executeTime = time.time() - startTime
            print("Time for searching: ", str(round(executeTime, 4)))
            print("Total node generated: ", len(stack) + len(visited)) 
            return
         generateNodeList = generateNode(currentNode, self.row, self.col)
         for item in generateNodeList:
            if item not in visited and item not in stack:
               stack.append(item)
                  

      
   def aStar(self):
      startTime = time.time()
      openList = []
      closeList = []
      heuristic_value = AstarFunction(self.initNode, self.row, self.col)
      openList.append([heuristic_value, self.initNode])
      #openList.append([rule.AstarFunction(self.initNode) ,self.initNode])
      while(len(openList) != 0):
         currentNode = openList.pop(0)
         #print(len(openList), currentNode[1].countCamp)
         closeList.append(currentNode[1])
         if isGoalState(currentNode[1], self.row, self.col):
            self.path =  self.getPath(closeList[len(closeList) - 1])

            executeTime = time.time() - startTime
            print("Time for searching: ", str(round(executeTime, 4)))
            print("Total node: ", len(openList) + len(closeList))
            return
         generateNodeList = generateNode(currentNode[1], self.row, self.col)
         for item in generateNodeList:
            if item not in closeList and item not in (subitem for subitem in openList):
               openList.append([AstarFunction(item, self.row, self.col), item])
         openList.sort(key=lambda x: int(x[0]))

      self.path = self.getPath(closeList[len(closeList) - 1])