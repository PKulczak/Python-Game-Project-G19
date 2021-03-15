try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import time
import random
class Player:
    def __init__(self, name, pokemon_list, Level):
        self.name = name
        self.pokemon_list = pokemon_list

        

class Fight:
    def __init__(self, monster, pokemon, keyboard):
        self.monster = monster
        self.pokemon = pokemon
        self.count = 70
        self.attack = True
        self.fullhp = pokemon.HP
        self.kbd = keyboard
        self.info = self.monster.name+" VS "+ self.pokemon.name
        self.image = simplegui._load_local_image("fight_background.png")
        self.col1 = "White"
        self.col2 = "Grey"
        self.col3 = "Grey"
        self.col4 = "Grey"
        self.inte = 1
        self.run = False
        self.bag = simplegui._load_local_image("bag.png")
        self.first = True

    def draw(self, canvas):
        if self.inte == 4 and self.kbd.select:
            if not self.kbd.quit:
                canvas.draw_image(self.bag, (375,250), (750,500), (250,250), (500,333))
            else:
                self.kbd.select = False
        else:
            canvas.draw_image(self.image, (375,250), (750,500), (250,250), (500,333))
            canvas.draw_text(self.monster.name, (90, 140), 20, 'Black')
            canvas.draw_text("HP:"+str(self.monster.HP), (120, 165), 20, 'Black')
            canvas.draw_text(self.pokemon.name, (340, 260), 20, 'Black')
            canvas.draw_text("HP:"+str(self.pokemon.HP)+"/"+str(self.fullhp), (360, 290), 20, 'Black')
            self.pokemon.draw(canvas)
            self.monster.draw(canvas)
            if self.run:
                canvas.draw_text(self.info, (80, 370), 20, 'White')
            elif self.count != 0:
                if not self.first:
                    if self.attack:
                        self.monster.draw_effect(canvas)
                    else:
                        self.pokemon.draw_effect(canvas)
                canvas.draw_text(self.info, (80, 370), 20, 'White')
                self.count = self.count - 1
            else:
                self.first = False
                if self.attack:
                    if not self.kbd.select:
                        self.inte = self.interact(self.inte, canvas)
                    else:
                        if self.inte <=2 :
                            self.fight(self.pokemon, self.monster, self.inte, canvas)
                            self.kbd.select = False
                            self.count = 130
                else:
                    self.fight(self.pokemon, self.monster, self.inte, canvas)
                    self.count = 110
    def fight(self, pokemon, monster, inte, canvas):
        if pokemon.HP > 0 and monster.HP > 0:
            if not self.attack:
                pokemon.HP = pokemon.HP-(monster.ATK - pokemon.DEF)
                self.info = monster.name+" attack "+pokemon.name
                self.attack = True
            else:
                if inte == 1:
                    monster.HP = monster.HP-(pokemon.ATK - monster.DEF)
                    self.info = pokemon.name+" attack "+monster.name
                    self.attack = False
                elif inte == 2:
                    run = random.randint(1,2)
                    if run == 1:
                        self.info = pokemon.name+" escaped!"
                        self.run = True
                    else:
                        self.info = "Escape failed!"
                        self.attack = False
        else:
            if pokemon.HP > 0:
                self.info = "Fight end, "+pokemon.name+" win!"
            else:
                self.info = "Fight end, "+monster.name+" win!"

    def interact(self, inte, canvas):
        canvas.draw_text("What will "+self.pokemon.name+" do?", (80, 370), 20, 'White')
        canvas.draw_text("Attack",(310,370), 20, self.col1)
        canvas.draw_text("Skill",(390,370), 20, self.col2)
        canvas.draw_text("Run",(360,395), 20, self.col3)
        canvas.draw_text("Bag",(360,345), 20, self.col4)
        if self.kbd.left:
            self.col1 = "White"
            self.col2 = self.col3 = self.col4 = "Grey"
            inte = 1
        elif self.kbd.down:
            self.col1 = self.col2 = self.col4 = "Grey"
            self.col3 = "White"
            inte = 2
        elif self.kbd.right:
            self.col1 = self.col3 = self.col4 = "Grey"
            self.col2 = "White"
            inte = 3
        elif self.kbd.up:
            self.col1 = self.col2 = self.col3 = "Grey"
            self.col4 = "White"
            inte = 4
        return inte
        
            
