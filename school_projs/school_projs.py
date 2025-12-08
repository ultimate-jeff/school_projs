"""
made by Matthew Robins for 4th hour computer science
----------------------------------
proj = console interactive program / Tetres clone


Note the game loop is at the botom of the file  \/
"""
from threading import Thread
import time
import random
import json

# console color map / texture map   
# Note this i used a google serch for the color codes and the texture charicter (but i knew i wanted the black box char )
prin_RED = '\033[91m'
prin_GREEN = '\033[92m'
prin_BLUE = '\033[94m'
prin_RESET = '\033[0m'
prin_orange = '\033[33m'
prin_black = '\033[30m'
prin_gray = '\033[37m'
colors = [prin_RESET,prin_RED,prin_GREEN,prin_BLUE,prin_orange,prin_black,prin_gray]
orientation_map = ["north","east","south","west"]
textures = ["\u2588"]

with open("data/blocks.json","r") as f:
    shapes = json.load(f)

def tile(color_ind):
    return f"{colors[color_ind]}{textures[0]}{textures[0]}{prin_RESET}"

class Bord:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.fill(5)

    def fill(self,tile_ind):
        self.bord = {}
        for y in range(self.height):
            for x in range(self.width):
                self.bord[(x,y)] = {"texture":tile(tile_ind),"owner":None}
        
    def blit(self):
        for y in range(self.height):
            for x in range(self.width):
                print(self.bord[(x,y)]["texture"],end="")
            print()

class Block:
    def __init__(self,x,y):
        global last_color
        self.x = x
        self.y = y
        self.can_move = True
        self.rotation = "north"
        self.shape = random.choice(shapes["blocks"])
        self.formation = self.shape["formation"]
        if self.shape["color_ind"] == None:
            last_color = max(((last_color + 1) % 4),1)
            self.shape["color_ind"] = last_color
        print(f"created a {self.shape["type"]}")
        self.id = random.randint(0,99999999999)
        # self.formation[self.rotation] is [(x1,y1),(x2,y2),...]  a list of all the tiles that make up the block in the current rotation

    def blit(self,disp):
        for t in self.formation[self.rotation]:
            square = (self.x + t[0],self.y + t[1])
            disp.bord[square]["texture"] = tile(self.shape["color_ind"])
            disp.bord[square]["owner"] = self.id


    def move(self,move_dir,disp):
        x,y = self.x,self.y
        if move_dir == "left":
            x -= 1
        elif move_dir == "rite":
            x += 1
        for t in self.formation[self.rotation]:
            squarex = x + t[0]
            squarey = y + t[1]
            if squarex < 0 or squarex >= disp.width:
                return
        self.x = x
        return
            
    def update(self,disp):
        if self.can_move:
            self.y += 1
        for t in self.formation[self.rotation]:
            square_under = (self.x + t[0],self.y + 1 + t[1])
            if square_under in disp.bord:
                if disp.bord[square_under]["owner"] != self.id and disp.bord[square_under]["texture"] != tile(6):
                    self.can_move = False
            else:
                self.can_move = False

        
display = Bord(10,20)
running = True
loops = 0
all_blocks = []
move = None
last_color = random.randint(1,4)

def blit_all(all_b):
    for b in all_b:
        b.blit(display)

def manage_inputs():
    global move,running
    while running:
        move_choice = input("")
        if move_choice == "a":
            move = "left"
        elif move_choice == "d":
            move = "rite"
        elif move_choice == " ":
            move = "rotate"
        elif move_choice == "q":
            running = False
        else:
            move = None
    time.sleep(0.1)

def apply_moves(block):
    global move,display
    if block.can_move:
        block.move(move,display)
        if move == "rotate":
            curent_rotation = orientation_map.index(block.rotation)
            new_rotation = (curent_rotation + 1) % 4
            block.rotation = orientation_map[new_rotation]
    move = None

def get_curent_block(curent_block):
    global all_blocks
    if not curent_block.can_move:
        B = Block(int(display.width/2),1)
        all_blocks.append(B)
    else:
         B = curent_block
    return B

def check_lose():
    for x in range(display.width):
        pass  # ======================================= i was working on creating rool checks ===============================

in_thread = Thread(target=manage_inputs,daemon=True)
confermation = input("move; a:left / b:rite  rotate: space   press enter to play :")
all_blocks.append(Block(int(display.width/2),1))
curent_block = all_blocks[-1]
in_thread.start()

while running:
    loops += 1
    time.sleep(0.5)
    print(f"{prin_GREEN}frame {loops}{prin_RESET}")
    display.fill(6)
    blit_all(all_blocks)

    curent_block = get_curent_block(curent_block)
    apply_moves(curent_block)
    curent_block.update(display)

    display.blit()

print("game over")


"""
def update(self,disp):
        if self.can_move:
            self.y += 1
        for t in self.formation[self.rotation]:
            square_under = (self.x + t[0],self.y + 1 + t[1])
            if square_under in disp.bord:
                if disp.bord[square_under] != tile(6) and disp.bord[square_under] != tile(self.shape["color_ind"]):
                    self.can_move = False
            else:
                self.can_move = False
        print(self.can_move)
"""