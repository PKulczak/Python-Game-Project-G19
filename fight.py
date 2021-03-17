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
    def __init__(self, monster_list, pokemon_list, keyboard):
        self.mons_list = monster_list
        self.monster = monster_list[0]
        self.poke_list = pokemon_list
        self.pokemon = pokemon_list[0]
        self.count = 70
        self.attack = True
        self.fullhp = self.pokemon.HP
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
        self.light = simplegui._load_local_image("highlight.png")
        self.first = True
        self.change = False
        self.catch = False
        self.centre = [0,0]
        self.pos = [[(348,145),(348,265),(348,380)],[(598,145),(598,265),(598,380)]]
        #self.end

    def draw(self, canvas):
        if self.change:
            if not self.kbd.quit:
                if not self.kbd.select:
                    canvas.draw_image(self.bag, (375,250), (750,500), (400,240), (735,490))
                    if not self.first:
                        if self.kbd.left and self.centre[0] == 1:
                            self.centre[0] = 0
                            self.first = True
                        elif self.kbd.down and self.centre[1] < 2:
                            self.centre[1] += 1
                            self.first = True
                        elif self.kbd.right and self.centre[0] == 0:
                            self.centre[0] = 1
                            self.first = True
                        elif self.kbd.up and self.centre[1] > 0:
                            self.centre[1] -= 1
                            self.first = True
                    else:
                        if not(self.kbd.left or self.kbd.right or self.kbd.up or self.kbd.down):
                            self.first = False
                    canvas.draw_image(self.light, (116,45), (233,91), self.pos[self.centre[0]][self.centre[1]], (233,91))
                    for i in range(0,len(self.poke_list)):
                        if i<3:
                            canvas.draw_text(self.poke_list[i].name, (270, 130+(i*120)), 25, 'Black')
                            canvas.draw_text("HP:"+str(self.poke_list[i].HP), (350, 160+(i*120)), 25, 'Black')
                        else:
                            canvas.draw_text(self.poke_list[i].name, (520, 130+(i-3)*120), 25, 'Black')
                            canvas.draw_text("HP:"+str(self.poke_list[i].HP), (600, 160+(i-3)*120), 25, 'Black')
                else:
                    if self.centre[0] == 0 :
                        choice = self.centre[0]+self.centre[1]
                    else:
                        choice = self.centre[0]+self.centre[1]+2
                    if self.catch:
                        self.monster.pos = self.pokemon.pos
                        self.monster.pos1 = self.pokemon.pos1
                        self.poke_list[choice] = self.monster
                        self.mons_list.remove(self.monster)
                        self.monster = self.mons_list[0]
                        self.catch = False
                    else:
                        if len(self.poke_list)-1>=choice:
                            self.pokemon = self.poke_list[choice]
                            self.change = False
                        self.kbd.select = False
            else:
                self.change = False
                if self.catch:
                    self.info = "You release it again."
                    self.catch = False
        else:
            canvas.draw_image(self.image, (375,250), (750,500), (400,240), (735,490))
            canvas.draw_text(self.monster.name, (155, 80), 25, 'Black')
            canvas.draw_text("HP:"+str(self.monster.HP), (190, 110), 25, 'Black')
            canvas.draw_text(self.pokemon.name, (530, 255), 25, 'Black')
            canvas.draw_text("HP:"+str(self.pokemon.HP)+"/"+str(self.fullhp), (550, 295), 25, 'Black')
            self.pokemon.draw(canvas)
            self.monster.draw(canvas)
            if self.run:
                canvas.draw_text(self.info, (120, 415), 25, 'White')
            elif self.count != 0:
                if not self.first:
                    if self.attack:
                        self.monster.draw_effect(canvas)
                    else:
                        self.pokemon.draw_effect(canvas)
                canvas.draw_text(self.info, (120, 415), 25, 'White')
                self.count = self.count - 1
            else:
                self.first = False
                if self.attack:
                    if not self.kbd.select:
                        self.inte = self.interact(self.inte, canvas)
                    else:
                        if self.inte <=3 :
                            self.fight(self.pokemon, self.monster, self.inte, canvas)
                            self.kbd.select = False
                            self.count = 130
                        elif self.inte == 4:
                            self.change = True
                            self.kbd.select = False
                else:
                    self.fight(self.pokemon, self.monster, self.inte, canvas)
                    self.count = 110
    def fight(self, pokemon, monster, inte, canvas):
        if pokemon.HP > 0 and monster.HP > 0:
            if not self.attack:
                if monster.ATK>pokemon.DEF:
                    pokemon.HP = pokemon.HP-(monster.ATK - pokemon.DEF)
                else:
                    pokemon.HP = pokemon.HP-1
                self.info = monster.name+" attack "+pokemon.name
                self.attack = True
            else:
                if inte == 1:
                    if pokemon.ATK>monster.DEF:
                        monster.HP = monster.HP-(pokemon.ATK - monster.DEF)
                    else:
                        monster.HP = monster.HP-1
                    if monster.HP<0:
                        monster.HP = 0
                    self.info = pokemon.name+" attack "+monster.name
                    self.attack = False
                elif inte == 2:
                    run = random.randint(1,4)
                    if run == 1:
                        self.info = "You escaped!"
                        self.run = True
                    else:
                        self.info = "Escape failed!"
                        self.attack = False
                elif inte == 3:
                    catch = random.randint(1,5)
                    if catch == 1:
                        if len(self.poke_list) < 6:
                            self.info = "Catch succeed!"
                            self.monster.pos = self.pokemon.pos
                            self.monster.pos1 = self.pokemon.pos1
                            self.poke_list.append(monster)
                            self.mons_list.remove(self.monster)
                            self.monster = self.mons_list[0]
                        else:
                            self.change = True
                            self.catch = True
                    else:
                        self.info = "Catch failed!"
                        self.attack = False
                            
                        
        else:
            if pokemon.HP > 0 and len(self.mons_list) == 0:
                self.info = "Fight end, you win!"
            elif monster.HP >0:
                survive = False
                for i in range(0,len(self.pokemon_list)):
                    if self.poke_list[i].HP>0:
                        survive = True
                if survive:
                    self.change = True
                else:
                    self.info = "Fight end, "+monster.name+" win!"
            elif pokemon.HP > 0:
                self.mons_list.remove(monster)
                if not(len(self.mons_list) == 0):
                    self.monster = self.mons_list[0]
                
    def interact(self, inte, canvas):
        canvas.draw_text("What will "+self.pokemon.name+" do?", (120, 415), 25, 'White')
        canvas.draw_text("Attack",(500,415), 25, self.col1)
        canvas.draw_text("Catch",(600,415), 25, self.col2)
        canvas.draw_text("Run",(560,450), 25, self.col3)
        canvas.draw_text("Bag",(560,380), 25, self.col4)
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
    def __init__(self, name, ATK, DEF, HP, IMG, effect_img, pos, row, pos1, row1):
        self.name = name
        self.ATK = ATK
        self.DEF = DEF
        self.HP = HP
        #self.MP = MP
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
                              [self.frame_dim[0]*3,self.frame_dim[1]*3])
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
                          [self.frame_dim1[0]+35,self.frame_dim1[1]+35])
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





