try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector
from Welcome import Welcome

WIDTH = 500
HEIGHT = 500

walls_list = []

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
        
        self.pos = Vector(frame_width/2, frame_height/2)
        self.frame_center = [frame_width/2, frame_height/2]
        self.frame_dim = [frame_width, frame_height]
        self.frame_index = [0,0]
        
        self.vel = Vector(0,0)
        self.moving = False

        self.player_left = self.pos.x - self.frame_center[0]
        self.player_right = self.pos.x + self.frame_center[0]
        self.player_top = self.pos.y - self.frame_center[1]
        self.player_bot = self.pos.y + self.frame_center[1]


    def draw(self, canvas):
        if self.moving == True:
            canvas.draw_image(self.image, 
                    [self.frame_center[0] + self.frame_index[0] * self.frame_dim[0], 
                     self.frame_center[1] + self.frame_index[1] * self.frame_dim[1]], 
                     self.frame_dim, [self.pos.x,self.pos.y], [self.frame_dim[0]//2,self.frame_dim[1]//2])
        else:
            canvas.draw_image(self.image, 
                    [self.frame_center[0] + 0 * self.frame_dim[0], 
                     self.frame_center[1] + self.frame_index[1] * self.frame_dim[1]], 
                     self.frame_dim, [self.pos.x,self.pos.y], [self.frame_dim[0]//2,self.frame_dim[1]//2])
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

class Interaction:
    def __init__(self, welcome, tutorial, player, keyboard):
        self.player = player
        self.keyboard = keyboard
        self.welcome = welcome
        self.tutorial = tutorial

    def update(self):
        if self.keyboard.start:
            if self.keyboard.right:
                self.player.vel = Vector(3, 0)
                self.player.frame_index[1] = 2
                self.player.moving = True
            elif self.keyboard.left:
                self.player.vel = Vector(-3,0)
                self.player.frame_index[1] = 1
                self.player.moving = True
            elif self.keyboard.up:
                self.player.vel = Vector(0,-3)
                self.player.frame_index[1] = 3
                self.player.moving = True
            elif self.keyboard.down:
                self.player.vel = Vector(0,3)
                self.player.frame_index[1] = 0
                self.player.moving = True
            else:
                self.player.moving = False
                self.player.vel = Vector(0,0)

    def draw(self, canvas):
        global walls_list
        if self.keyboard.start:
            self.update()
            self.player.update()
            self.player.draw(canvas)
            for x in walls_list:
                x.draw(canvas)
                col = x.collision(self.player)
                if col == True:
                    x.interact(self.player)
        else:
            if not self.keyboard.tutorial:
                self.welcome.draw(canvas)
            else:
                self.tutorial.draw(canvas)
                if self.keyboard.back:
                    self.keyboard.tutorial = False
                    self.keyboard.back = False
            

class Wall:
    def __init__(self, name, pos):
        walls_list.append(self)
        self.image = simplegui._load_local_image(name)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.pos = pos
        self.frame_dim = [self.width*2, self.height*2]

        self.wall_left = self.pos.x - (self.frame_dim[0]//2)
        self.wall_right = self.pos.x + (self.frame_dim[0]//2)
        self.wall_top = self.pos.y - (self.frame_dim[1]//2)
        self.wall_bot = self.pos.y + (self.frame_dim[1]//2)


    def draw(self, canvas):
        canvas.draw_image(self.image, 
                    [self.width//2, self.height//2], 
                     [self.width, self.height], [self.pos.x,self.pos.y], [self.frame_dim[0],self.frame_dim[1]])
        
    def collision(self, player):
        player.player_left = player.pos.x - (player.frame_dim[0]//4)
        player.player_right = player.pos.x + (player.frame_dim[0]//4)
        player.player_top = player.pos.y - (player.frame_dim[1]//4)
        player.player_bot = player.pos.y + (player.frame_dim[1]//4)

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
            player.pos.x = self.wall_left-(player.frame_dim[0]//4)
        if player.vel.x < 0:
            player.pos.x = self.wall_right+(player.frame_dim[0]//4)
        if player.vel.y > 0:
            player.pos.y = self.wall_top-(player.frame_dim[1]//4)
        if player.vel.y < 0:
            player.pos.y = self.wall_bot+(player.frame_dim[1]//4)
            

        
kbd = Keyboard()
clock = Clock()
player = Player(clock)
welcome = Welcome("welcome.png")
tutorial = Welcome("tutorial.png")
wall = Wall("tree.png", Vector(WIDTH//2, HEIGHT//2))
wall = Wall("tree.png", Vector(WIDTH//2-60, HEIGHT//2))
inter = Interaction(welcome, tutorial, player, kbd)


frame = simplegui.create_frame('Interactions', WIDTH, HEIGHT)
frame.set_canvas_background('#2C6A6A')
frame.set_draw_handler(inter.draw)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)
frame.start()
