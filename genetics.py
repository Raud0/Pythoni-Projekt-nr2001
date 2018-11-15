from math import exp
from tkinter import *
from random import randint, choice

# Functions


def sigmoid(x):
    return 1/(1 + exp(-x))

# World Constants


worldWIDTH = 2000
worldHEIGHT = 2000
screenWIDTH = 1000
screenHEIGHT = 800

root = Tk()
screen = Canvas(root, width=screenWIDTH, height=screenHEIGHT)
screen.pack()

# Interaction Constants
birth_dif = 1000
exist_dif = 1000
accel_dif = 1000
mvmnt_dif = 1000
cnsme_dif = 1000
elite_dif = 1000
mutnt_dif = 1000
lucky_dif = 1000
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
        self.AC = float((w/4)*m/exist_dif)
        self.HP = float(1000)
        self.genecode = genecode
        self.elite = False
        self.child = False
        self.lucky = False

        ACef = round(32*sigmoid(float((self.AC-60))/30))
        ENGef = round(32*sigmoid(float((self.energy-1000)/500)))
        HPef = round(self.HP/1000*128)

        r_col = str(hex(HPef + ACef + ENGef - 1)).replace("0x", "").rjust(2, "0")
        g_col = str(hex(HPef + ACef - 2*ENGef - 1)).replace("0x", "").rjust(2, "0")
        b_col = str(hex(HPef - 2*ACef - 2*ENGef - 1)).replace("0x", "").rjust(2, "0")
        hex_col = "#" + r_col + g_col + b_col
        self.body = screen.create_oval(self.cx-(w/2), self.cy-(w/2), self.cx+(w/2), self.cy+(w/2), fill=hex_col)

        organism_list.append(self)

    # evolution functions

    def get_fitness(self):
        self.fitness_rating = 0
        for j in range(len(self.genecode)):
            self.fitness_rating *= self.genecode[j]
        self.fitness_rating = self.fitness_rating ** (1 / len(self.genecode))

    # actions

    def divide(self, t, ratio):
        m = self.mass * (1-ratio) * (1/2) * (1-(birth_dif/t)) * (1000/self.HP)
        self.mass *= (1+ratio) * (1/2)
        w = self.width * (1-ratio) * (1/(2**(1/3)))
        self.width *= (1+ratio) * (1/(2**(1/3)))
        e = self.energy * (1 - ratio) * (1 / 2) * (1-(birth_dif/t)) * (1000/self.HP)
        self.energy *= (1 + ratio) * (1 / 2)
        x = self.cx +(self.width+w)/4
        self.cx += -(self.width+w)/4
        y = self.cy
        self.cy += 0
        genecode = self.genecode #lisa mutateerimisfunktsioon
        Organism(m, e, x, y, w, genecode)

    def accelerate(self, x, y, e):
        ex = e * (x/(abs(x)+abs(y)))
        ey = e * (y/(abs(x)+abs(y)))
        self.energy -= e
        self.vx += (ex/self.mass) * (1/accel_dif) * (1000/self.HP)
        self.vy += (ey/self.mass) * (1/accel_dif) * (1000/self.HP)

    # state resolution

    def exist(self):
        self.energy -= self.mass * exist_dif * (1/self.AC) * (1000/self.HP)
        if self.energy <= 0:
            self.die()

    def move(self):
        screen.move(self.body, self.vx, self.vy)
        self.vx += -(1/mvmnt_dif)
        self.vy += -(1/mvmnt_dif)

    def die(self):
        screen.delete(self.body)
        del organism_list[organism_list.index(self)]
        del self


def create_initial_population(start_pop, dna_length):

    for creature in range(start_pop):

        m = randint(1000, 2000)
        e = randint(1000, 2000)
        w = randint(30, 60)
        x = randint(round(w/2), screenWIDTH-round(w/2))
        y = randint(round(w/2), screenHEIGHT-round(w/2))

        genecode = []
        for j in range(dna_length):
            genecode.append(randint(1,500))

        Organism(m, e, x, y, w, genecode)

    return organism_list


def fitness(elite_ratio): # survival_ratio - how many out of a number of srvvl_dif creatures survive
    elite_number = round(elite_ratio/elite_dif)

    elites = []
    ordered_list = []
    for i in range(len(organism_list)): # Arvutab skoori ja leiab seal elite
        organism_list[i].get_fitness()

        for j in range(len(ordered_list)+1):
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


def crossover(mutation_ratio, elites): # Loob nõ lapsed, võttes kahelt vektrilt 2 suvalist arvu ja loob 3. suvalise arvu
    crossover_children = []
    for i in range(len(elites)):
        new_gene = []

        # Creates new gene code, by mixing the genes of two random organisms.

        main_gene = elites[randint(0, len(elites)-1)].genecode
        side_gene = elites[randint(0, len(elites)-1)].genecode
        for x in range(len(main_gene)):
            if x < len(side_gene):
                new_gene.append(choice(main_gene[x], side_gene[x]))
            else:
                new_gene.append(main_gene[x])

        mutation_number = round(mutation_ratio / mutnt_dif * len(new_gene))
        for i in range(mutation_number): # Mutates a certain amount of the genes
            new_gene[randint(0, len(new_gene)-1)] = randint(1, 500)

        # Creates the organism

        m = randint(1000, 2000)
        e = randint(1000, 2000)
        w = randint(30, 60)
        x = randint(round(w / 2), screenWIDTH - round(w / 2))
        y = randint(round(w / 2), screenHEIGHT - round(w / 2))
        Organism(m, e, x, y, w, new_gene)
        organism_list[len(organism_list)-1].child = True
        crossover_children.append(organism_list[len(organism_list)-1])

    return crossover_children


def luckybreed(luck_ratio):
    lucky = []
    luck_number = round(luck_ratio/lucky_dif*len(organism_list))
    while len(lucky) < luck_number+1:
        i = randint(0, len(organism_list)-1)
        if not organism_list[i].elite and not organism_list[i].child and not organism_list[i].lucky:
            lucky.append(organism_list[i])
            organism_list[i].lucky = True

    return lucky


def mutation(): # Mutates the leftovers
    mutated = []
    for i in range(len(organism_list)):
        if not organism_list[i].elite and not organism_list[i].child and not organism_list[i].lucky:
            gene_mutation = organism_list[i].genecode
            for j in range(len(gene_mutation)):
                gene_mutation[j] = randint(1,500)
            organism_list[i].genecode = gene_mutation
            mutated.append(organism_list[i])
    return mutated


def generation_pass():
    new_generation = []

    elites = fitness(100)
    crossover_children = crossover(333,elites)
    lucky_ones = luckybreed(100)
    mutated = mutation()

    for i in elites:
        new_generation.append(i)
    for i in crossover_children:
        new_generation.append(i)
    for i in lucky_ones:
        new_generation.append(i)
    for i in mutated:
        new_generation.append(i)

    return new_generation


create_initial_population(200,3)
for i in range(len(organism_list)):
    print(organism_list[i].genecode)
new_generation = generation_pass()
for i in range(len(new_generation)):
    print(new_generation[i].genecode)

root.mainloop()
