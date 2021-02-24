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


WIDTH = 500
HEIGHT = 500





