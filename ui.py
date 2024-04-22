from numpy import matrix
import pygame
from algorithm import *
import tkinter as tk  
widthscreen = 800
heightscreen = 600

khaki = (240,230,140)
slate_gray = (112,128,144)
white = (255,255,255)
brown = (165,42,42)
darkgreen = (0,100,0)
green = (152,251,152)
red = (255,0,0)
black = (0,0,0)
pygame.init()

font1 = pygame.font.Font(None,30)
font_large = pygame.font.Font(None, 40)

clock = pygame.time.Clock()

length_between_2_button = 5

from matplotlib.backend_bases import LocationEvent
import pygame,sys

class Button:
	'''
	Create button for UI design
	'''
	def __init__(self, locaton: list, width, height, text):

		self.width = width
		height = height
		self.locaton = locaton
		self.rect =  pygame.Rect( locaton, (width, height))
		self.rect.topleft = self.locaton
		self.buttonColor = (14, 70, 163)
		self.clicked = False
		font1 = pygame.font.Font(None,30)
		self.fontButton = font1.render(text, True, (14, 70, 163))
		self.action = False
	def draw(self, surface):
		self.action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				self.action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		if self.action == True:
			self.buttonColor = (154, 200, 205)
			pygame.draw.rect(surface, self.buttonColor,self.rect)
		else: 
			self.buttonColor = (154, 200, 205)
			pygame.draw.rect(surface, self.buttonColor,self.rect)
		
		
		surface.blit(self.fontButton, (self.locaton[0] + 15, self.locaton[1] + 15))


		return self.action


class CampButton:
   def __init__(self, display_surface,location: list, width, height) -> None:
      self.display_surface = display_surface
      self.location = location #()
      self.width = width
      self.press = False
      self.height = height
      self.button = pygame.Rect(location, (width, height))
      self.buttonColor = white
      self.clicked = False
      self.setCamp = False
      self.action = False
   def draw(self):
      self.action = False
      pos = pygame.mouse.get_pos()
      if self.button.collidepoint(pos):
         if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.clicked = True
            self.action = True
      if pygame.mouse.get_pressed()[0] == 0:
         self.clicked = False
      return self.action
   def display(self):
      if self.setCamp:
         self.displayCamp()
      else:
         self.displayNULL()

   def displayCamp(self):
        pygame.draw.rect(self.display_surface, green, self.button)
        tent_color = slate_gray if self.press else darkgreen  # Change the color when pressed
        pygame.draw.polygon(self.display_surface, tent_color, [
            (self.location[0] + self.width * 0.25, self.location[1] + self.height * 0.75),
            (self.location[0] + self.width * 0.5, self.location[1] + self.height * 0.25),
            (self.location[0] + self.width * 0.75, self.location[1] + self.height * 0.75),
        ])
        # Add more details or a shadow for a 3D effect
        # ...

   def displayNULL(self):
        # Use a subtle fill color for empty cells
        empty_color = khaki if self.press else white
        pygame.draw.rect(self.display_surface, empty_color, self.button)
        # Optionally, draw a soft border
        pygame.draw.rect(self.display_surface, slate_gray, self.button, 1)


class TreeButton:
   def __init__(self, display_surface, location, width, height) -> None:
      self.display_surface = display_surface
      self.location = location
      self.width = width
      self.height = height
      self.button = pygame.Rect(location, (width, height))
   def display(self):
        # Fill the button background
        pygame.draw.rect(self.display_surface, green, self.button)
        # Draw the tree trunk
        trunk_rect = pygame.Rect(
            (self.location[0] + self.width * 0.4, self.location[1] + self.height * 0.6),
            (self.width * 0.2, self.height * 0.4)
        )
        pygame.draw.rect(self.display_surface, brown, trunk_rect)
        # Draw the tree canopy
        canopy_ellipse = pygame.Rect(
            (self.location[0] + self.width * 0.2, self.location[1] + self.height * 0.1),
            (self.width * 0.6, self.height * 0.6)
        )
        pygame.draw.ellipse(self.display_surface, darkgreen, canopy_ellipse)


