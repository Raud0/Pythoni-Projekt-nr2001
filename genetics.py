from math import exp, log, ceil, floor, fabs, copysign, inf, sin
from tkinter import *
from random import randint, choice
import time
import itertools
import copy
# Input Functions

def leftKey(event):
    screen.xview(SCROLL, -10, UNITS)

def rightKey(event):
    screen.xview(SCROLL, 10, UNITS)

def upKey(event):
    screen.yview(SCROLL, -10, UNITS)

def downKey(event):
    screen.yview(SCROLL, 10, UNITS)

def backspaceKey(event):
    global world_speed
    if world_speed > 0.001:
        world_speed -= 0.001
    else:
        world_speed = 0

def returnKey(event):
    global  world_speed
    if world_speed < 0.001:
        world_speed = 0.001
    else:
        world_speed += 0.001


scale = 1
a_scale_mult = 0.8
b_scale_mult = 1/a_scale_mult
def nextKey(event):
    global scale
    scale *= a_scale_mult
    screen.scale("all", 0, 0, a_scale_mult, a_scale_mult)

def priorKey(event):
    global scale
    scale *= b_scale_mult
    screen.scale("all", 0, 0, b_scale_mult, b_scale_mult)

# Mathematical Functions

def sigmoid(x):
    return 1 / (1 + exp(-x))

# World Constants

worldWIDTH = 4000
worldHEIGHT = 4000
chunkWIDTH = 100
chunkHEIGHT = 100
t_chunkWIDTH = 50
t_chunkHEIGHT = 50
screenWIDTH = 1000
screenHEIGHT = 1000

# Interaction Constants
birth_dif = 1000
exist_dif = 1000
accel_dif = 1000
mvmnt_dif = 1000
cnsme_dif = 1000
elite_dif = 1000
mutnt_dif = 1000
lucky_dif = 1000
srvvl_dif = 1000
union_dif = 2000
sunlight = 4
organism_list = []
food_list = []