class Pokemon:
    def __init__(self, name, ATK, DEF, HP, MP, IMG, effect_img, pos, row, pos1, row1):
        self.name = name
        self.ATK = ATK
        self.DEF = DEF
        self.HP = HP
        self.MP = MP
        self.count = 0
        # pokemon image
        self.image = simplegui._load_local_image(IMG)
        width = self.image.get_width()
        frame_width = width//5
        height = self.image.get_height()
        frame_height = height//row
        self.pos = pos
        self.frame_center = [frame_width/2, frame_height/2]
        self.frame_dim = [frame_width, frame_height]
        self.frame_index = [0,0]
        self.row = row
        # attack effect image
        self.effectimg = simplegui._load_local_image(effect_img)
        width = self.effectimg.get_width()
        frame_width = width//5
        height = self.effectimg.get_height()
        frame_height = height//row1
        self.pos1 = pos1
        self.frame_center1 = [frame_width/2, frame_height/2]
        self.frame_dim1 = [frame_width, frame_height]
        self.frame_index1 = [0,0]
        self.row1 = row1
        
        


    #def skill(self):
    def draw(self, canvas):
            canvas.draw_image(self.image,
                              [self.frame_center[0] + self.frame_index[0] * self.frame_dim[0],
                               self.frame_center[1] + self.frame_index[1] * self.frame_dim[1]],
                              self.frame_dim, [self.pos[0], self.pos[1]],
                              [self.frame_dim[0]*2,self.frame_dim[1]*2])
            if self.count%10 == 0:
                self.next_frame()
            self.count +=1
    
    def next_frame(self):
        self.frame_index[0] += 1
        if self.frame_index[0] >= 5:
            self.frame_index[0] = 0
            self.frame_index[1] +=1
            if self.frame_index[1] >= self.row:
                self.frame_index[1] = 0
                
    def next_effect(self):
        self.frame_index1[0] += 1
        if self.frame_index1[0] >= 5:
            self.frame_index1[0] = 0
            self.frame_index1[1] +=1
            if self.frame_index1[1] >= self.row1:
                self.frame_index1[1] = 0
                
    def draw_effect(self, canvas):
        canvas.draw_image(self.effectimg,
                          [self.frame_center1[0] + self.frame_index1[0] * self.frame_dim1[0],
                           self.frame_center1[1] + self.frame_index1[1] * self.frame_dim1[1]],
                          self.frame_dim1, [self.pos1[0], self.pos1[1]],
                          [self.frame_dim1[0]+20,self.frame_dim1[1]+20])
        if self.count%4 == 0:
                self.next_effect()


class Keyboard:
    def __init__(self):
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.select = False
        self.quit = False

    def keyDown(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = True
        if key == simplegui.KEY_MAP['left']:
            self.left = True
        if key == simplegui.KEY_MAP['up']:
            self.up = True
        if key == simplegui.KEY_MAP['down']:
            self.down = True
        if key == simplegui.KEY_MAP['q']:
            self.quit = True
        if key == simplegui.KEY_MAP['space']:
            self.select = True

    def keyUp(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = False
        if key == simplegui.KEY_MAP['left']:
            self.left = False
        if key == simplegui.KEY_MAP['up']:
            self.up = False
        if key == simplegui.KEY_MAP['down']:
            self.down = False
        if key == simplegui.KEY_MAP['q']:
            self.quit = False
##        if key == simplegui.KEY_MAP['space']:
##            self.select = False





pikachu = Pokemon('Pikachu', 10, 4, 20, 15, "pokemon1.png", "effect1.png", [120, 260], 6, [370, 180], 9)
squirtle = Pokemon('Squirtle', 5, 8, 20, 15, "pokemon2.png", "effect2.png", [370, 180], 5, [120, 250], 3)
kbd = Keyboard()
fight = Fight(squirtle, pikachu, kbd)
frame = simplegui.create_frame('Interactions', 500, 500)
frame.set_canvas_background('Black')
frame.set_draw_handler(fight.draw)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)
frame.start()
