import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
import matplotlib
matplotlib.use('TkAgg') #to  avoid potential crash
import matplotlib.pyplot as plt
fig = plt.figure()

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
GRAY =  (128,128,128)
MAROON = (128,0,0)
PURPLE = (75,0,130)

print("RULES: Use arrow keys to move\n Touching yourself is a loss of game\n Touching a wall is a loss of game unless you are starting\n Collect as many apples as you can!")
color_user = input("What color would you like for your snake?\n'r' for red\n'g' for green\n'b' for blue\n'y' for yellow\n'm' for maroon\n'p' for purple\n DEFAULT IS GREEN\nEnter: ")
if color_user[0].lower()=='g':
	col = GREEN
elif color_user[0].lower()=='b':
	col = BLUE
elif color_user[0].lower()=='y':
	col = YELLOW
elif color_user[0].lower()=='m':
	col = MAROON
elif color_user[0].lower()=='p':
	col = PURPLE
elif color_user[0].lower()=='r':
	col = RED
else:
	col = GREEN
	
class cube(object):
	rows = 20 #20 rows/columns. Decreasing this number would make it harder and vice versa
	w = 500 #screen width
	def __init__(self,start,dirx=0, diry=0, color=(col)):
		self.pos = start
		self.dirx = 0 #snake begins as still with a movement of 0x and 0y. 
		self.diry = 0
		self.color = color


	def move(self,dirx,diry):
		self.dirx = dirx
		self.diry = diry
		self.pos = (self.pos[0]+ self.dirx, self.pos[1] + self.diry)#updates snake position to move

	def draw(self, surface, eyes=False):
		dis = self.w//self.rows
		i = self.pos[0]
		j = self.pos[1]

		pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
		if eyes:
			center = dis//2
			rad = 3
			circleMiddle = (i*dis+center-rad,j*dis+8)#equation for eyes
			circleMiddle2 = (i*dis + dis -rad*2, j*dis+8)
			pygame.draw.circle(surface, WHITE, circleMiddle, rad)#drawing eyes
			pygame.draw.circle(surface, WHITE, circleMiddle2, rad)


		

class snake(object):
	body = []
	turns = {}

	def __init__(self, color, pos):
		self.color = color
		self.head = cube(pos)
		self.body.append(self.head)
		self.dirx = 0
		self.diry = 0

	def move(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

			keys = pygame.key.get_pressed()

			#user uses arrow keys to move:
			for key in keys:
				if keys[pygame.K_LEFT]:
					self.dirx=-1
					self.diry=0
					self.turns[self.head.pos[:]] = [self.dirx, self.diry]

				elif keys[pygame.K_RIGHT]:
					self.dirx=1
					self.diry=0
					self.turns[self.head.pos[:]] = [self.dirx, self.diry]

				elif keys[pygame.K_UP]:
					self.dirx=0
					self.diry=-1
					self.turns[self.head.pos[:]] = [self.dirx, self.diry]

				elif keys[pygame.K_DOWN]:
					self.dirx=0
					self.diry=1
					self.turns[self.head.pos[:]] = [self.dirx, self.diry]

		for i, c in enumerate(self.body):
			p = c.pos[:]
			if p in self.turns:
				turn = self.turns[p]
				c.move(turn[0], turn[1])
				if i==len(self.body)-1:
					self.turns.pop(p)
			
			else:
				#if snake touches wall with a length longer than 1, game over as the following code makes the snake touch itself
				if c.dirx == -1 and c.pos[0] <= 0: 
					c.pos = (0, c.pos[1])
				elif c.dirx == 1 and c.pos[0] >= c.rows-1: 
					c.pos = (rows-1,c.pos[1])
				elif c.diry == 1 and c.pos[1] >= c.rows-1: 
					c.pos = (c.pos[0], rows-1)
				elif c.diry == -1 and c.pos[1] <= 0: 
					c.pos = (c.pos[0], 0)
				else: 
					c.move(c.dirx, c.diry)#if it is not touching a wall, proceed as usual
			

	def reset(self,pos):
		self.head = cube(pos)
		self.body = []
		self.body.append(self.head)
		self.turns = {}
		self.dirx = 0
		self.diry = 0

	def addCube(self):
		tail = self.body[-1]
		dx = tail.dirx
		dy = tail.diry

		if dx==1 and dy==0:
			self.body.append(cube((tail.pos[0]-1, tail.pos[1]))) #if tail is moving right, add a tail to the end at the left
		elif dx==-1 and dy==0:
			self.body.append(cube((tail.pos[0]+1, tail.pos[1]))) #if tail is moving left, add a tail to the end at the right
		elif dx==0 and dy==-1:
			self.body.append(cube((tail.pos[0], tail.pos[1]+1))) #if tail is moving up, add a tail to the end at the bottom
		elif dx==0 and dy==1:
			self.body.append(cube((tail.pos[0], tail.pos[1]-1))) #if tail is moving down, add a tail to the end at the top

		self.body[-1].dirx = dx
		self.body[-1].diry = dy


	def draw(self, surface):
		for i, c in enumerate(self.body):
			if i==0:
				c.draw(surface, True) #if it's the head, eyes = True
			else:
				c.draw(surface)

def drawGrid(w, rows, surface):
	sizeBetween = w//rows
	x = 0
	y = 0
	for l in range(rows):
		x+= sizeBetween
		y+= sizeBetween

		pygame.draw.line(surface, (WHITE), (x,0), (x,w)) #draw lines on grid
		pygame.draw.line(surface, (WHITE), (0,y), (w,y))


def clearWindow(surface):
	global rows, width, s, snack
	surface.fill(BLACK)
	s.draw(surface)
	snack.draw(surface)
	drawGrid(width, rows, surface)
	pygame.display.update()


def randomSnack(rows, item):
	positions = item.body

	while True:
		x = random.randrange(rows)
		y = random.randrange(rows)
		if len(list(filter(lambda z:z.pos == (x,y),positions)))>0: #generate new snack in a logical place on the grid
			continue
		else:
			break
	return (x,y)

def message(subject, content):
	root = tk.Tk()
	root.attributes("-topmost", True)
	root.withdraw()
	messagebox.showinfo(subject, content) #using tkinter for a message
	try:
		root.destroy()
	except:
		pass

def main():
	global width,height,rows,s,snack,col
	width = 500
	height = 500
	rows = 20
	window = pygame.display.set_mode((width,height))
	s = snake(col, (10,10))
	if col==RED or col==MAROON:
		apple_color = GREEN
	else:
		apple_color = RED
	snack = cube(randomSnack(rows, s), color=apple_color)
	run = True
	clock = pygame.time.Clock()

	while run:
		pygame.time.delay(50)
		clock.tick(10)
		s.move()
		if s.body[0].pos == snack.pos: #add a cube if the snake gets to the snack
			s.addCube()
			snack = cube(randomSnack(rows, s), color=apple_color) #generate new snack

		for x in range(len(s.body)):
			if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])): #if snake touches itself the game is over
				print("\nSCORE: ", len(s.body)) #display user score
				message("GAME OVER", "PLAY AGAIN...")
				s.reset((10,10))
				break


		clearWindow(window)

	pass

main()


pygame.quit()