pikachu = Pokemon('Pikachu', 10, 4, 20, "pokemon1.png", "effect1.png", [210, 250], 6, [570, 140], 9)
pokemon2 = Pokemon('Squirtle', 10, 4, 19, "pokemon2.png", "effect1.png", [210, 250], 5, [570, 140], 9)
pokemon3 = Pokemon('Bulbasaur', 10, 4, 18, "pokemon3.png", "effect1.png", [210, 250], 4, [570, 140], 9)
pokemon4 = Pokemon('Charmander', 10, 4, 17, "pokemon1.png", "effect1.png", [210, 250], 6, [570, 140], 9)
pokemon5 = Pokemon('Pidgey', 10, 4, 16, "pokemon1.png", "effect1.png", [210, 250], 6, [570, 140], 9)
#pokemon6 = Pokemon('Kakuna', 10, 4, 15, "pokemon1.png", "effect1.png", [210, 250], 6, [570, 140], 9)
squirtle = Pokemon('Squirtle', 5, 8, 20, "pokemon2.png", "effect2.png", [570, 140], 5, [200, 250], 3)
squirtle1 = Pokemon('Squirtle1', 5, 8, 20, "pokemon2.png", "effect2.png", [570, 140], 5, [200, 250], 3)
squirtle2 = Pokemon('Squirtle2', 5, 8, 20, "pokemon2.png", "effect2.png", [570, 140], 5, [200, 250], 3)
pokemon_list = [pikachu, pokemon2, pokemon3, pokemon4, pokemon5]
monster_list = [squirtle, squirtle1, squirtle2]
kbd = Keyboard()
fight = Fight(monster_list, pokemon_list, kbd)
frame = simplegui.create_frame('Interactions', 800, 480)
frame.set_canvas_background('Black')
frame.set_draw_handler(fight.draw)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)
frame.start()
