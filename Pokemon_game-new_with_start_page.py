try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random
from vector import Vector
from Welcome import Welcome

WIDTH = 800
HEIGHT = 480

walls_list = []
npc_list = []
npc_lost = []

class Clock:
    def __init__(self):
        self.time = 0
        
    def tick(self):
        self.time += 1
    
    def transition(self,frame_duration):
        if self.time >= frame_duration:
            self.time = 0
            return True
        else:
            return False
                
class Player:
    def __init__(self, clock): 
        self.clock = clock
        self.image = simplegui._load_local_image("player.png")

        self.rows = 4
        self.columns = 4
        
        width = self.image.get_width()
        frame_width = width//self.columns
        height = self.image.get_height()
        frame_height = height//self.rows

        self.pos = Vector(552, 224)
        self.frame_center = [frame_width/2, frame_height/2]
        self.frame_dim = [frame_width, frame_height]
        self.frame_index = [0,0]
        
        self.vel = Vector(0,0)
        self.moving = False
        self.in_fight = False
        self.interacting = False
        self.lock = False
        self.scale_factor = 0.26
        
        self.lives = 6
        self.heart_img = simplegui._load_local_image("heart.png")

        self.player_left = self.pos.x - self.frame_center[0]
        self.player_right = self.pos.x + self.frame_center[0]
        self.player_top = self.pos.y
        self.player_bot = self.pos.y + self.frame_center[1]


    def draw(self, canvas):
        if self.moving == True:
            canvas.draw_image(self.image, 
                    [self.frame_center[0] + self.frame_index[0] * self.frame_dim[0], 
                     self.frame_center[1] + self.frame_index[1] * self.frame_dim[1]], 
                     self.frame_dim, [self.pos.x,self.pos.y], [self.frame_dim[0]*self.scale_factor,self.frame_dim[1]*self.scale_factor])
        else:
            canvas.draw_image(self.image, 
                    [self.frame_center[0] + 0 * self.frame_dim[0], 
                     self.frame_center[1] + self.frame_index[1] * self.frame_dim[1]], 
                     self.frame_dim, [self.pos.x,self.pos.y], [self.frame_dim[0]*self.scale_factor,self.frame_dim[1]*self.scale_factor])

        canvas.draw_image(self.heart_img, [8,8], [16,16], [16,16], [16,16])
        lives = "x"+str(self.lives)
        canvas.draw_text(lives, [32,20], 24, "Black")
        
        self.clock.tick()
        move_on = self.clock.transition(6)
        if move_on == True:
            self.next_frame()
        
    def next_frame(self):
        self.frame_index[0] += 1
        if self.frame_index[0] >= self.columns:
            self.frame_index[0] = 0

    def update(self):
        self.pos.add(self.vel)

