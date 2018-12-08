from math import exp, log, ceil, floor, fabs, copysign, inf
from tkinter import *
from random import randint, choice
import time
import itertools
import copy


# Functions


def sigmoid(x):
    return 1 / (1 + exp(-x))


# World Constants


worldWIDTH = 2000
worldHEIGHT = 2000
chunkWIDTH = 100
chunkHEIGHT = 100
screenWIDTH = 1000
screenHEIGHT = 800

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

        self.body = screen.create_oval(self.cx - (self.width / 2), self.cy - (self.width / 2), self.cx + (self.width / 2), self.cy + (self.width / 2),
                                       fill=self.hex_col)

        organism_list.append(self)
        print("ENERGIA ENNE-INNITM8",self.energy)
        self.energy = self.energy + (organism_list[0].genecode[2])
        print("ENERGIA PÄRAST-INNITM8",self.energy)
        print("MASS ENNE-INNITM8",self.mass)
        self.mass = self.mass + (organism_list[0].genecode[1])
        print("MASS PÄRAST-INNITM8",self.mass)
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
        if self.energy > 1500:
            self.divide(1000, 400)
        else:

            Default = True
            if Default:
                nearby_entities = []
                bestgoal = self
                bestdistance = inf

                for y in range(self.y_chunk - self.chunk_range, self.y_chunk + self.chunk_range + 1):
                    for x in range(self.x_chunk - self.chunk_range, self.x_chunk + self.chunk_range + 1):
                        for entity in itertools.chain(world_space[y][x]):
                            if entity != self:
                                nearby_entities.append(entity)

                for entity in nearby_entities:
                    if type(entity) == food:
                        distance = (fabs(self.cx - entity.cx)**2 + fabs(self.cy - entity.cy)**2)**(1/2)
                        if distance < bestdistance:
                            bestdistance = distance
                            bestgoal = entity

                x_dir = bestgoal.cx - self.cx
                y_dir = bestgoal.cy - self.cy

            if bestdistance <= self.width/2:
                self.eat(1000, bestgoal)
            elif x_dir != 0 or y_dir != 0:
                self.accelerate(x_dir, y_dir, 5)

    def motor(self):
        self.exist()
        self.move()
        #self.collide()

    # actions

    def eat(self, energy_ratio, entity):
        self.energy += entity.energy * (1000 / (cnsme_dif*10))
        self.energy += (energy_ratio / 1000) * entity.energy * (1000 / (cnsme_dif*10))
        self.mass += ((1000-energy_ratio) / 1000) * entity.mass * (1000/cnsme_dif)
        entity.die()

    def accelerate(self, x, y, e):
        ex = e * (x / (abs(x) + abs(y)))
        ey = e * (y / (abs(x) + abs(y)))
        self.energy -= e*(accel_dif/(1000*10))

        self.vx += (ex / self.mass) * (accel_dif/1000*10) * (1000 / self.HP)
        self.vy += (ey / self.mass) * (accel_dif/1000*10) * (1000 / self.HP)
        
    def divide(self, t, ratio):

        efficiency = (self.HP/1000)*(t/birth_dif)

        m = self.mass * (ratio / 1000) * efficiency
        self.mass *= ((1000 - ratio)/1000)
        e = (self.energy * (ratio / 1000) * efficiency)
        self.energy *= ((1000 - ratio)/1000)
        
        # Hope I don't break it now
        print("ENERGIA ENNE-DIVIDE",self.energy)
        self.energy = self.energy + (organism_list[0].genecode[2])
        print("ENERGIA PÄRAST-DIVIDE",self.energy)
        print("MASS ENNE-DIVIDE",self.mass)
        self.mass = self.mass + (organism_list[0].genecode[1])
        print("MASS PÄRAST-DIVIDE",self.mass)

        w = self.width * ((ratio / 1000)**(1/2))

        self.AC = float((self.width / 4) * self.mass / exist_dif)

        self.width *= (((1000 - ratio)/1000)**(1/2))
        x = self.cx + (self.width + w) / 4
        self.cx += -(self.width + w) / 4
        y = self.cy
        self.cy += -(self.width + w) / 4
        screen.coords(self.body, self.cx - (self.width / 2), self.cy - (self.width / 2), self.cx + (self.width / 2), self.cy + (self.width / 2))

        genecode = self.genecode  # lisa mutateerimisfunktsioon
        Organism(m, e, x, y, w, genecode)


    # state resolution

    def exist(self):
        self.energy -= self.mass * (exist_dif/(1000*100000)) * (1 / self.AC) * (1000 / self.HP)
        if self.energy <= 0:
            self.die()

    def move(self):
        self.cx += self.vx
        self.cy += self.vy
        screen.move(self.body, self.vx, self.vy)
        self.vx += -(mvmnt_dif/(1000*1000))*self.vx
        self.vy += -(mvmnt_dif/(1000*1000))*self.vy

    def die(self):
        screen.delete(self.body)
        del organism_list[organism_list.index(self)]
        del self
        
    def collide(self):
       None

