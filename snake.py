import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
import matplotlib
matplotlib.use('TkAgg')
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
	rows = 20
	w = 500
	def __init__(self,start,dirnx=0, dirny=0, color=(col)):
		self.pos = start
		self.dirnx = 0
		self.dirny = 0
		self.color = color


	def move(self,dirnx,dirny):
		self.dirnx = dirnx
		self.dirny = dirny
		self.pos = (self.pos[0]+ self.dirnx, self.pos[1] + self.dirny)

	def draw(self, surface, eyes=False):
		dis = self.w//self.rows
		i = self.pos[0]
		j = self.pos[1]

		pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
		if eyes:
			center = dis//2
			rad = 3
			circleMiddle = (i*dis+center-rad,j*dis+8)
			circleMiddle2 = (i*dis + dis -rad*2, j*dis+8)
			pygame.draw.circle(surface, WHITE, circleMiddle, rad)
			pygame.draw.circle(surface, WHITE, circleMiddle2, rad)


		

class snake(object):
	body = []
	turns = {}

	def __init__(self, color, pos):
		self.color = color
		self.head = cube(pos)
		self.body.append(self.head)
		self.dirnx = 0
		self.dirny = 0

	def move(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

			keys = pygame.key.get_pressed()

			for key in keys:
				if keys[pygame.K_LEFT]:
					self.dirnx=-1
					self.dirny=0
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

				elif keys[pygame.K_RIGHT]:
					self.dirnx=1
					self.dirny=0
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

				elif keys[pygame.K_UP]:
					self.dirnx=0
					self.dirny=-1
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

				elif keys[pygame.K_DOWN]:
					self.dirnx=0
					self.dirny=1
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

		for i, c in enumerate(self.body):
			p = c.pos[:]
			if p in self.turns:
				turn = self.turns[p]
				c.move(turn[0], turn[1])
				if i==len(self.body)-1:
					self.turns.pop(p)
			
			else:
				if c.dirnx == -1 and c.pos[0] <= 0: 
					c.pos = (0, c.pos[1])
				elif c.dirnx == 1 and c.pos[0] >= c.rows-1: 
					c.pos = (rows-1,c.pos[1])
				elif c.dirny == 1 and c.pos[1] >= c.rows-1: 
					c.pos = (c.pos[0], rows-1)
				elif c.dirny == -1 and c.pos[1] <= 0: 
					c.pos = (c.pos[0], 0)
				else: 
					c.move(c.dirnx, c.dirny)
			

	def reset(self,pos):
		self.head = cube(pos)
		self.body = []
		self.body.append(self.head)
		self.turns = {}
		self.dirnx = 0
		self.dirny = 0

	def addCube(self):
		tail = self.body[-1]
		dx = tail.dirnx
		dy = tail.dirny

		if dx==1 and dy==0:
			self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
		elif dx==-1 and dy==0:
			self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
		elif dx==0 and dy==-1:
			self.body.append(cube((tail.pos[0], tail.pos[1]+1)))
		elif dx==0 and dy==1:
			self.body.append(cube((tail.pos[0], tail.pos[1]-1)))

		self.body[-1].dirnx = dx
		self.body[-1].dirny = dy


	def draw(self, surface):
		for i, c in enumerate(self.body):
			if i==0:
				c.draw(surface, True)
			else:
				c.draw(surface)

def drawGrid(w, rows, surface):
	sizeBetween = w//rows
	x = 0
	y = 0
	for l in range(rows):
		x+= sizeBetween
		y+= sizeBetween

		pygame.draw.line(surface, (WHITE), (x,0), (x,w))
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
		if len(list(filter(lambda z:z.pos == (x,y),positions)))>0:
			continue
		else:
			break
	return (x,y)

def message(subject, content):
	root = tk.Tk()
	root.attributes("-topmost", True)
	root.withdraw()
	messagebox.showinfo(subject, content)
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
	s = snake(RED, (10,10))
	if col==RED:
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
		if s.body[0].pos == snack.pos:
			s.addCube()
			snack = cube(randomSnack(rows, s), color=apple_color)

		for x in range(len(s.body)):
			if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
				print("\nSCORE: ", len(s.body))
				message("GAME OVER", "PLAY AGAIN...")
				s.reset((10,10))
				break


		clearWindow(window)

	pass

main()


pygame.quit()