# Classes and Functions
class Organism:

    # initialize

    def __init__(self, m, e, x, y, w, genecode):
        self.mass = float(m)
        self.energy = float(e)

        self.vx = 0
        self.vy = 0

        self.cx = x
        self.cy = y
        self.width = w

        self.x_chunk = 0
        self.y_chunk = 0

        self.AC = float((self.width / 4) * self.mass / exist_dif)
        self.HP = float(1000)
        self.chunk_range = 1

        self.genecode = genecode

        self.elite = False
        self.early = False
        self.child = False
        self.lucky = False
        self.markedfordeath = False

        self.colour_mode = 2
        if self.colour_mode == 0:
            r_col = str(hex(self.genecode[0])).replace("0x", "").rjust(2, "0")
            g_col = str(hex(self.genecode[1])).replace("0x", "").rjust(2, "0")
            b_col = str(hex(self.genecode[2])).replace("0x", "").rjust(2, "0")
        elif self.colour_mode == 1: # seems like a bad idea, too many calculations, but i guess it's fancy
            self.ACef = round(32 * sigmoid(float((self.AC - 60)) / 30))
            self.ENGef = round(32 * sigmoid(float((self.energy - 1000) / 500)))
            self.HPef = round(self.HP / 1000 * 128)
            r_col = str(hex(self.HPef + self.ACef + self.ENGef - 1)).replace("0x", "").rjust(2, "0")
            g_col = str(hex(self.HPef + self.ACef - 2 * self.ENGef - 1)).replace("0x", "").rjust(2, "0")
            b_col = str(hex(self.HPef - 2 * self.ACef - 2 * self.ENGef - 1)).replace("0x", "").rjust(2, "0")
        elif self.colour_mode == 2:
            self.ENGef = round(32 * sigmoid(float((self.energy - 1000) / 500)))
            r_col = str(hex(8*self.ENGef - 1)).replace("0x", "").rjust(2, "0")
            g_col = str(hex(8*self.ENGef - 1)).replace("0x", "").rjust(2, "0")
            b_col = str(hex(8*self.ENGef - 1)).replace("0x", "").rjust(2, "0")

        self.hex_col = "#" + r_col + g_col + b_col

        self.body = screen.create_oval(round((self.cx - (self.width / 2))*scale, 8), round((self.cy - (self.width / 2))*scale, 8), round((self.cx + (self.width / 2))*scale, 8), round((self.cy + (self.width / 2))*scale, 8), fill=self.hex_col)

        organism_list.append(self)
        # Geen 3 - Mõjutab olendi enerigiat
        # Geen 2 - Mõjutab olendi massi
        # Geen 1 - Mõjutab kui kaugele näevad
        self.energy = self.energy + (organism_list[0].genecode[2])
        self.mass = self.mass + (organism_list[0].genecode[1])
        #self.chunk_range = floor(self.chunk_range + ((organism_list[0].genecode[0]) / 10 )) liiga suur, nägemiskaugus on piiratud selle jaoks, et organismi liiga palju küsimisi ei teeks enda ümber, sest see mõjutab performance'it kõvasti
    # evolution functions

    def update_color(self):
        if self.colour_mode == 0:
            r_col = str(hex(self.genecode[0])).replace("0x", "").rjust(2, "0")
            g_col = str(hex(self.genecode[1])).replace("0x", "").rjust(2, "0")
            b_col = str(hex(self.genecode[2])).replace("0x", "").rjust(2, "0")
        elif self.colour_mode == 1: # seems like a bad idea
            self.ACef = round(32 * sigmoid(float((self.AC - 60)) / 30))
            self.ENGef = round(32 * sigmoid(float((self.energy - 1000) / 500)))
            self.HPef = round(self.HP / 1000 * 128)
            r_col = str(hex(self.HPef + self.ACef + self.ENGef - 1)).replace("0x", "").rjust(2, "0")
            g_col = str(hex(self.HPef + self.ACef - 2 * self.ENGef - 1)).replace("0x", "").rjust(2, "0")
            b_col = str(hex(self.HPef - 2 * self.ACef - 2 * self.ENGef - 1)).replace("0x", "").rjust(2, "0")
        elif self.colour_mode == 2:
            self.ENGef = round(32 * sigmoid(float((self.energy - 1000) / 500)))
            r_col = str(hex(8*self.ENGef - 1)).replace("0x", "").rjust(2, "0")
            g_col = str(hex(8*self.ENGef - 1)).replace("0x", "").rjust(2, "0")
            b_col = str(hex(8*self.ENGef - 1)).replace("0x", "").rjust(2, "0")
        self.hex_col = "#" + r_col + g_col + b_col
        screen.itemconfig(self.body, fill=self.hex_col)

    def update_tags(self):
        self.elite = False
        self.early = False
        self.child = False
        self.lucky = False
        self.markedfordeath = False

    def get_fitness(self):
        self.fitness_rating = 0

        mode = 0
        if mode == 0:
            # blue preference
            for j in range(len(self.genecode)):
                self.fitness_rating += self.genecode[j] * (j ** 2)
        if mode == 1:
            # dark preference
            self.fitness_rating = 1000 / (1 + self.genecode[0] * self.genecode[1] * self.genecode[2])
        if mode == 2:
            # blue dislike
            self.fitness_rating = ((self.genecode[0] ** 2) + (self.genecode[1] ** 2)) / (1 + self.genecode[2])
        if mode == 3:
            # pink!
            x = -(self.genecode[0]) * (self.genecode[0] - 400) / 40000
            y = -(self.genecode[0]) * (self.genecode[0] - 400) / 40000
            self.fitness_rating = (self.genecode[0] ** 2) * x * y

    # Organism systems

    def brain(self):
        thinking_array = [3000 - self.energy, 3000/self.AC, self.energy] # siia võiks geenikordajad panna
        choice = 0
        choice_value = -inf
        for i in range(len(thinking_array)):
            if thinking_array[i] > choice_value:
                choice_value = thinking_array[i]
                choice = i

        if choice == 0: # accelerate towards nearest food
            Default = True
            if Default:
                nearby_entities = []
                bestgoal = self
                bestdistance = inf

                y_floor = min(max(self.y_chunk - self.chunk_range, 0), y_chunkNUM - 1)
                y_ceil = max(min(self.y_chunk + self.chunk_range, y_chunkNUM - 1), 0)
                x_floor = min(max(self.x_chunk - self.chunk_range, 0), x_chunkNUM - 1)
                x_ceil = max(min(self.x_chunk + self.chunk_range, x_chunkNUM - 1), 0)

                for y in range(y_floor, y_ceil + 1):
                    for x in range(x_floor, x_ceil + 1):
                        for entity in itertools.chain(world_space[y][x]):
                            if entity != self:
                                nearby_entities.append(entity)

                for entity in nearby_entities:
                    if type(entity) == food:
                        distance = (fabs(self.cx - entity.cx) ** 2 + fabs(self.cy - entity.cy) ** 2) ** (1 / 2)
                        if distance < bestdistance:
                            bestdistance = distance
                            bestgoal = entity

                x_dir = bestgoal.cx - self.cx
                y_dir = bestgoal.cy - self.cy

            if bestdistance <= ((self.width / 2) + (bestgoal.width / 2)):
                if (bestgoal in food_list) or (bestgoal in organism_list):
                    self.eat(1000, bestgoal)
            elif x_dir != 0 or y_dir != 0:
                self.accelerate(x_dir, y_dir, 5)

        elif choice == 1: # change own shape
            self.grow(200)

        elif choice == 2: # divide
            self.divide(1000, 400)

    def motor(self):
        self.exist()
        self.move()
        #self.collide()

    # actions

    def eat(self, energy_ratio, entity):
        if not entity.markedfordeath:
            before = self.energy
            energy_amount = 0
            energy_amount += entity.energy * (1000 / (cnsme_dif * 10))
            energy_amount += (energy_ratio / 1000) * entity.energy * (1000 / (cnsme_dif * 10))
            eating_time = randint(2,10) # Needs configuration
            energy_gain = (energy_amount/(2*eating_time)) + 2*eating_time
            while eating_time > 0:
                self.energy += energy_gain
                eating_time -= 1
            self.mass += ((1000 - energy_ratio) / 1000) * entity.mass * (1000 / cnsme_dif)
            after = self.energy
            if after < before:
                print("Organism gained negative energy through eating?",after-before)
            entity.die()




    def accelerate(self, x, y, e):
        ex = e * (x / (abs(x) + abs(y)))
        ey = e * (y / (abs(x) + abs(y)))
        self.energy -= e*(accel_dif/(1000*10))

        accel_mods = world_space_terrain[floor(self.cy/t_chunkHEIGHT)][floor(self.cx/t_chunkWIDTH)][0:4]
        a_w = accel_mods[0]
        a_e = accel_mods[1]
        a_n = accel_mods[2]
        a_s = accel_mods[3]
        self.vx += (ex / self.mass) * (accel_dif/1000*10) * (1000 / self.HP)
        if self.vx < 0:
            self.vx *= (1000 + a_w)/1000
        elif self.vx > 0:
            self.vx *= (1000 + a_e)/1000
        self.vy += (ey / self.mass) * (accel_dif/1000*10) * (1000 / self.HP)
        if self.vy < 0:
            self.vy *= (1000 + a_n)/1000
        elif self.vy > 0:
            self.vy *= (1000 + a_s)/1000

    def divide(self, t, ratio):

        efficiency = (self.HP/1000)*(t/birth_dif)

        m = self.mass * (ratio / 1000) * efficiency
        self.mass *= ((1000 - ratio)/1000)
        e = (self.energy * (ratio / 1000) * efficiency)
        self.energy *= ((1000 - ratio)/1000)
        
        # Hope I don't break it now
        self.energy = self.energy + (organism_list[0].genecode[2])
        self.mass = self.mass + (organism_list[0].genecode[1])

        w = self.width * ((ratio / 1000)**(1/2))

        self.AC = float((self.width / 4) * self.mass / exist_dif)

        self.width *= (((1000 - ratio)/1000)**(1/2))
        x = self.cx + (self.width + w) / 4
        self.cx += -(self.width + w) / 4
        y = self.cy
        self.cy += -(self.width + w) / 4
        screen.coords(self.body, (self.cx - (self.width / 2))*scale, (self.cy - (self.width / 2))*scale, (self.cx + (self.width / 2))*scale, (self.cy + (self.width / 2))*scale)

        genecode = self.genecode  # lisa mutateerimisfunktsioon
        Organism(m, e, x, y, w, genecode)

    def grow(self, e):
        self.energy -= e
        self.width += log(e)/(self.AC*(3/2))
        self.AC = float((self.width / 4) * self.mass / exist_dif)

        screen.coords(self.body, (self.cx - (self.width / 2)) * scale, (self.cy - (self.width / 2)) * scale, (self.cx + (self.width / 2)) * scale, (self.cy + (self.width / 2)) * scale)


    # state resolution

    def exist(self):
        self.energy -= self.mass * (exist_dif/(1000*100000)) * (1 / self.AC) * (1000 / self.HP)
        if self.energy <= 0:
            self.die()

    def move(self):
        self.cx += self.vx
        self.cy += self.vy
        screen.move(self.body, (self.vx)*scale, (self.vy)*scale)
        self.vx += -(mvmnt_dif/(1000*1000))*self.vx
        self.vy += -(mvmnt_dif/(1000*1000))*self.vy

    def die(self):
        screen.delete(self.body)
        del organism_list[organism_list.index(self)]
        del self


