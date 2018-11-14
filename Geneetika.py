from random import randint
from math import pi, exp
from tkinter import *

def sigmoid(x):
    return 1/(1 + exp(-x))

birth_dif = 1000
exist_dif = 1000
accel_dif = 1000
mvmnt_dif = 1000
cnsme_dif = 1000

organism_list = []

root = Tk()

worldWIDTH = 2000
worldHEIGHT = 2000
screenWIDTH = 1000
screenHEIGHT = 800

screen = Canvas(root, width=screenWIDTH, height=screenHEIGHT)
screen.pack()


class Organism:

    # initialize

    def __init__(self, m, e, x, y, w):
        self.mass = float(m)
        self.energy = float(e)
        self.vx = 0
        self.vy = 0
        self.cx = x
        self.cy = y
        self.width = w
        self.AC = float((w/4)*m/exist_dif)
        self.HP = float(1000)

        ACef = round(32*sigmoid(float((self.AC-60))/30))
        ENGef = round(32*sigmoid(float((self.energy-1000)/500)))
        HPef = round(self.HP/1000*128)

        r_col = str(hex(HPef + ACef + ENGef - 1)).replace("0x", "").rjust(2, "0")
        g_col = str(hex(HPef + ACef - 2*ENGef - 1)).replace("0x", "").rjust(2, "0")
        b_col = str(hex(HPef - 2*ACef - 2*ENGef - 1)).replace("0x", "").rjust(2, "0")
        hex_col = "#" + r_col + g_col + b_col
        self.body = screen.create_oval(self.cx-(w/2), self.cy-(w/2), self.cx+(w/2), self.cy+(w/2), fill=hex_col)

        organism_list.append(self)

    # actions

    def divide(self, t, ratio):
        m = self.mass * (1-ratio) * (1/2) * (1-(birth_dif/t)) * (1000/self.HP)
        self.mass *= (1+ratio) * (1/2)
        w = self.width * (1-ratio) * (1/(2^(1/3)))
        self.width *= (1+ratio) * (1/(2^(1/3)))
        e = self.energy * (1 - ratio) * (1 / 2) * (1-(birth_dif/t)) * (1000/self.HP)
        self.energy *= (1 + ratio) * (1 / 2)
        x = self.cx +(self.width+w)/4
        self.cx += -(self.width+w)/4
        y = self.cy
        self.cy += 0
        Organism(m, e, x, y, w)

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


def esialgne_populatsioon(isendite_arv, muutuja):
    alg_populatsioon = []

    for i in range(isendite_arv):
        alg_populatsioon.append([randint(0,200)])
        m = randint(1000, 2000)
        e = randint(1000, 2000)
        w = randint(30, 60)
        x = randint(round(w/2), screenWIDTH-round(w/2))
        y = randint(round(w/2), screenHEIGHT-round(w/2))
        Organism(m, e, x, y, w)

        for x in range(muutuja-1):
            alg_populatsioon[i].append(randint(0,200))
    return alg_populatsioon


esialgne_populatsioon(100, 3)

def fitness(populatsioon,edasi): # edasi - Mitu elite viiakse üle järgmisesse generatsiooni
    parimskoor = []
    skoor = []
    elite = []
    for i in range(len(populatsioon)): # Arvutab skoori ja leiab seal elite
        x = populatsioon[i][0]
        y = populatsioon[i][1]
        z = populatsioon[i][2]
        fitness_rating = (2*x+1)**2 + (3*y+4)**2 + (z-2)**2
        skoor.append(fitness_rating)
    for i in range(edasi):
        temp = max(skoor)
        parimskoor.append(temp)
        skoor.remove(temp)
        
    for i in range(len(populatsioon)): # Leiab, millistel vektoritel olid elite tulemued ja lisab listi elite
        x = populatsioon[i][0]
        y = populatsioon[i][1]
        z = populatsioon[i][2]
        fitness_rating = (2*x+1)**2 + (3*y+4)**2 + (z-2)**2
        for el in range(len(parimskoor)):
            if fitness_rating == parimskoor[el]:
                elite.append(populatsioon[i])
                
        
        
    return elite

def crossover(elite): # Loob nõ lapsed, võttes kahelt vektrilt 2 suvalist arvu ja loob 3. suvalise arvu
    crossover_children = [[],[],[],[]]
    for i in range(len(elite)): # Võtab 2 suvaliselt arvu vanematelt
        for j in range(len(elite[0])-1):
            gene = elite[randint(0,3)][randint(0,2)]
            crossover_children[i].append(gene)
    for i in range(len(elite)): # Lisab suvalise arvu
        crossover_children[i].append(randint(0,200))
    return crossover_children

def lucky(populatsioon):
    lucky = []
    elite = fitness(populatsioon,4)
    for i in range(20):
        if populatsioon[i] != elite[0] and populatsioon[i] != elite[1] and populatsioon[i] != elite[2] and populatsioon[i] != elite[3]:
            lucky.append(populatsioon[i])
            if len(lucky) == 4:
                break
    return lucky
    
def mutation(algpopulatsioon,elite,lucky): # Võtab ülejäänud algpopulatsioonist ja muudab nende elemente suvaliselt
    mutation_children = []
    mutation_canditates = algpopulatsioon[:]
    elite = fitness(algpopulatsioon,4)
    lucky = lucky(algpopulatsioon)
    while len(mutation_children) != 8:
        for i in range(1):
            if mutation_canditates[i] in elite or mutation_canditates[i] in lucky:
                mutation_canditates.remove(mutation_canditates[i])
            else:
                mutation_children.append(mutation_canditates[i])
                mutation_canditates.remove(mutation_canditates[i])
                
    for i in range(len(mutation_children)):
        for j in range(randint(0,len(mutation_children[0]))):
            mutation_children[i][j] = randint(0,200)
        
    return mutation_children

def next_gen(population):
    new_generation = []
    elite = fitness(population,4)
    crossover_x = crossover(elite)
    lucky_x = lucky(population)
    mutation_x = mutation(population,elite,lucky)
    for i in elite:
        new_generation.append(i)
    for i in crossover_x:
        new_generation.append(i)
    for i in lucky_x:
        new_generation.append(i)
    for i in mutation_x:
        new_generation.append(i)
    return new_generation

esimene_pop = esialgne_populatsioon(200,3)
print(next_gen(esimene_pop))

root.mainloop()
