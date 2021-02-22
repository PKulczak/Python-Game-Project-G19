try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector

class Welcome:
    global WIDTH
    global HEIGHT
    def __init__(self, img_name):
        self.image = simplegui._load_local_image(img_name)
        width = self.image.get_width()
        height = self.image.get_height()
        self.pos = Vector(WIDTH/2, HEIGHT/2)
        self.centre = (width/2, height/2)
        self.dim = (width, height)
        self.img_dest_dim = (width, height)

    def draw(self, canvas):
        canvas.draw_image(self.image, self.centre, self.dim, self.pos.get_p(), self.img_dest_dim)

class Keyboard:
    def __init__(self):
        self.start = False
        self.tutorial = False
        self.back = False

    def keyDown(self, key):
        if key == simplegui.KEY_MAP['space']:
            self.start = True
        if key == simplegui.KEY_MAP['q']:
            self.back = True
        if key == simplegui.KEY_MAP['t']:
            self.tutorial = True

##    def keyUp(self, key):
##        if key == simplegui.KEY_MAP['enter']:
##            self.start = False


class Interaction:
    def __init__(self, welcome, tutorial, keyboard):
        self.keyboard = keyboard
        self.welcome = welcome
        self.tutorial = tutorial

##    def update(self):
##        if self.keyboard.start:
##            
##        if self.keyboard.quit:
##            
##        elif self.keyboard.tutorial:



    def draw(self, canvas):
        if not self.keyboard.start:
            if not self.keyboard.tutorial:
                self.welcome.draw(canvas)
            else:
                self.tutorial.draw(canvas)
                if self.keyboard.back:
                    self.keyboard.tutorial = False
                    self.keyboard.back = False



WIDTH = 500
HEIGHT = 500
kbd = Keyboard()
welcome = Welcome("welcome.png")
tutorial = Welcome("tutorial.png")
inter = Interaction(welcome, tutorial, kbd)
frame = simplegui.create_frame('Interactions', WIDTH, HEIGHT)
frame.set_canvas_background('#2C6A6A')
frame.set_draw_handler(inter.draw)
frame.set_keydown_handler(kbd.keyDown)
##frame.set_keyup_handler(kbd.keyUp)
frame.start()