class food:

    def __init__(self, e, m, x, y, tree_level):
        self.energy = e
        self.mass = m

        if self.energy < 0 or self.mass < 0: # abort
            print("aborted plant creation because of negative energy")
            del self
            return
        self.width = (self.energy**(2/5))

        self.cx = x
        self.cy = y

        self.x_chunk = 0
        self.y_chunk = 0
        self.chunk_range = 2

        self.markedfordeath = False
        self.tree_level = tree_level
        self.expansionlimit = 1000 + 500*(self.tree_level**2)

        r_col = str(hex(int(min(127+32*tree_level, 255)))).replace("0x", "").rjust(2, "0")
        g_col = str(hex(int(max(255-32*tree_level, 0)))).replace("0x", "").rjust(2, "0")
        b_col = str(hex(int(63))).replace("0x", "").rjust(2, "0")
        self.hex_col = "#" + r_col + g_col + b_col

        x_top = round((self.cx - (self.width / 2))*scale, 8)
        y_top = round((self.cy - (self.width / 2))*scale, 8)
        x_bot = round((self.cx + (self.width / 2))*scale, 8)
        y_bot = round((self.cy + (self.width / 2))*scale, 8)

        self.body = screen.create_rectangle(x_top, y_top, x_bot, y_bot, fill=self.hex_col)

        food_list.append(self)

    def brain(self):

        if self.energy > self.expansionlimit:
            self.expand(200)
        else:
            self.photosynthesize()

    def motor(self):
        chunk_fertility = world_space_fertility[self.y_chunk][self.x_chunk]
        if not self.markedfordeath:
            self.energy += chunk_fertility
            self.mass += chunk_fertility
            if self.energy < 10 or self.mass < 10:
                self.markedfordeath = True
            else:
                if chunk_fertility > 5:
                    plants = []
                    for plant in world_space[self.y_chunk][self.x_chunk]:
                        if type(plant) == food:
                            if plant != self and not plant.markedfordeath and plant.tree_level == self.tree_level:
                                distance = min(fabs(plant.cx - self.cx), fabs(plant.cy - self.cy)) - plant.width/2
                                if distance < self.width/2:
                                    plants.append(plant)

                    if len(plants) > 4:
                        energy = self.energy
                        mass = self.mass
                        while len(plants) > 5:
                            del plants[randint(0,len(plants)-1)]
                        for plant in plants:
                            energy += plant.energy
                            mass += plant.mass
                            plant.markedfordeath = True

                        food(energy*(1000/union_dif), mass*(1000/union_dif), self.cx, self.cy, self.tree_level+1)
                        self.markedfordeath = True
        if self.energy < 10 and not self.markedfordeath:
            print("passed through plant with negative energy?!?")



    def expand(self, ratio):
        e = self.energy*(ratio/1000)
        self.energy *= ((1000 - ratio)/1000)
        m = self.mass * (ratio / 1000)
        self.mass *= ((1000 - ratio) / 1000)

        self.width = (self.energy**(2/5))
        food(e, m, (self.cx + randint(-1, 1)*self.width/2), (self.cy + randint(-1, 1)*self.width/2), self.tree_level)

    def photosynthesize(self):
        self.energy += sunlight
        self.mass += sunlight

    def die(self):
        screen.delete(self.body)
        del food_list[food_list.index(self)]
        del self

