try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector
from Welcome import Welcome

WIDTH = 500
HEIGHT = 500

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
        width = self.image.get_width()
        frame_width = width//4
        height = self.image.get_height()
        frame_height = height//4
        self.rows = 4
        self.columns = 4
        self.pos = Vector(frame_width/2, frame_height/2)
        self.frame_center = [frame_width/2, frame_height/2]
        self.frame_dim = [frame_width, frame_height]
        self.frame_index = [0,0]
        self.vel = Vector(0,0)
        self.moving = False

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
        if self.keyboard.start:
            self.update()
            self.player.update()
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
inter = Interaction(welcome, tutorial, player, kbd)

frame = simplegui.create_frame('Interactions', WIDTH, HEIGHT)
frame.set_canvas_background('#2C6A6A')
frame.set_draw_handler(inter.draw)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)
frame.start()
