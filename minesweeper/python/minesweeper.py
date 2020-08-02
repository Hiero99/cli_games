from random import shuffle

x_max = 10; y_max = 10; bombs = 10;
game_data_raw = [[{'bomb':0, 'click':0} for x in range(x_max)] for y in range(y_max)]
gamestate = 'r'

def init():
  global game_data_raw
  game_data_raw = [[{'bomb':0, 'click':0} for x in range(x_max)] for y in range(y_max)]
  gen_game()
  
def gen_game():
  global game_data_raw;
  new_gd = [-1 if x<bombs else 0 for x in range(x_max*y_max)]
  shuffle(new_gd)
  game_data_raw = [[{'bomb':new_gd[x+y*x_max], 'click':0} for x in range(x_max)] for y in range(y_max)]
  for y in range(y_max):
    for x in range(x_max):
      game_data_raw[y][x]['bomb'] = -1 if game_data_raw[y][x]['bomb']==-1 else count_surrunding_bombs(x,y)

def count_surrunding_bombs(x,y):
  nbombs = 0;
  if x>0:
    if game_data_raw[y][x-1]['bomb']==-1:nbombs+=1
    if y>0 and game_data_raw[y-1][x-1]['bomb']==-1:nbombs+=1
    if y+1<y_max and y+1<y_max and game_data_raw[y+1][x-1]['bomb']==-1:nbombs+=1
  if y>0 and game_data_raw[y-1][x]['bomb']==-1:nbombs+=1
  if y+1<y_max and game_data_raw[y+1][x]['bomb']==-1:nbombs+=1
  if x+1<x_max:
    if game_data_raw[y][x+1]['bomb']==-1:nbombs+=1
    if y>0 and game_data_raw[y-1][x+1]['bomb']==-1:nbombs+=1
    if y+1<y_max and game_data_raw[y+1][x+1]['bomb']==-1:nbombs+=1
  return nbombs

def askx():
  x = input("Where do you want to click? \nx: ")
  return int(x)

def asky():
  y = input("y: ")
  return int(y)

def click(x,y):
  global game_data_raw;
  game_data_raw[y][x]['click']+=1;
  if game_data_raw[y][x]['bomb']==0 and game_data_raw[y][x]['click']<2:
    if x>0:
      click(x-1,y)
      if y>0:click(x-1,y-1)
      if y+1<y_max:click(x-1,y+1)
    if y>0:click(x,y-1)
    if y+1<y_max:click(x,y+1)
    if x+1<x_max:
      click(x+1,y)
      if y>0:click(x+1,y-1)
      if y+1<y_max:click(x+1,y+1)

def tick(x,y):
  click(x,y)
  mprint()

def show_all():
  for x in range(x_max):
    for y in range(y_max):
      click(x,y)
  mprint()
  
def check_gamestate():
  global gamestate
  counter_clicked_bombs = 0
  counter_clicked_tiles = 0
  for x in range(x_max):
    for y in range(y_max):
      if game_data_raw[y][x]['click']>0:
        counter_clicked_tiles+=1
        if game_data_raw[y][x]['bomb']==-1:
          counter_clicked_bombs+=1
  if counter_clicked_bombs > 0: gamestate = input('You lost because a bomb went of.\nDo you wanna play again ? (y/n)')
  if counter_clicked_tiles == x_max*y_max-bombs: gamestate = input('You won !!!\nDo you wanna play again ? (y/n)')

def mprint():
  for x in range(y_max):
    print(mprint_helper(x));
  print()

def mprint_helper(i):
  return ('{:2}'*x_max).format(*pre_format(i))

def pre_format(i):
  return [' _' if game_data_raw[i][x]['click']<1 else (' X' if game_data_raw[i][x]['bomb']==-1 else game_data_raw[i][x]['bomb']) for x in range(x_max)]


# game loop
init()
mprint()
while gamestate == 'y' or gamestate == 'r':
  click(askx(),asky())
  mprint()
  check_gamestate()
  if gamestate == 'y':
    gamestate == 'r'
    init()
    mprint()