def create_food():
    for i in range(max(x_chunkNUM*y_chunkNUM*2-len(food_list), 1)):
        food(randint(50, 800), randint(50, 1000), randint(100, worldWIDTH - 100), randint(100, worldHEIGHT - 100), 0)

def create_initial_population(start_pop, dna_length):
    for creature in range(start_pop):

        m = randint(1000, 2000)
        e = randint(1000, 2000)
        w = randint(30, 60)
        x = randint(round(w / 2) + 2*t_chunkWIDTH, worldWIDTH - round(w / 2) - 2*t_chunkWIDTH)
        y = randint(round(w / 2) + 2*t_chunkHEIGHT, worldHEIGHT - round(w / 2) - 2*t_chunkHEIGHT)

        genecode = []
        for j in range(dna_length):
            genecode.append(randint(0, 255))
        Organism(m, e, x, y, w, genecode)
        organism_list[len(organism_list) - 1].early = True

    return organism_list


def fitness(elite_ratio):  # survival_ratio - how many out of a number of srvvl_dif creatures survive
    elite_number = round(elite_ratio / elite_dif * (len(organism_list)))

    elites = []
    ordered_list = []
    for i in range(len(organism_list)):  # Arvutab skoori ja leiab seal elite
        organism_list[i].get_fitness()

        for j in range(len(ordered_list) + 1):
            if j == len(ordered_list):
                ordered_list.insert(j, organism_list[i])
                break
            if organism_list[i].fitness_rating >= ordered_list[j].fitness_rating:
                ordered_list.insert(j, organism_list[i])
                break

    for i in range(elite_number):
        ordered_list[i].elite = True
        elites.append(ordered_list[i])
    return elites


