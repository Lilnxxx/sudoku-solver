import pygame
import copy
import requests
from bs4 import BeautifulSoup
pygame.font.init()

# Total window
screen = pygame.display.set_mode((610, 600))
pygame.display.set_caption("SUDOKU SOLVER USING BACKTRACKING")
# img = pygame.image.load('icon.png')
# pygame.display.set_icon(img)
time_rate=0;raise_err_2=300
mins=0
hrs=0
f=True
x = 0
y = 0
dif = 500 / 9
val = 0
level_value =1;you_lose=False
# Default Sudoku Board.
grid =[
		[7, 8, 0, 4, 0, 0, 1, 2, 0],
		[6, 0, 0, 0, 7, 5, 0, 0, 9],
		[0, 0, 0, 6, 0, 1, 0, 7, 8],
		[0, 0, 7, 0, 4, 0, 2, 6, 0],
		[0, 0, 1, 0, 5, 0, 9, 3, 0],
		[9, 0, 4, 0, 6, 0, 0, 0, 5],
		[0, 7, 0, 3, 0, 0, 0, 1, 2],
		[1, 2, 0, 0, 0, 7, 4, 0, 0],
		[0, 4, 9, 2, 0, 6, 0, 0, 7]
	]
grid_2nd =copy.deepcopy(grid)

# Load test fonts for future use
font1 = pygame.font.SysFont("comicsans", 40)
font2 = pygame.font.SysFont("comicsans", 20)
font3 = pygame.font.SysFont("comicsans", 18)

clock = pygame.time.Clock()

def new_grid(l=1):
    print(l)
    url ="https://five.websudoku.com/?level="+str(l)
    r = requests.get(url)
    htmlcontent= r.content
    soup = BeautifulSoup(htmlcontent,"html.parser")
    str1 =str(soup.find_all(id='editmask'))
    str2 =str(soup.find_all(id='cheat'))
    str1=str1[43:124]
    str2=str2[53:134]
    q1=[[],[],[],[],[],[],[],[],[]]
    m=0
    for i in range(9):
        for j in range(9):
            if(str1[m+j]=='0'):q1[j].append(int(str2[m+j]))
            else: q1[j].append(0)
        m+=9
    return q1


def get_cord(pos):
	global x
	x = pos[0]//dif
	global y
	y = pos[1]//dif

# Highlight the cell selected
def draw_box():
	global x,y
	if(x>8 or x<0):x=0
	if(y>8 or y<0):y=0
	# if(grid_2nd[int(x)][int(y)]!=0):return
	for i in range(2):
		pygame.draw.line(screen, (255, 0, 0), (x * dif-3, (y + i)*dif), (x * dif + dif + 3, (y + i)*dif), 7)
		pygame.draw.line(screen, (255, 0, 0), ( (x + i)* dif, y * dif ), ((x + i) * dif, y * dif + dif), 7)

# Function to draw required lines for making Sudoku grid		
def draw():
	# Draw the lines
	for i in range (9):
		for j in range (9):
			if grid[i][j]!= 0:
				# Fill blue color in already numbered grid
				if grid_2nd[i][j]!=0:
					pygame.draw.rect(screen, (0, 183, 153), (i * dif, j * dif, dif + 1, dif + 1))
					text1 = font1.render(str(grid_2nd[i][j]), 1, (0, 0, 0))
					screen.blit(text1, (i * dif + 15, j * dif + 0))
				# Fill grid with default numbers specified
				# if grid_2nd[i][j]!=0:
				else:
					text1 = font1.render(str(grid[i][j]), 1, (0, 0, 0))
					screen.blit(text1, (i * dif + 15, j * dif + 0))
	# Draw lines horizontally and verticallyto form grid		
	for i in range(10):
		if i % 3 == 0 :
			thick = 7
		else:
			thick = 1
		pygame.draw.line(screen, (0, 0, 0), (0, i * dif), (500, i * dif), thick)
		pygame.draw.line(screen, (0, 0, 0), (i * dif, 0), (i * dif, 500), thick)	

# Fill value entered in cell	
def draw_val(val):
	text1 = font1.render(str(val), 1, (0, 0, 0))
	screen.blit(text1, (x * dif + 15, y * dif + 15))

# Raise error when wrong value entered
def raise_error1():
	global grid,error
	text1 = font1.render("WRONG !!!", 1, (0, 0, 0))
	screen.blit(text1, (190, 515))
	grid =copy.deepcopy(grid_2nd)
	# print(" error is here ",error)
		
def raise_error2():
	global raise_err_2,start_clock,grid,mins,hrs,you_lose
	if(raise_err_2>420):
		grid =copy.deepcopy(grid_2nd)
		start_clock=False;raise_err_2=300;mins=0;hrs=0
		pygame.draw.rect(screen, (255,255,255), (0,0,500,600))
		text1 = font1.render("YOU LOSE ,RESET GAME", 1, (255, 0, 0))
		screen.blit(text1, (10, 515))
		you_lose=True 
		return
	text1 = font1.render("X", 1, (255, 0, 0))
	screen.blit(text1, (raise_err_2-290, 505));raise_err_2+=35