class food:

    def __init__(self):
        self.energy = randint(500, 2500)
        self.mass = randint(500, 2500)
        self.width = (self.energy**(2/5))

        self.cx = randint(round(self.width / 2), screenWIDTH - round(self.width / 2))
        self.cy = randint(round(self.width / 2), screenWIDTH - round(self.width / 2))

        self.body = screen.create_rectangle(self.cx - (self.width / 2), self.cy - (self.width / 2), self.cx + (self.width / 2), self.cy + (self.width / 2),
                                       fill="yellow")

        food_list.append(self)

    def die(self):
        screen.delete(self.body)
        del food_list[food_list.index(self)]
        del self

def create_food():
    for i in range(200):
        food()

def create_initial_population(start_pop, dna_length):
    for creature in range(start_pop):

        m = randint(1000, 2000)
        e = randint(1000, 2000)
        w = randint(30, 60)
        x = randint(round(w / 2), screenWIDTH*0.600 - round(w / 2))
        y = randint(round(w / 2), screenHEIGHT*0.600 - round(w / 2))

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
        x = randint(round(w / 2), screenWIDTH*0.600 - round(w / 2))
        y = randint(round(w / 2), screenHEIGHT*0.600 - round(w / 2))
        
        print("ENERGIA ENNE-CROSSOVER",e)
        e = e + (organism_list[0].genecode[2])
        print("ENERGIA PÄRAST-CROSSOVER",e)
        print("MASS ENNE-CROSSOVER",m)
        m = m + (organism_list[0].genecode[1])
        print("MASS PÄRAST-CROSSOVER",m)
        
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

    elites = fitness(200)
    crossover_children = crossover(200, elites)
    lucky_ones = luckybreed(50)
    mutated = mutation(250)

    for i in range(len(organism_list) - 1, -1, -1):
        if not organism_list[i].markedfordeath:
            new_generation.append(organism_list[i])
        else:
            organism_list[i].die()
    return new_generation

def time_pass():
    print("------")
    for i in range(len(organism_list) - 1, -1, -1):
        organism_list[i].brain()
        organism_list[i].motor()
        print(organism_list[i].genecode)


def update_chunks():
    global world_space

    for y in range(len(world_space)):
        for x in range(len(world_space[y])):
            del world_space[y][x][:]

    for entity in itertools.chain(organism_list, food_list):
        y = floor(entity.cy/chunkHEIGHT)
        x = floor(entity.cx/chunkWIDTH)
        entity.y_chunk = y
        entity.x_chunk = x
        world_space[y][x].append(entity)

##Create Screen
root = Tk()
root.title("Evolutsiooni simulatsioon V0.7")
screen = Canvas(root, width=screenWIDTH, height=screenHEIGHT)
screen.pack()
Populatsiooni_arv = "Unknown"
pop_text = screen.create_text(100,10,text="Populatsioon: "+str(Populatsiooni_arv))

##Create World

world_space = []
for y in range(ceil(worldHEIGHT/chunkHEIGHT)):
    row = []
    for x in range(ceil(worldWIDTH/chunkWIDTH)):
        row.append([])
    world_space.append(copy.deepcopy(row))

create_food()
create_initial_population(10, 3)

root.update()
time.sleep(1)
world_clock = 100
while True:
    world_clock -= 1
    update_chunks()
    screen.delete(pop_text)
    Populatsiooni_arv = (len(organism_list))
    pop_text = screen.create_text(100,10,text="Populatsioon: "+str(Populatsiooni_arv))
    if world_clock == 0:
        generation_pass()
        world_clock = 100
    time_pass()
    for i in range(len(organism_list)):
        organism_list[i].update_color() #ma ei tea kui tihti seda peaks tegema, aga kindlasti mitte iga tsükkel
        organism_list[i].update_tags() #ma ei tea kui tihti seda peaks tegema, aga kindlasti mitte iga tsükkel
    root.update()
    time.sleep(0.05)

##Standard print mode

##create_initial_population(200,3)
##for i in range(len(organism_list)):
##    print(organism_list[i].genecode)
##new_generation = generation_pass()
##for i in range(len(new_generation)):
##    print(new_generation[i].genecode)

##root.mainloop()