def crossover(mutation_ratio, elites):  # Loob nõ lapsed, võttes kahelt vektrilt 2 suvalist arvu ja loob 3. suvalise arvu
    crossover_children = []
    for i in range(len(elites)):
        new_gene = []

        # Creates new gene code, by mixing the genes of two random organisms.

        main_gene = elites[randint(0, len(elites) - 1)].genecode
        side_gene = elites[randint(0, len(elites) - 1)].genecode
        for x in range(len(main_gene)):
            if x < len(side_gene):
                new_gene.append(choice([main_gene[x], side_gene[x]]))
            else:
                new_gene.append(main_gene[x])

        mutation_number = round(mutation_ratio / mutnt_dif * len(new_gene))
        for i in range(mutation_number):  # Mutates a certain amount of the genes
            new_gene[randint(0, len(new_gene) - 1)] = randint(0, 255)

        # Creates the organism

        m = randint(1000, 2000)
        e = randint(1000, 2000)
        w = randint(30, 60)
        x = randint(round(w / 2), worldWIDTH - round(w / 2))
        y = randint(round(w / 2), worldHEIGHT - round(w / 2))

        e = e + (organism_list[0].genecode[2])
        m = m + (organism_list[0].genecode[1])
        
        Organism(m, e, x, y, w, new_gene)
        organism_list[len(organism_list) - 1].child = True
        crossover_children.append(organism_list[len(organism_list) - 1])

    return crossover_children


def luckybreed(luck_ratio):
    lucky = []
    luck_number = round(luck_ratio / lucky_dif * len(organism_list))
    while len(lucky) < luck_number + 1 and len(organism_list) > luck_number:
        i = randint(0, len(organism_list) - 1)
        if not organism_list[i].elite and not organism_list[i].child and not organism_list[i].lucky:
            lucky.append(organism_list[i])
            organism_list[i].lucky = True

    return lucky