# Check if the value entered in board is valid
def valid(m, i, j, val):
	for it in range(9):
		if m[i][it]== val:
			return False
		if m[it][j]== val:
			return False
	it = i//3
	jt = j//3
	for i in range(it * 3, it * 3 + 3):
		for j in range (jt * 3, jt * 3 + 3):
			if m[i][j]== val:
				return False
	return True

# Solves the sudoku board using Backtracking Algorithm
def solve(grid, i, j):
	while grid[i][j]!= 0:
		if i<8:
			i+= 1
		elif i == 8 and j<8:
			i = 0
			j+= 1
		elif i == 8 and j == 8:
			return True
	pygame.event.pump()
	for it in range(1, 10):
		if valid(grid, i, j, it)== True:
			grid[i][j]= it
			global x, y
			x = i
			y = j
			# screen.fill((255, 255, 255))
			pygame.draw.rect(screen, (255, 255, 255), (0,0,500,600))
			draw()
			draw_box()
			pygame.display.update()
			pygame.time.delay(20)
			if solve(grid, i, j)== 1:
				return True
			else:
				grid[i][j]= 0
			# white color background\
			screen.fill((255, 255, 255))
			# pygame.draw.rect(screen, (255, 255, 255), (0,0,500,600))		
			draw()
			draw_box()
			pygame.display.update()
			if level_value==1:pygame.time.delay(50)
			else:pygame.time.delay(0)
	return False

def is_full(grid):
	for i in range(9):
		for j in range(9):
			if(grid[i][j]==0):return 0

	return 1
# Display instruction for the game
def instruction():
	pygame.draw.rect(screen, (255,255,255), (10,570,560,60))
	text1 = font3.render("FILL VAL &  ENTER TO VISUALIZE | D-RESET | R-EMPTY ", 1, (0, 0, 0))
	screen.blit(text1, (10, 570))	

# Display options when solved
def result():
	text1 = font1.render("FINISHED PRESS R or D", 1, (0, 0, 0))
	screen.blit(text1, (20, 570))

def side_buttons():
	pygame.draw.rect(screen,(196,214,214),[520,100,80,40]) #start
	pygame.draw.rect(screen,(196,214,214),[520,150,80,40]) #new
	pygame.draw.rect(screen,(196,214,214),[520,200,80,40]) #reset
	pygame.draw.rect(screen,(196,214,214),[520,250,80,40]) #solve
	pygame.draw.rect(screen,(196,214,214),[520,300,80,40]) #level
	# pygame.draw.rect(screen,(196,214,214),[520,350,80,40]) #help

	# text1 = font1.render(f"{time_rate}:{time_rate}", 0, (0))
	# screen.blit(text1, (527,17))
	text1 = font3.render("START", 0, (0))
	screen.blit(text1, (527,107))
	text1 = font3.render("NEW", 1, (0, 0, 0))
	screen.blit(text1, (527,157))
	text1 = font3.render("RESET", 1, (0, 0, 0))
	screen.blit(text1, (527,207))
	text1 = font3.render("SOLVE", 1, (0, 0, 0))
	screen.blit(text1, (527,257))
	text1 = font3.render("LEVEL", 1, (0, 0, 0))
	screen.blit(text1, (527,307))

def start_time(secs):
	global mins,time_rate,hrs
	if time_rate%60==0:time_rate=0;secs=0;mins+=1
	if(secs%60==60):mins+=1
	if(mins==60):mins=0;hrs+=1
	text1 = font1.render(f"{hrs}:{mins}", 0, (0))
	screen.blit(text1, (517,17))

def level(g):
	global f
	if g:
		pygame.draw.rect(screen,(196,214,214),[527,350,60,35]) #level
		pygame.draw.rect(screen,(196,214,214),[527,390,60,35]) #level
		pygame.draw.rect(screen,(196,214,214),[527,430,60,35]) #level
		pygame.draw.rect(screen,(196,214,214),[527,470,60,35]) #level

		text1 = font3.render("EASY", 0, (0))
		screen.blit(text1, (529,357))
		text1 = font3.render("MED", 0, (0))
		screen.blit(text1, (529,397))
		text1 = font3.render("HARD", 0, (0))
		screen.blit(text1, (529,437))
		text1 = font3.render("EVIL", 0, (0))
		screen.blit(text1, (529,477))

		f=False
	else :
		pygame.draw.rect(screen, (255,255,255), (505,340,160,260))
		f=True

def level_selected(x1,f1):
	global f,level_value
	if not f1 and x1>350 and x1<385: level_value=1
	if not f1 and x1>390 and x1<425: level_value=2
	if not f1 and x1>430 and x1<465: level_value=3
	if not f1 and x1>470 and x1<505: level_value=4

	pygame.draw.rect(screen, (255,255,255), (505,340,160,260));f=True

