"""
made by Matthew Robins for 4th hour computer science
----------------------------------
proj = console interactive program / Tetres clone


Note the game loop is at the botom of the file
"""
from threading import Thread
import time
import random
import json
from turtle import color

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
error_queue = []

with open("data/blocks.json","r") as f:
    shapes = json.load(f)

#with open("data/settings/json","r") as f:
#    settings_data = json.load(f)   #  i was working on settings

def tile(color_ind):
    return f"{colors[color_ind]}{textures[0]}{textures[0]}{prin_RESET}"

class Bord:
    def __init__(self,width,height,color_ind=6):
        self.background_color = color_ind
        self.width = width
        self.height = height
        self.bord = {}
        self.fill(5)

    def _set_tile(self,pos,color_ind):
        x,y = self._snap_cords_in_bounds(pos[0],pos[1])
        self.bord[(x,y)]["texture"] = tile(color_ind)
    def _get_tile(self,pos):
        x,y = self._snap_cords_in_bounds(pos[0],pos[1])
        return self.bord[(x,y)]["texture"]
    def _get_tile_owner(self,pos):
        x,y = self._snap_cords_in_bounds(pos[0],pos[1])
        return self.bord[(x,y)]["owner"]
    def _set_tile_owner(self,pos,owner):
        x,y = self._snap_cords_in_bounds(pos[0],pos[1])
        self.bord[(x,y)]["owner"] = owner

    def fill(self,tile_ind):
        for y in range(self.height):
            for x in range(self.width):
                self.bord[(x,y)] = {"texture":tile(tile_ind),"owner":None}
        
    def flip(self):
        for y in range(self.height):
            for x in range(self.width):
                print(self._get_tile((x,y)),end="")
            print()

    def fill_row(self,row,color_ind):
        for x in range(self.width):
            self._set_tile((x,row),color_ind)

    def _move_pixle_in_bounds(self,pos,new_pos):
        color = self._get_tile(pos)
        self._set_tile(pos,self.background_color)
        self.bord[new_pos]["texture"] = color

    def _snap_cords_in_bounds(self,x,y):
        new_x = min(max(x,0),self.width-1)
        new_y = min(max(y,0),self.height-1)
        return new_x,new_y

    def move_pixle(self,x,y,new_x,new_y):
        x,y = self._snap_cords_in_bounds(x,y)
        new_x,new_y = self._snap_cords_in_bounds(new_x,new_y)
        self._move_pixle_in_bounds((x,y),(new_x,new_y))
                
    def place_pixle(self,x,y,color_ind):
        x,y = self._snap_cords_in_bounds(x,y)
        self._set_tile((x,y),color_ind)

    def check_if_can_move(self,list_of_positions,dx,dy,X=0,Y=0):
        # pacial flail
        can_move = True
        for p in list_of_positions:
            x,y = p[0]+X,p[1]+Y
            target_x,target_y = (x+dx),(y+dy)
            target = self._get_tile((target_x,target_y))
            target_owner = self._get_tile_owner((target_x,target_y))
            if target_owner != None and target != tile(self.background_color) and (target_x,target_y) in self.bord:
                can_move = False
        return can_move

    def place_shape(self,list_of_positions,X,Y,color_ind,owner=None):
        for p in list_of_positions:
            x,y = p[0]+X,p[1]+Y
            self.place_pixle(x,y,color_ind)
            self._set_tile_owner((x,y),owner)

    def remove_shape(self,list_of_positions,X,Y,color_ind):
        for p in list_of_positions:
            x,y = p[0]+X,p[1]+Y
            if self._get_tile((x,y)) == tile(color_ind):
                self._set_tile((x,y),self.background_color)
                self._set_tile_owner((x,y),owner=None)
        
class Block:
    def __init__(self,x,y):
        global last_color
        self.can_move = True
        self.x = x
        self.y = y
        self.next_x = self.x
        self.next_y = self.y
        self.rotation = "north"
        self.shape = random.choice(shapes["blocks"])
        self.formation = self.shape["formation"]  # self.formation[self.rotation] is [(x1,y1),(x2,y2),...]
        if self.shape["color_ind"] == None:
            last_color = max(((last_color + 1) % 4),1)
        self.color_ind = last_color
        self.id = f"{random.randint(0,99999)}_{len(all_blocks)}"
        display.place_shape(self.formation[self.rotation],x,y,self.color_ind,owner=self.id)

    def update(self):
        if self.y > display.height:
            self.can_move = False
        display.remove_shape(self.formation[self.rotation],self.x,self.y,self.color_ind)
        self.can_move = display.check_if_can_move(self.formation[self.rotation],0,gravaty,self.x,self.y)  
        if self.can_move:
            self.y += gravaty  # i was working on fixing colisions (i was having probs with snaping and colision detection)
            self.apply_moves()
        display.place_shape(self.formation[self.rotation],self.x,self.y,self.color_ind,owner=self.id)

    def move(self,move_dir,disp):
        if move_dir == "left":
            self.x -= 1
        elif move_dir == "rite":
            self.x += 1
        for t in self.formation[self.rotation]:
            squarex = self.x + t[0]
            squarey = self.y + t[1]
            if squarex < 0 or squarex >= disp.width:
                return

    def apply_moves(self):
        global move,display
        if self.can_move:
            self.move(move,display)
            if move == "rotate":
                curent_rotation = orientation_map.index(self.rotation)
                new_rotation = (curent_rotation + 1) % 4
                self.rotation = orientation_map[new_rotation]
        move = None
             
class Rules:
    def __init__(self):
        self.points = 0
        self.leval = 0
        self.alive = True
        self.activate_dellay = 0

    def update(self,disp):
        pass
                

display = Bord(width=10,height=20,color_ind=6)
rules = Rules()
running = True
loops = 0
frame_dellay = 0.3
gravaty = 1
all_blocks = []
move = None
last_color = random.randint(1,4)

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

def get_curent_block(curent_block):
    global all_blocks
    if not curent_block.can_move:
        B = Block(int(display.width/2),0)
        all_blocks.append(B)
    else:
         B = curent_block
    return B

def update_all(all_b):
    for b in all_b:
        b.update()

in_thread = Thread(target=manage_inputs,daemon=True)
confermation = input("move; a:left / b:rite  rotate: space   press enter to play :")
all_blocks.append(Block(int(display.width/2),0))
curent_block = all_blocks[-1]
in_thread.start()
display.fill(display.background_color)
while running:
    loops = (loops + 1) % 1000
    display.fill(display.background_color)
    time.sleep(frame_dellay)


    #update_all(all_blocks)
    print(f"{prin_GREEN}frame {loops}{prin_RESET} -------------------------------")
    curent_block = get_curent_block(curent_block)
    curent_block.apply_moves()
    curent_block.update()

    
    display.flip()
print("game over")

"""

def update(self):
        self.can_move = display.check_if_can_move(self.formation[self.rotation],0,gravaty,self.x,self.y)
        if self.y > display.height:
            self.can_move = False
        if self.can_move:
            display.remove_shape(self.formation[self.rotation],self.x,self.y,self.color_ind)
            self.y += gravaty
            self.apply_moves()
            display.place_shape(self.formation[self.rotation],self.x,self.y,self.color_ind,owner=self.id)


"""