def mutation(death_ratio):  # Mutates the leftovers, srvvl ratio affects how many organisms survive
    mutated = []
    for i in range(len(organism_list)):
        if not organism_list[i].elite and not organism_list[i].child and not organism_list[i].lucky:
            gene_mutation = organism_list[i].genecode
            for j in range(len(gene_mutation)):
                gene_mutation[j] = randint(0, 255)
            organism_list[i].genecode = gene_mutation
            mutated.append(organism_list[i])
            if randint(1, srvvl_dif) < death_ratio:
                organism_list[i].markedfordeath = True
    return mutated



def generation_pass():
    new_generation = []

    create_food()

    elites = fitness(200)
    crossover_children = crossover(200, elites)
    lucky_ones = luckybreed(50)
    mutated = mutation(250)

    for i in range(len(organism_list) -1, -1, -1):
        if not organism_list[i].markedfordeath:
            new_generation.append(organism_list[i])
        else:
            organism_list[i].die()
    return new_generation

def time_pass():
    for i in range(len(organism_list) -1, -1, -1):
        organism_list[i].brain()
        organism_list[i].motor()
    for i in range(len(food_list) -1, -1, -1):
        if not food_list[i].markedfordeath:
            food_list[i].brain()
            food_list[i].motor()
        else:
            food_list[i].die()

def update_chunks():
    global world_space

    for y in range(y_chunkNUM):
        for x in range(x_chunkNUM):
            del world_space[y][x][:]
            world_space_fertility[y][x] = float(0)

    for entity in itertools.chain(organism_list, food_list):
        y = floor(entity.cy/chunkHEIGHT)
        x = floor(entity.cx/chunkWIDTH)
        entity.y_chunk = y
        entity.x_chunk = x
        if (y > y_chunkNUM-1) or (y < 0) or (x > x_chunkNUM-1) or (x < 0):
            entity.die()
        else:
            world_space[y][x].append(entity)
            if type(entity) == food:
                world_space_fertility[y][x] += 1

    for y in range(y_chunkNUM):
        for x in range(x_chunkNUM):
            count = float(world_space_fertility[y][x])
            world_space_fertility[y][x] = -(count-10)*(count-20)*log(count+4)*(1/30)+5

##Create Window

root = Tk()

root.resizable(width=FALSE, height=FALSE)
root.geometry(str(screenWIDTH)+"x"+str(screenHEIGHT))
root.title("Evolutsiooni simulatsioon V0.7")

root.bind("<Left>", leftKey)
root.bind("<Right>", rightKey)
root.bind("<Up>", upKey)
root.bind("<Down>", downKey)
root.bind("<Next>", nextKey)
root.bind("<Prior>", priorKey)
root.bind("<BackSpace>", backspaceKey)
root.bind("<Return>", returnKey)

## World Objects
def river():
    x_kasv = 20.1
    x_tegur = 0.10
    y_amp = 80
    river_xy=[]
    for x in range(200):
        river_xy.append(x*x_kasv)
        river_xy.append(int(sin(x*x_tegur) * y_amp) + 2500)
    return river_xy



##Create Frame

Populatsiooni_arv = StringVar()
Toidu_arv = StringVar()
timer = StringVar()
FPS = StringVar()

status_bar = Frame(root, height=30, relief=SUNKEN, bd=1)
status_bar.pack(side=TOP, fill=X)

l1 = Label(status_bar, text="Populatsioon: ",textvariable=Populatsiooni_arv,width=20,font=("arial",10))
l2 = Label(status_bar, text="Toit: ",textvariable=Toidu_arv,width=20,font=("arial",10))
l3 = Label(status_bar,text="Aeg: ",textvariable=timer,width=20,font=("arial",10))
l4 = Label(status_bar,text="FPS: ",textvariable=FPS,font=("courier",10))
l1.pack(side=LEFT)
l2.pack(side=LEFT)
l3.pack(side=LEFT)
l4.pack(side=RIGHT)

#Create Screen

screen = Canvas(root, width=worldWIDTH, height=worldHEIGHT, xscrollincrement="1", yscrollincrement="1")
screen.create_rectangle(0, 0, worldWIDTH, worldHEIGHT)
jõgi = screen.create_line(river(),fill="blue",width=10)

#Lake
#screen.create_oval(t_chunkWIDTH * randint(1,100), t_chunkHEIGHT * randint(1,100), t_chunkWIDTH * (randint(10,20) + 1), t_chunkHEIGHT * (randint(10,20) + 1),fill="blue")
screen.pack()

