from math import exp, log, ceil, floor, fabs, copysign
from tkinter import *
from random import randint, choice
import time


# Functions


def sigmoid(x):
    return 1 / (1 + exp(-x))


# World Constants


worldWIDTH = 2000
worldHEIGHT = 2000
chunkWIDTH = 50
chunkHEIGHT = 50
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
        self.AC = float((w / 4) * m / exist_dif)
        self.HP = float(1000)
        self.genecode = genecode
        self.elite = False
        self.early = False
        self.child = False
        self.lucky = False
        self.markedfordeath = False

        ACef = round(32 * sigmoid(float((self.AC - 60)) / 30))
        ENGef = round(32 * sigmoid(float((self.energy - 1000) / 500)))
        HPef = round(self.HP / 1000 * 128)

        r_col = str(hex(self.genecode[0])).replace("0x", "").rjust(2, "0")
        g_col = str(hex(self.genecode[1])).replace("0x", "").rjust(2, "0")
        b_col = str(hex(self.genecode[2])).replace("0x", "").rjust(2, "0")
        self.hex_col = "#" + r_col + g_col + b_col

        ##        r_col = str(hex(HPef + ACef + ENGef - 1)).replace("0x", "").rjust(2, "0")
        ##        g_col = str(hex(HPef + ACef - 2*ENGef - 1)).replace("0x", "").rjust(2, "0")
        ##        b_col = str(hex(HPef - 2*ACef - 2*ENGef - 1)).replace("0x", "").rjust(2, "0")

        self.body = screen.create_oval(self.cx - (self.width / 2), self.cy - (self.width / 2), self.cx + (self.width / 2), self.cy + (self.width / 2),
                                       fill=self.hex_col)

        organism_list.append(self)

    # evolution functions

    def update_color(self):
        r_col = str(hex(self.genecode[0])).replace("0x", "").rjust(2, "0")
        g_col = str(hex(self.genecode[1])).replace("0x", "").rjust(2, "0")
        b_col = str(hex(self.genecode[2])).replace("0x", "").rjust(2, "0")
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
        if self.energy > 1000:
            self.divide(1000, 500)
        else:
            self.accelerate(100, 100, 10)

    def motor(self):
        self.exist()
        self.move()

    # actions

    def divide(self, t, ratio):

        efficiency = (self.HP/1000)*(t/birth_dif)

        m = self.mass * (ratio / 1000) * efficiency
        self.mass *= ((1000 - ratio)/1000)
        e = self.energy * (ratio / 1000) * efficiency
        self.energy *= ((1000 - ratio)/1000)

        w = self.width * (ratio / 1000) * (1 / (2 ** (1 / 3)))

        self.width *= ((1000 - ratio)/1000) * (1 / (2 ** (1 / 3)))
        x = self.cx + (self.width + w) / 4
        self.cx += -(self.width + w) / 4
        y = self.cy
        self.cy += -(self.width + w) / 4
        screen.coords(self.body, self.cx - (self.width / 2), self.cy - (self.width / 2), self.cx + (self.width / 2), self.cy + (self.width / 2))



        genecode = self.genecode  # lisa mutateerimisfunktsioon
        Organism(m, e, x, y, w, genecode)

    def accelerate(self, x, y, e):
        ex = e * (x / (abs(x) + abs(y)))
        ey = e * (y / (abs(x) + abs(y)))
        self.energy -= e

        self.vx += (ex / self.mass) * (accel_dif/1000) * (1000 / self.HP)
        self.vy += (ey / self.mass) * (accel_dif/1000) * (1000 / self.HP)

    # state resolution

    def exist(self):
        self.energy -= self.mass * (exist_dif/(1000*100)) * (1 / self.AC) * (1000 / self.HP)
        if self.energy <= 0:
            self.die()

    def move(self):
        screen.move(self.body, self.vx, self.vy)
        self.vx += -(mvmnt_dif/(1000*100))*self.vx
        self.vy += -(mvmnt_dif/(1000*100))*self.vy

    def die(self):
        screen.delete(self.body)
        del organism_list[organism_list.index(self)]
        del self


class food:
    def __init__(self):
        self.food_value = randint(500,2500)
        self.width = (self.food_value**(2/5))
        self.x = randint(round(self.width / 2), screenWIDTH - round(self.width / 2))
        self.y = randint(round(self.width / 2), screenWIDTH - round(self.width / 2))
        self.body = screen.create_oval(self.x - (self.width / 2), self.y - (self.width / 2), self.x + (self.width / 2), self.y + (self.width / 2),
                                       fill="green")


def create_food():
    for i in range(200):
        food()

def create_initial_population(start_pop, dna_length):
    for creature in range(start_pop):

        m = randint(1000, 2000)
        e = randint(1000, 2000)
        w = randint(30, 60)
        x = randint(round(w / 2), screenWIDTH*0.200 - round(w / 2))
        y = randint(round(w / 2), screenHEIGHT*0.200 - round(w / 2))

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
        x = randint(round(w / 2), screenWIDTH*0.200 - round(w / 2))
        y = randint(round(w / 2), screenHEIGHT*0.200 - round(w / 2))
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
    for i in range(len(organism_list) - 1, -1, -1):
        organism_list[i].brain()
        organism_list[i].motor()

def update_chunks():
    for y in range(len(world_space)):
        for x in range(world_space[y]):
            del world_space[y][x][:]

    for i in range(len(organism_list)):
        world_space[floor(organism_list[i].cy/chunkHEIGHT)][floor(organism_list[i].cx/chunkWIDTH)].append(organism_list[i])

##Create Screen
root = Tk()
screen = Canvas(root, width=screenWIDTH, height=screenHEIGHT)
screen.pack()

##Create World

world_space = [[]*(ceil(worldWIDTH/chunkWIDTH))]*(ceil(worldHEIGHT/chunkHEIGHT))

create_food()
create_initial_population(10, 3)

root.update()
time.sleep(1)
world_clock = 1000
while True:
    print(world_clock)
    world_clock -= 1
    if world_clock == 0:
        generation_pass()
        world_clock = 1000
    time_pass()
    for i in range(len(organism_list)):
        organism_list[i].update_color()
        organism_list[i].update_tags()
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
