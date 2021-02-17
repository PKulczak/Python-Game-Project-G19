try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# The Vector class
class Vector:

    # Initialiser
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    # Returns a string representation of the vector
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    # Tests the equality of this vector and another
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # Tests the inequality of this vector and another
    def __ne__(self, other):
        return not self.__eq__(other)

    # Returns a tuple with the point corresponding to the vector
    def get_p(self):
        return (self.x, self.y)

    # Returns a copy of the vector
    def copy(self):
        return Vector(self.x, self.y)

    # Adds another vector to this vector
    def add(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __add__(self, other):
        return self.copy().add(other)

    # Negates the vector (makes it point in the opposite direction)
    def negate(self):
        return self.multiply(-1)

    def __neg__(self):
        return self.copy().negate()

    # Subtracts another vector from this vector
    def subtract(self, other):
        return self.add(-other)

    def __sub__(self, other):
        return self.copy().subtract(other)

    # Multiplies the vector by a scalar
    def multiply(self, k):
        self.x *= k
        self.y *= k
        return self

    def __mul__(self, k):
        return self.copy().multiply(k)

    def __rmul__(self, k):
        return self.copy().multiply(k)

    # Divides the vector by a scalar
    def divide(self, k):
        return self.multiply(1/k)

    def __truediv__(self, k):
        return self.copy().divide(k)

    # Normalizes the vector
    def normalize(self):
        return self.divide(self.length())

    # Returns a normalized version of the vector
    def get_normalized(self):
        return self.copy().normalize()

    # Returns the dot product of this vector with another one
    def dot(self, other):
        return self.x * other.x + self.y * other.y

    # Returns the length of the vector
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    # Returns the squared length of the vector
    def length_squared(self):
        return self.x**2 + self.y**2

    # Reflect this vector on a normal
    def reflect(self, normal):
        n = normal.copy()
        n.multiply(2*self.dot(normal))
        self.subtract(n)
        return self

    # Returns the angle between this vector and another one
    def angle(self, other):
        return math.acos(self.dot(other) / (self.length() * other.length()))

    # Rotates the vector 90 degrees anticlockwise
    def rotate_anti(self):
        self.x, self.y = -self.y, self.x
        return self

    # Rotates the vector according to an angle theta given in radians
    def rotate_rad(self, theta):
        rx = self.x * math.cos(theta) - self.y * math.sin(theta)
        ry = self.x * math.sin(theta) + self.y * math.cos(theta)
        self.x, self.y = rx, ry
        return self

    # Rotates the vector according to an angle theta given in degrees
    def rotate(self, theta):
        theta_rad = theta / 180 * math.pi
        return self.rotate_rad(theta_rad)
    
    # project the vector onto a given vector
    def get_proj(self, vec):
        unit = vec.get_normalized()
        return unit.multiply(self.dot(unit))
    
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

    def keyDown(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = True
        if key == simplegui.KEY_MAP['left']:
            self.left = True
        if key == simplegui.KEY_MAP['up']:
            self.up = True
        if key == simplegui.KEY_MAP['down']:
            self.down = True

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
    def __init__(self, player, keyboard):
        self.player = player
        self.keyboard = keyboard

    def update(self):
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


        
kbd = Keyboard()
clock = Clock()
player = Player(clock)
inter = Interaction(player, kbd)

def draw(canvas):
    inter.update()
    player.update()
    player.draw(canvas)


frame = simplegui.create_frame('Interactions', WIDTH, HEIGHT)
frame.set_canvas_background('#2C6A6A')
frame.set_draw_handler(draw)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)
frame.start()