##Create World

world_space = []
y_chunkNUM = 0
x_chunkNUM = 0
for y in range(ceil(worldHEIGHT/chunkHEIGHT)):
    row = []
    x_chunkNUM = 0
    for x in range(ceil(worldWIDTH/chunkWIDTH)):
        row.append([])
        x_chunkNUM += 1
    y_chunkNUM += 1
    world_space.append(copy.deepcopy(row))
world_space_fertility = copy.deepcopy(world_space)

##World Terrain
world_space_terrain = []
y_t_chunkNUM = 0
x_t_chunkNUM = 0
for y in range(ceil(worldHEIGHT/t_chunkHEIGHT)):
    row = []
    x_t_chunkNUM = 0
    for x in range(ceil(worldWIDTH/t_chunkWIDTH)):
        row.append([])
        x_t_chunkNUM += 1
    y_t_chunkNUM += 1
    world_space_terrain.append(copy.deepcopy(row))

for y in range(y_t_chunkNUM):
    for x in range(x_t_chunkNUM):
        a_w = 0
        a_e = 0
        a_n = 0
        a_s = 0
        vx = 0
        vy = 0
        if y <= 1:
            a_n += -200
            a_s += -a_n
            screen.create_rectangle(t_chunkWIDTH * x, t_chunkHEIGHT * y, t_chunkWIDTH * (x + 1), t_chunkHEIGHT * (y + 1), fill="blue")

        if y >= y_t_chunkNUM - 2:
            a_s += -200
            a_n += -a_s
            screen.create_rectangle(t_chunkWIDTH * x, t_chunkHEIGHT * y, t_chunkWIDTH * (x + 1), t_chunkHEIGHT * (y + 1), fill="blue")

        if x <= 1:
            a_w += -200
            a_e += -a_w
            screen.create_rectangle(t_chunkWIDTH * x, t_chunkHEIGHT * y, t_chunkWIDTH * (x + 1), t_chunkHEIGHT * (y + 1), fill="blue")

        if x >= y_t_chunkNUM - 2:
            a_e += -200
            a_w += -a_e
            screen.create_rectangle(t_chunkWIDTH * x, t_chunkHEIGHT * y, t_chunkWIDTH * (x + 1), t_chunkHEIGHT * (y + 1), fill="blue")

        world_space_terrain[y][x] = (a_w, a_e, a_n, a_s, vx, vy)

##Initialize Entities

create_food()
create_initial_population(50, 3)

#Main Cycle

root.update()
time.sleep(1)
world_speed = 0.05
Aeg = 1000
world_clock = Aeg
while True:
    start_time = time.time()

    world_clock -= 1

    update_chunks()

    Populatsiooni_arv.set("Populatsioon: "+str((len(organism_list))))
    Toidu_arv.set("Toit: "+str((len(food_list))))
    timer.set("Aeg: "+str(world_clock))
    if len(organism_list) < 20:
        l1.config(fg="red")
    else:
        l1.config(fg="green")
    if len(food_list) < 200:
        l2.config(fg="red")
    else:
        l2.config(fg="green")
    if (world_clock) < 100:
        l3.config(fg="red")
    else:
        l3.config(fg="green")

    time_pass()
    if world_clock == 0:
        generation_pass()
        world_clock = Aeg
    #Leiab need objektid mis on jõe peal #jõgi = screen.find_overlapping(screen.coords(jõgi)[0],screen.bbox(jõgi)[1],screen.bbox(jõgi)[2],screen.bbox(jõgi)[3])
    if world_clock % 10:
        for i in range(len(organism_list)):
            organism_list[i].update_color()
            organism_list[i].update_tags()

    root.update()
    time.sleep(world_speed)
    if world_clock%5:
        FPS.set("FPS: "+str(round(1.0/(time.time()-start_time), 2)))


##Standard print mode

##create_initial_population(200,3)
##for i in range(len(organism_list)):
##    print(organism_list[i].genecode)
##new_generation = generation_pass()
##for i in range(len(new_generation)):
##    print(new_generation[i].genecode)

##root.mainloop()