run = True 
start_clock =False
flag1 = 0
flag2 = 0
rs = 0 
error = 0
screen.fill((255, 255, 255))
side_buttons()
# The loop thats keep the window running
while run:
	time_rate+=1
	pygame.draw.rect(screen, (255, 255, 255), (505,10,160,60))
	if start_clock: start_time(time_rate)
	# White color background
	# screen.fill((255, 255, 255))
	pygame.draw.rect(screen, (255, 255, 255), (0,0,507,500))

	# Loop through the events stored in event.get()
	for event in pygame.event.get():
		# Quit the game window
		if event.type == pygame.QUIT:
			run = False
		# Get the mouse position to insert number
		if event.type == pygame.MOUSEBUTTONDOWN:
			flag1 = 1
			pos = pygame.mouse.get_pos()
			if(pos[0]<500 and pos[1]<500):
				get_cord(pos)
			elif(pos[0]>520 and pos[0]<595 and pos[1]>200 and pos[1]<240  ):
				rs = 0;error = 0;flag2 = 0
				grid =copy.deepcopy(grid_2nd)
				start_clock=False;raise_err_2=300;mins=0;you_lose=False
				# pygame.draw.rect(screen, (255,255,255), (505,350,160,260))
				pygame.draw.rect(screen, (255,255,255), (0,0,500,600))
			elif(pos[0]>520 and pos[0]<595 and pos[1]>250 and pos[1]<290  ):
				flag2=1 #solve
				start_clock=False;raise_err_2=300;mins=0;raise_err_2=300
			elif(pos[0]>520 and pos[0]<595 and pos[1]>100 and pos[1]<140 ):
				start_clock=True; time_rate=0;mins=0;hrs=0; start_time(0)
				you_lose=False;pygame.draw.rect(screen, (255,255,255), (0,0,500,600))
			elif(pos[0]>520 and pos[0]<595 and pos[1]>150 and pos[1]<190 ):
				rs = 0;error = 0;flag2 = 0
				grid =copy.deepcopy(new_grid(level_value));grid_2nd =copy.deepcopy(grid)
				start_clock=False;raise_err_2=300;mins=0;you_lose=False
				pygame.draw.rect(screen, (255,255,255), (0,0,500,600))
			elif(pos[0]>520 and pos[0]<595 and pos[1]>300 and pos[1]<340 ):
				level(f)
			elif(pos[0]>520 and pos[0]<595 and pos[1]>350 and pos[1]<505 ):
				level_selected(pos[1],f)
				
		# Get the number to be inserted if key pressed
		if event.type == pygame.KEYDOWN and not you_lose:
			if event.key == pygame.K_LEFT:
				x-= 1
				flag1 = 1
			if event.key == pygame.K_RIGHT:
				x+= 1
				flag1 = 1
			if event.key == pygame.K_UP:
				y-= 1
				flag1 = 1
			if event.key == pygame.K_DOWN:
				y+= 1
				flag1 = 1
			if event.key == pygame.K_1:
				val = 1
			if event.key == pygame.K_2:
				val = 2
			if event.key == pygame.K_3:
				val = 3
			if event.key == pygame.K_4:
				val = 4
			if event.key == pygame.K_5:
				val = 5
			if event.key == pygame.K_6:
				val = 6
			if event.key == pygame.K_7:
				val = 7
			if event.key == pygame.K_8:
				val = 8
			if event.key == pygame.K_9:
				val = 9
			if event.key == pygame.K_RETURN:
				flag2 = 1
			# If R pressed clear the sudoku board
			if event.key == pygame.K_r:
				rs = 0
				error = 0
				flag2 = 0
				grid =[
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0]
				]
			# If D is pressed reset the board to default
			if event.key == pygame.K_d:
				rs = 0
				error = 0
				flag2 = 0
				grid =copy.deepcopy(grid_2nd)
				# grid =grid_2nd.copy()
				
	if flag2 == 1:
		if solve(grid, 0, 0)== False:
			error = 1
		else:
			rs = 1
		flag2 = 0
	if val != 0:
		if error==1:error=0;pygame.draw.rect(screen, (255,255,255), (100,0,400,600))
		start_clock=True
		draw_val(val)
		if valid(grid, int(x), int(y), val)== True :
			if grid_2nd[int(x)][int(y)]==0:
				grid[int(x)][int(y)]= val
			if is_full(grid):
				if not you_lose: pygame.draw.rect(screen, (255,255,255), (0,0,500,600))
				print(" son you won");you_lose=True
				text1 = font1.render(" YOU WON ", 1, (255, 0, 0))
				screen.blit(text1, (190, 510))	
			flag1 = 0
		else:
			if grid_2nd[int(x)][int(y)]==0:
				if(grid[int(x)][int(y)])!=val:
					raise_error2()
				grid[int(x)][int(y)]= 0
				# raise_error2()
		val = 0
	
	if error == 1:
		side_buttons()
		raise_error1()
		# print("error 1")
	if rs == 1:
		result()	
		side_buttons()
		rs=0
	draw()
	if flag1 == 1:
		draw_box()	
	instruction()
	clock.tick(60)
	# Update window
	pygame.display.update()

# Quit pygame window
pygame.quit()	
	