class GameControl:
   def __init__(self, data, path, size, initLocation, width, height) -> None:
      self.path = path
      self.widthEle = width
      self.heightEle = height
      self.display_surface = pygame.display.set_mode((widthscreen, heightscreen))
      self.display_surface.fill((255, 255, 255))
      pygame.display.set_caption("Tent-puzzle")
      img = pygame.image.load("shin.jpg")
      pygame.display.set_icon(img)
      self.size = size
      self.row = data["idxRow"]
      self.col = data["idxCol"]
      self.initLocation = initLocation
      self.interfaceMatrix = []
      self.step = 0
      self.setData(self.path[0])
      

      self.nextStep = Button((600,500), 75, 50, "next")
      self.previousStep = Button( (475,500), 116, 50, "previous")

       
   def setData(self, temp):
      self.matrix = temp
      self.interfaceMatrix = []
      for i in range(self.size):
         for j in range(self.size):
            if j == 0:
               if(self.matrix.matrix[i][j] == 0 or self.matrix.matrix[i][j] == 2):
                  self.interfaceMatrix.append([CampButton(self.display_surface,(self.initLocation[0] + j *(self.widthEle + length_between_2_button), self.initLocation[1] + i *(self.heightEle + length_between_2_button)), self.widthEle,self.heightEle)])
               else:
                  self.interfaceMatrix.append([TreeButton(self.display_surface, (self.initLocation[0] + j *(self.widthEle + length_between_2_button), self.initLocation[1] + i *(self.heightEle + length_between_2_button)), self.widthEle,self.heightEle)])
            else:
                  if(self.matrix.matrix[i][j] == 0 or self.matrix.matrix[i][j] == 2):
                     self.interfaceMatrix[i].append(CampButton(self.display_surface, (self.initLocation[0] + j *(self.widthEle + length_between_2_button), self.initLocation[1] + i *(self.heightEle + length_between_2_button)), self.widthEle,self.heightEle))
                  else:
                     self.interfaceMatrix[i].append(TreeButton(self.display_surface, (self.initLocation[0] + j *(self.widthEle + length_between_2_button), self.initLocation[1] + i *(self.heightEle + length_between_2_button)), self.widthEle,self.heightEle))       
            if self.matrix.matrix[i][j] == 2:
               self.interfaceMatrix[i][j].setCamp = True

   def changeData(self, temp):
      for i in range(self.size):
         for j in range(self.size):
            if temp.matrix[i][j] == 0:
               self.interfaceMatrix[i][j].setCamp = False
            elif temp.matrix[i][j] == 2: 
               self.interfaceMatrix[i][j].setCamp = True

   def display(self):
      title = font_large.render("Tents Puzzle", True, (30, 3, 66))
      self.display_surface.blit(title, (310, 75))
      stepDispay = font1.render("Step: " + str(self.step), True, (14, 70, 163))
      self.display_surface.blit(stepDispay, (50,50))
      for i in range(self.size):
         if not(self.checkCol(i)):
            autoTurnOn =font1.render(str(self.col[i]) , True, red)          
         else: 
            autoTurnOn =font1.render(str(self.col[i]) , True, black)
         self.display_surface.blit(autoTurnOn, (300 + i*(self.widthEle + length_between_2_button) + self.widthEle/3, 125))

      for i in range(self.size):
         if not(self.checkRow(i)):
            autoTurnOn =font1.render(str(self.row[i]) , True, red)
         else:
            autoTurnOn =font1.render(str(self.row[i]) , True, black)
         self.display_surface.blit(autoTurnOn, (275, 150 + i*(self.heightEle + length_between_2_button) + self.heightEle/3))
      
      for i in range(self.size):
         for j in range(self.size):
            if isinstance(self.interfaceMatrix[i][j], CampButton):
               if self.interfaceMatrix[i][j].draw():
                  self.interfaceMatrix[i][j].setCamp = not(self.interfaceMatrix[i][j].setCamp)
                  print(i,j)
            self.interfaceMatrix[i][j].display()
      if self.nextStep.draw(self.display_surface):
         self.next()
      elif self.previousStep.draw(self.display_surface):
         self.previous()

         '''
         
            if isinstance(self.interfaceMatrix[i][j], CampButton):
               if self.interfaceMatrix[i][j].setCamp:
                  print(i,j)
         '''
   def next(self):
      if self.step < len(self.path) - 1:
         self.step += 1
         self.changeData(self.path[self.step])
         self.display()
         pygame.display.update()
   
   def previous(self):
      if self.step > 0:
         self.step -= 1
         self.changeData(self.path[self.step])
         self.display()
         pygame.display.update()

         
   def checkCol(self, temp):
      '''
      return True if no col error, else return False
      '''
      count = 0
      for j in range(self.size):
         if isinstance( self.interfaceMatrix[j][temp], CampButton):
            if self.interfaceMatrix[j][temp].setCamp:
               count += 1
            if count > self.col[temp]:
               return False
      return True

   def checkRow(self, temp):
      '''
      return True if no row error, else return False
      '''
      count = 0
      for j in range(self.size):
         if isinstance( self.interfaceMatrix[temp][j], CampButton):
            if self.interfaceMatrix[temp][j].setCamp:
               count += 1
            if count > self.row[temp]:
               return False
      return True




if __name__ == "__main__":
   temp = Searching()
   choose = int(input("Choose dfs: 1 or aStar: 2 => "))
   if choose == 1:
      print("Solving DFS. Please wait...")
      temp.dfs()
   elif choose == 2:
      temp.aStar()
      print("Solving A*. Please wait...")
   head = GameControl(temp.inputTESTCASE,temp.path, temp.size, (300,150), 30, 30)
   running = True
   while running:
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            running ==False
            pygame.quit()
            exit(0)
      head.display_surface.fill((225, 247, 245))
      head.display()
      
      pygame.display.update()