class NPC:
    def __init__(self, img_name, pos, clock):
        npc_list.append(self)
        self.clock = clock
        self.image_name = img_name
        self.image = simplegui._load_local_image(self.image_name+".png")
        
        self.rows = 1
        self.columns = 4
        
        width = self.image.get_width()
        frame_width = width//self.columns
        height = self.image.get_height()
        frame_height = height//self.rows

        self.pos = pos
        self.frame_center = [frame_width/2, frame_height/2]
        self.frame_dim = [frame_width, frame_height]
        self.frame_index = [0,0]
        
        self.vel = Vector(0,0)
        self.moving = False
        self.scale_factor = 0.26

        self.wall_left = self.pos.x - (self.frame_dim[0]//2*self.scale_factor)
        self.wall_right = self.pos.x + (self.frame_dim[0]//2*self.scale_factor)
        self.wall_top = self.pos.y - (self.frame_dim[1]//2*self.scale_factor)
        self.wall_bot = self.pos.y + (self.frame_dim[1]//2*self.scale_factor)

    def draw(self, canvas):
        if self.moving == True:
            canvas.draw_image(self.image, 
                    [self.frame_center[0] + self.frame_index[0] * self.frame_dim[0], 
                     self.frame_center[1] + self.frame_index[1] * self.frame_dim[1]], 
                     self.frame_dim, [self.pos.x,self.pos.y], [self.frame_dim[0]*self.scale_factor,self.frame_dim[1]*self.scale_factor])
        else:
            canvas.draw_image(self.image, 
                    [self.frame_center[0] + 0 * self.frame_dim[0], 
                     self.frame_center[1] + self.frame_index[1] * self.frame_dim[1]], 
                     self.frame_dim, [self.pos.x,self.pos.y], [self.frame_dim[0]*self.scale_factor,self.frame_dim[1]*self.scale_factor])
        
        if self.moving:
            self.update()
        self.clock.tick()
        move_on = self.clock.transition(6)
        if move_on == True:
            self.next_frame()

    def next_frame(self):
        self.frame_index[0] += 1
        if self.frame_index[0] >= self.columns:
            self.frame_index[0] = 0

    def update(self):
        self.pos.add(self.vel)

    def collision(self, player):
        player.player_left = player.pos.x - ((player.frame_dim[0]//2)*player.scale_factor)
        player.player_right = player.pos.x + ((player.frame_dim[0]//2)*player.scale_factor)
        player.player_top = player.pos.y - ((player.frame_dim[1]//2)*player.scale_factor)
        player.player_bot = player.pos.y + ((player.frame_dim[1]//2)*player.scale_factor)

        self.wall_left = self.pos.x - (self.frame_dim[0]//2*self.scale_factor)
        self.wall_right = self.pos.x + (self.frame_dim[0]//2*self.scale_factor)
        self.wall_top = self.pos.y - (self.frame_dim[1]//2*self.scale_factor)
        self.wall_bot = self.pos.y + (self.frame_dim[1]//2*self.scale_factor)
        
        col_left = ((self.wall_left - player.player_right) >= 0)
        col_right = ((player.player_left - self.wall_right) >= 0)
        col_top = ((self.wall_top - player.player_bot) >= 0)
        col_bot = ((player.player_top - self.wall_bot) >= 0)

        collision = True
        if (col_right) :
            collision = False
        if (col_left):
            collision = False
        if (col_bot):
            collision = False
        if (col_top):
            collision = False

        return collision

    def interact(self, player):
        global npc_lost
        self.vel = Vector(0,0)
        print("fight")
        npc_lost.append(self.image_name)
        self.moving = False

    def move_to_player(self,player):
        player.player_left = player.pos.x - ((player.frame_dim[0]//2)*player.scale_factor)
        player.player_right = player.pos.x + ((player.frame_dim[0]//2)*player.scale_factor)

        col_left = ((self.wall_left - player.player_right) >= 0)
        col_right = ((player.player_left - self.wall_right) >= 0)
        
        distance = player.pos.y - self.pos.y
        if distance < 96:
            if player.pos.y > self.pos.y:
                if (col_left == False) and (col_right == False):
                    player.vel = Vector(0,0)
                    player.moving = False
                    player.lock = True
                    self.moving = True
                    self.vel = Vector(0,2)

class NPCWall(NPC):
    def __init__(self, img_name, pos, clock):
        super().__init__(img_name, pos, clock)

    def interact(self, player):
        if player.vel.x > 0:
            player.pos.x = self.wall_left-((player.frame_dim[0]//2)*player.scale_factor)-1
        if player.vel.x < 0:
            player.pos.x = self.wall_right+((player.frame_dim[0]//2)*player.scale_factor)+1
        if player.vel.y > 0:
            player.pos.y = self.wall_top-((player.frame_dim[1]//2)*player.scale_factor)-1
        if player.vel.y < 0:
            player.pos.y = self.wall_bot+((player.frame_dim[1]//2)*player.scale_factor)+1

    def move_to_player(self,player):
        pass
    
class Yacht(NPC):
    def __init__(self, img_name, pos, clock):
        super().__init__(img_name, pos, clock)
        self.vel = Vector(0, -0.01)
        self.moving = True

        width = self.image.get_width()
        height = self.image.get_height()
        self.frame_center = [width/2, height/2]
        self.frame_dim = [width, height]
        
    def draw(self, canvas):
        if self.pos.y > -100:
            canvas.draw_image(self.image, 
                    [self.frame_center[0] + 0 * self.frame_dim[0], 
                    self.frame_center[1] + self.frame_index[1] * self.frame_dim[1]], 
                    self.frame_dim, [self.pos.x,self.pos.y], [self.frame_dim[0]*self.scale_factor,self.frame_dim[1]*self.scale_factor])
        if self.moving:
            self.update()
        
        self.clock.tick()
        move_on = self.clock.transition(20)
        if move_on == True:
            self.vel.add(self.vel)
            self.clock.time = 0
            
    def update(self):
        self.pos.add(self.vel)

    def move_to_player(self,player):
        pass
        
        
class Keyboard:
    def __init__(self):
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.start = False
        self.tutorial = False
        self.back = False

    def keyDown(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = True
        if key == simplegui.KEY_MAP['left']:
            self.left = True
        if key == simplegui.KEY_MAP['up']:
            self.up = True
        if key == simplegui.KEY_MAP['down']:
            self.down = True
        if key == simplegui.KEY_MAP['space']:
            self.start = True
        if key == simplegui.KEY_MAP['q']:
            self.back = True
        if key == simplegui.KEY_MAP['t']:
            self.tutorial = True


    def keyUp(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = False
        if key == simplegui.KEY_MAP['left']:
            self.left = False
        if key == simplegui.KEY_MAP['up']:
            self.up = False
        if key == simplegui.KEY_MAP['down']:
            self.down = False

class Wall:
    def __init__(self, name, pos):
        walls_list.append(self)
        self.image = simplegui._load_local_image(name)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.pos = pos
        self.frame_dim = [self.width, self.height]

        self.wall_left = self.pos.x - (self.frame_dim[0]//2)
        self.wall_right = self.pos.x + (self.frame_dim[0]//2)
        self.wall_top = self.pos.y - (self.frame_dim[1]//2)
        self.wall_bot = self.pos.y + (self.frame_dim[1]//2)


    def draw(self, canvas):
        canvas.draw_image(self.image, 
                    [self.width//2, self.height//2], 
                     [self.width, self.height], [self.pos.x,self.pos.y], [self.frame_dim[0],self.frame_dim[1]])
        
    def collision(self, player):
        player.player_left = player.pos.x - ((player.frame_dim[0]//2)*player.scale_factor)
        player.player_right = player.pos.x + ((player.frame_dim[0]//2)*player.scale_factor)
        player.player_top = player.pos.y
        player.player_bot = player.pos.y + ((player.frame_dim[1]//2)*player.scale_factor)

        col_left = ((self.wall_left - player.player_right) >= 0)
        col_right = ((player.player_left - self.wall_right) >= 0)
        col_top = ((self.wall_top - player.player_bot) >= 0)
        col_bot = ((player.player_top - self.wall_bot) >= 0)

        collision = True
        if (col_right) :
            collision = False
        if (col_left):
            collision = False
        if (col_bot):
            collision = False
        if (col_top):
            collision = False

        return collision

    def interact(self, player):
        if player.vel.x > 0:
            player.pos.x = self.wall_left-((player.frame_dim[0]//2)*player.scale_factor)-1
        if player.vel.x < 0:
            player.pos.x = self.wall_right+((player.frame_dim[0]//2)*player.scale_factor)+1
        if player.vel.y > 0:
            player.pos.y = self.wall_top-((player.frame_dim[1]//2)*player.scale_factor)-1
        if player.vel.y < 0:
            player.pos.y = self.wall_bot+1
        

class Interact(Wall):
    def __init__(self, name, pos, int_type, location = None):
        super().__init__(name, pos)
        self.location = location
        self.int_type = int_type
        
    def interact(self, player):
        if self.int_type == "fight":
            if player.moving:
                player.in_fight = True
        if self.int_type == "interact":
            player.interacting = True
            
class Background:
    def __init__(self, Map, width, height):
        self.Map = simplegui._load_local_image(Map+".png")
        self.map_name = Map
        self.width = width
        self.height = height
        
        self.orig_width = self.Map.get_width()
        self.orig_height = self.Map.get_height()

    def draw(self, canvas):
        canvas.draw_image(self.Map, (self.orig_width/2,self.orig_height/2), (self.orig_width,self.orig_height), (self.width/2, self.height/2), (self.width,self.height))

    def load_wall(self):
        global walls_list, npc_list, npc_lost
        walls_list = []
        npc_list = []
        with open(self.map_name+".txt","r") as file:
            level = file.readlines()
            x = y = 0
            for row in level:
                for col in row:
                    if col == "t":
                        wall = Wall("tree.png", Vector(8+(32*x), 0+(32*y)))
                    if col == "w":
                        wall = Wall("up.png", Vector(8+(32*x), 8+(32*y)))
                    if col == "s":
                        wall = Wall("up.png", Vector(8+(32*x), -8+(32*y)))
                    if col == "a":
                        wall = Wall("left.png", Vector(16+(32*x), 0+(32*y)))
                    if col == "d":
                        wall = Wall("left.png", Vector(0+(32*x), 0+(32*y)))
                    if col == "1":
                        wall = Interact("tree.png", Vector(8+(32*x), 0+(32*y)), "interact", 0)
                    if col == "2":
                        wall = Interact("tree.png", Vector(8+(32*x), 0+(32*y)), "interact", 1)
                    if col == "3":
                        wall = Interact("tree.png", Vector(8+(32*x), 0+(32*y)), "interact", 2)
                    if col == "4":
                        wall = Interact("tree.png", Vector(8+(32*x), 0+(32*y)), "interact", 3)
                    if col == "f":
                        wall = Interact("tree.png", Vector(8+(32*x), 0+(32*y)), "fight")
                    if col == "y":
                        clock = Clock()
                        yacht = Yacht("yacht", Vector(8+(32*x), 0+(32*y)), clock)
                    if col == "b":
                        clock = Clock()
                        npc_name = self.load_npc()
                        if npc_name in npc_lost:
                            npc = NPCWall(npc_name, Vector(8+(32*x), 0+(32*y)), clock)
                        else:
                            npc = NPC(npc_name, Vector(8+(32*x), 0+(32*y)), clock)
                    x += 1
                y += 1
                x = 0
            
    def new_level(self, location, player):
        map_str = {"map2y": [["route1", Vector(111,43)]],
                   "map": [["route1", Vector(770,338)], ["route2", Vector(58,236)], ["pokecenter", Vector(406,424)]],
                   "map2": [["route1", Vector(111,43)]],
                   "map3": [["route3", Vector(745,47)]],
                   "route1": [["map2", Vector(756, 169)], ["map", Vector(58,169)]],
                   "route2": [["map", Vector(768,225)], ["route3a", Vector(56,120)], ["route3b", Vector(47,447)]],
                   "route3": [["route2a", Vector(680,143)], ["route2b", Vector(514,443)], ["map3", Vector(220, 424)], ["route4", Vector(52,319)]],
                   "route4": [["route3", Vector(774,351)], ["bossfight1",Vector(406,424)]],
                   "map3": [["route3",Vector(746,67)], ["gym2",Vector(406,424)], ["pokecenter2",Vector(406,424)]],
                   "gym2": [["map3",Vector(650,143)]],
                   "pokecenter": [["map",Vector(290,261)]],
                   "pokecenter2": [["map3",Vector(172,382)]],
                   "bossfight1": [["route4",Vector(626,200)], ["bossfight2",Vector(406,424)]],
                   "bossfight2": [["bossfight1",Vector(406,70)], ["bossfight3",Vector(406,424)]],
                   "bossfight3": [["bossfight2",Vector(406,70)]]}
        
        player.pos = map_str[self.map_name][location][1]
        player.vel = Vector(0,0)
        self.map_name = map_str[self.map_name][location][0]

        if (self.map_name == "route3a") or (self.map_name == "route3b"):
            self.map_name = "route3"
        if (self.map_name == "route2a") or (self.map_name == "route2b"):
            self.map_name = "route2"

        player.interacting = False
        self.Map = simplegui._load_local_image(self.map_name+".png")
        self.load_wall()

    def load_npc(self):
        npc_str =  {"gym2": "boss1",
                    "bossfight3": "boss2",
                    "bossfight1": "boss3",
                    "bossfight2": "boss4"}
        npc_name = npc_str[self.map_name]
        return npc_name
                
class Interaction:
    def __init__(self, welcome, tutorial, player, keyboard, background):
        self.player = player
        self.keyboard = keyboard
        self.welcome = welcome
        self.tutorial = tutorial
        self.background = background

    def update(self):
        if self.keyboard.start:
            if self.player.lock == False:
                if self.keyboard.right:
                    self.player.vel = Vector(2, 0)
                    self.player.frame_index[1] = 2
                    self.player.moving = True
                elif self.keyboard.left:
                    self.player.vel = Vector(-2,0)
                    self.player.frame_index[1] = 1
                    self.player.moving = True
                elif self.keyboard.up:
                    self.player.vel = Vector(0,-2)
                    self.player.frame_index[1] = 3
                    self.player.moving = True
                elif self.keyboard.down:
                    self.player.vel = Vector(0,2)
                    self.player.frame_index[1] = 0
                    self.player.moving = True
                else:
                    self.player.moving = False
                    self.player.vel = Vector(0,0)

    def draw(self, canvas):
        global walls_list, npc_list
        
        if self.keyboard.start:
            self.update()
            self.player.update()
            self.background.draw(canvas)
            
            for x in walls_list:
                x.draw(canvas)
                col = x.collision(self.player)
                if col == True:
                    x.interact(self.player)
                    if player.interacting == True:
                        self.background.new_level(x.location, self.player)
                    if player.in_fight == True:
                        rand_int = random.random()
                        if rand_int < 0.007:
                            print("fight")
                        player.in_fight = False

            if self.player.lives == 0:
                self.player.lives = 6
                self.keyboard.start = False
                self.background = Background("map2", WIDTH, HEIGHT)
                self.background.load_wall()
                self.player.pos = Vector(552, 224)

            #self.background.draw(canvas)
            for y in npc_list:
                y.draw(canvas)
                y.move_to_player(self.player)
                col = y.collision(self.player)
                if col == True:
                    y.interact(self.player)
                    self.background = Background(self.background.map_name, WIDTH, HEIGHT)
                    self.background.load_wall()
                    self.player.lock = False
            self.player.draw(canvas)
            
        else:
            if not self.keyboard.tutorial:
                self.welcome.draw(canvas)    
            else:
                self.tutorial.draw(canvas)
                if self.keyboard.back:
                    self.keyboard.tutorial = False
                    self.keyboard.back = False
              
kbd = Keyboard()
clock = Clock()
player = Player(clock)
welcome = Welcome("welcome.png")
tutorial = Welcome("tutorial.png")
background = Background("map2y", WIDTH, HEIGHT)
background.load_wall()
inter = Interaction(welcome, tutorial, player, kbd, background)


frame = simplegui.create_frame('Pokemon', WIDTH, HEIGHT)
frame.set_canvas_background('#2C6A6A')
frame.set_draw_handler(inter.draw)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)
frame.start()
