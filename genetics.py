from math import exp, log, ceil, floor, fabs, copysign, inf, sin, pi
from tkinter import *
from tkinter import messagebox, colorchooser
from random import randint, choice
from statistics import mean
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

# https://en.wikipedia.org/wiki/Approximate_entropy
#
# def ApEn(U, m, r):
#
#     def _maxdist(x_i, x_j):
#         return max([abs(ua - va) for ua, va in zip(x_i, x_j)])
#
#     def _phi(m):
#         x = [[U[j] for j in range(i, i + m - 1 + 1)] for i in range(N - m + 1)]
#         C = [len([1 for x_j in x if _maxdist(x_i, x_j) <= r]) / (N - m + 1.0) for x_i in x]
#         return (N - m + 1.0)**(-1) * sum(np.log(C))
#
#     N = len(U)
#
#     return abs(_phi(m+1) - _phi(m))



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

# Generation Pass
elite_ratio_constant = 200
crossover_mutation_constant = 200
lucky_survivor_constant = 50
generation_death_constant = 250

# Special Constants
gene_range = 0
sunlight = 2.5
Aeg = 1000
initialpopulationnum = 50
plant_per_chunk = 2
lake_amount = 10

organism_list = []
food_list = []

# Classes and Functions
class Organism:

    # initialize

    def __init__(self, m, e, x, y, w, genecode):
        global exist_dif
        self.mass = float(m)
        self.energy = float(e)

        if self.mass < 10 or self.energy < 10:
            print("stillbirth of " + str(self))
            del self
            return

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

        for i in self.genecode:
            if i <= 0 or i >= 1000:
                print("miscarriage of " + str(self))
                del self
                return

        self.genecomplexity = self.gene_evaluator(genecode)
        self.elite = False
        self.early = False
        self.child = False
        self.lucky = False
        self.markedfordeath = False

        self.age = 1
        self.divisions = 1

        self.friends = [self]
        self.enemies = []
        global colour_mode
        
        if colour_mode == 0:
            b_sum = 0
            g_sum = 0
            r_sum = 0
            part = floor(len(self.genecode)/3)
            for i in range(len(self.genecode)):
                if i <= part:
                    b_sum += self.genecode[i]
                elif i <= part*2:
                    g_sum += self.genecode[i]
                else:
                    r_sum += self.genecode[i]
            b_sum = b_sum / (part * 1000)
            g_sum = g_sum / (part * 1000)
            r_sum = r_sum / ((len(self.genecode) - 2 * part) * 1000)
            r_col = str(hex(floor(r_sum * 255))).replace("0x", "").rjust(2, "0")
            g_col = str(hex(floor(g_sum * 255))).replace("0x", "").rjust(2, "0")
            b_col = str(hex(floor(b_sum * 255))).replace("0x", "").rjust(2, "0")
        elif colour_mode == 1:
            print(self.AC,self.HP,self.age)
            self.ACef = round(32 * sigmoid(float((self.AC - 20) / 10)))
            self.HPef = round(32 * sigmoid(float((self.HP - 500) / 250)))
            self.AGEef = round(32 * sigmoid(-float((self.age - 1000) / 500)))
            print(self.ACef, self.HPef, self.AGEef)
            r_col = str(hex(max(8 * self.ACef - 1, 0))).replace("0x", "").rjust(2, "0")
            g_col = str(hex(max(8 * self.HPef - 1, 0))).replace("0x", "").rjust(2, "0")
            b_col = str(hex(max(8 * self.AGEef - 1, 0))).replace("0x", "").rjust(2, "0")
        elif colour_mode == 2: # Energy Mode
            self.ENGef = round(32 * sigmoid(float((self.energy - 1000) / 500)))
            r_col = str(hex(8*self.ENGef - 1)).replace("0x", "").rjust(2, "0")
            g_col = str(hex(8*self.ENGef - 1)).replace("0x", "").rjust(2, "0")
            b_col = str(hex(8*self.ENGef - 1)).replace("0x", "").rjust(2, "0")

        self.hex_col = "#" + r_col + g_col + b_col

        self.body = screen.create_oval(round((self.cx - (self.width / 2))*scale, 8), round((self.cy - (self.width / 2))*scale, 8), round((self.cx + (self.width / 2))*scale, 8), round((self.cy + (self.width / 2))*scale, 8), fill=self.hex_col)

        organism_list.append(self)
        # Geen 0: ??
        # Geen 1: Maagiline energia
        # Geen 2: Maagiline mass
        # Geen 3: Eating Weight
        # Geen 4: Growing Weight
        # Geen 5: Division Weight
        # Geen 6: Division Ratio
        # Geen 7: Bite size
        # Geen 8: Growth Ratio

        self.energy += (self.genecode[2])/10
        self.mass += (self.genecode[1])/10
        #self.chunk_range = floor(self.chunk_range + ((organism_list[0].genecode[0]) / 10 )) liiga suur, nägemiskaugus on piiratud selle jaoks, et organismi liiga palju küsimisi ei teeks enda ümber, sest see mõjutab performance'it kõvasti
    # evolution functions

    def gene_evaluator(self,genes1,genes2=[]):
        collector = 0

        if len(genes2) == 0:
            for i in range(len(genes1)):
                collector += (fabs(500-genes1[i]))/500
            collector *= collector

        else:
            i_range = min(len(genes1),len(genes2))
            for i in range(i_range):
                collector += fabs(genes1[i]-genes2[i])/(fabs(genes1[i])+1)
            collector += fabs(len(genes1) - len(genes2))

        return collector


    def update_color(self):
        global colour_mode
        if colour_mode == 0:
            b_sum = 0
            g_sum = 0
            r_sum = 0
            part = floor(len(self.genecode)/3)
            for i in range(len(self.genecode)):
                if i <= part:
                    b_sum += self.genecode[i]
                elif i <= part * 2:
                    g_sum += self.genecode[i]
                else:
                    r_sum += self.genecode[i]
            b_sum = b_sum / (part * 1000)
            g_sum = g_sum / (part * 1000)
            r_sum = r_sum / ((len(self.genecode) - 2 * part) * 1000)
            r_col = str(hex(floor(r_sum*255))).replace("0x", "").rjust(2, "0")
            g_col = str(hex(floor(g_sum*255))).replace("0x", "").rjust(2, "0")
            b_col = str(hex(floor(b_sum*255))).replace("0x", "").rjust(2, "0")
        elif colour_mode == 1:
            print(self.AC, self.HP, self.age)
            self.ACef = round(32 * sigmoid(float((self.AC - 20) / 10)))
            self.HPef = round(32 * sigmoid(float((self.HP - 500) / 250)))
            self.AGEef = round(32 * sigmoid(-float((self.age - 1000) / 500)))
            print(self.ACef, self.HPef, self.AGEef)
            r_col = str(hex(max(8 * self.ACef - 1, 0))).replace("0x", "").rjust(2, "0")
            g_col = str(hex(max(8 * self.HPef - 1, 0))).replace("0x", "").rjust(2, "0")
            b_col = str(hex(max(8 * self.AGEef - 1, 0))).replace("0x", "").rjust(2, "0")
        elif colour_mode == 2: # Energy Mode
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
            # default fitness
            self.fitness_rating = self.age*self.age/self.divisions
        elif mode == 1:
            # blue preference
            for j in range(len(self.genecode)):
                self.fitness_rating += self.genecode[j] * (j ** 2)
        elif mode == 2:
            # dark preference
            self.fitness_rating = 1000 / (1 + self.genecode[0] * self.genecode[1] * self.genecode[2])
        elif mode == 3:
            # blue dislike
            self.fitness_rating = ((self.genecode[0] ** 2) + (self.genecode[1] ** 2)) / (1 + self.genecode[2])
        elif mode == 4:
            # pink!
            x = -(self.genecode[0]) * (self.genecode[0] - 400) / 40000
            y = -(self.genecode[0]) * (self.genecode[0] - 400) / 40000
            self.fitness_rating = (self.genecode[0] ** 2) * x * y

    # Organism systems

    def brain(self):
        # Geen 3: Eating Weight
        # Geen 4: Growing Weight
        # Geen 5: Division Weight
        # Geen 6: Division Ratio
        # Geen 7: Bite size
        # Geen 8: Growth Ratio
        # Geen 9: Enemy Memory Length
        # Geen 10: Bravery
        # Geen 11: Recovery
        if self.HP <= 0:
            self.HP = 1
        if self.AC <= 0:
            self.markedfordeath = True
            return

        thinking_array = [(3000 - self.energy)*(self.genecode[3]/1000), (3000/self.AC)*(self.genecode[4]/1000), (self.energy)*(self.genecode[5]/1000), self.energy*min(0,600-self.HP)*(self.genecode[11]/500)] # siia võiks geenikordajad panna
        choice = 0
        choice_value = -inf
        for i in range(len(thinking_array)):
            if thinking_array[i] > choice_value:
                choice_value = thinking_array[i]
                choice = i

        if choice == 0: # accelerate towards nearest food
            Default = True
            if Default:
                bestgoal = self
                bestvalue = -inf
                bestdistance = inf
                worstgoal = self
                worstvalue = -inf

                y_floor = min(max(self.y_chunk - self.chunk_range, 0), y_chunkNUM - 1)
                y_ceil = max(min(self.y_chunk + self.chunk_range, y_chunkNUM - 1), 0)
                x_floor = min(max(self.x_chunk - self.chunk_range, 0), x_chunkNUM - 1)
                x_ceil = max(min(self.x_chunk + self.chunk_range, x_chunkNUM - 1), 0)

                for y in range(y_floor, y_ceil + 1):
                    for x in range(x_floor, x_ceil + 1):
                        for entity in itertools.chain(world_space[y][x]):
                            if (type(entity) == Organism) and entity not in self.friends:
                                should = self.gene_evaluator(self.genecode,entity.genecode)
                                if should < 0.05:
                                    self.friends.append(entity)
                                else:
                                    if entity.width > self.width:
                                        self.enemies.append(entity)
                            if entity in self.enemies:
                                distance = (fabs(self.cx - entity.cx) ** 2 + fabs(self.cy - entity.cy) ** 2) ** (1 / 2)
                                value = entity.mass*entity.width/(distance*distance)*(self.genecode[10]/500)
                                if value > worstvalue:
                                    worstvalue = value
                                    worstgoal = entity
                            elif entity not in self.friends:
                                distance = (fabs(self.cx - entity.cx) ** 2 + fabs(self.cy - entity.cy) ** 2) ** (1 / 2)
                                value = entity.width/distance
                                if value > bestvalue:
                                    bestvalue = value
                                    bestdistance = distance
                                    bestgoal = entity

                x_dir = 0
                y_dir = 0
                if bestvalue > worstvalue:
                    if bestgoal != self:
                        x_dir += bestgoal.cx - self.cx
                        y_dir += bestgoal.cy - self.cy
                else:
                    if worstgoal != self:
                        x_dir += self.cx - worstgoal.cx
                        y_dir += self.cy - worstgoal.cy

                if bestdistance <= ((self.width / 2) + (bestgoal.width / 2)):
                    if not bestgoal == self and ((bestgoal in food_list) or (bestgoal in organism_list)):
                        self.eat(1000, self.genecode[7]/10, bestgoal)
                        if self.vx > 0 or self.vy > 0:
                            self.accelerate(-self.vx, -self.vy, 5)
                elif x_dir != 0 or y_dir != 0:
                    self.accelerate(x_dir, y_dir, 5)

        elif choice == 1: # change own shape
            self.grow(self.genecode[8]/2)

        elif choice == 2: # divide
            self.divide(1000, self.genecode[6])

        elif choice == 3:
            if self.HP < 800:
               self.recover(self.genecode[11])

    def motor(self):
        if len(self.enemies) > self.genecode[9]/100 and len(self.enemies) > 0:
            del self.enemies[0]
        if self.HP <= 0:
            self.HP = 1
        self.age += 1
        self.exist()
        self.move()
        #self.collide()

    # actions

    def eat(self, energy_ratio, bite_size, entity):
        global cnsme_dif

        if not entity.markedfordeath:
            if type(entity) == Organism and entity.HP > 300:
                bite = bite_size
                entity.vx += self.vx * (bite_size/300)
                entity.vy += self.vy * (bite_size/3000)
                self.energy -= bite*0.05
                bite *= sigmoid(-(entity.AC - 20) / 10) * sigmoid(-(bite_size - 200) / 100)
                entity.HP -= bite*(1000/entity.HP)
                entity.HP -= self.mass * ((self.vx)**2 + (self.vy)**2)**(1/2) / 100
                if entity.HP <= 0:
                    entity.HP = 1
            else:
                bite = bite_size
                entity.energy -= bite
                entity.mass -= bite
                if entity.mass < 0 or entity.energy < 0:
                    bite_size += (entity.mass + entity.energy)
                    entity.markedfordeath = True
                bite *= sigmoid(-(entity.AC-20)/10)*sigmoid(-(bite_size-200)/100)
                self.energy += bite * (1000 / (cnsme_dif * 10)) * (energy_ratio/1000)
                self.mass += bite * (1000 / cnsme_dif) * ((1000-energy_ratio)/1000)




    def accelerate(self, x, y, e):
        global accel_dif

        ex = e * (x / (fabs(x) + fabs(y)))
        ey = e * (y / (fabs(x) + fabs(y)))
        self.energy -= e*(accel_dif/(1000*10))

        accel_mods = world_space_terrain[floor(self.cy/t_chunkHEIGHT)][floor(self.cx/t_chunkWIDTH)][0:4]
        a_w = accel_mods[0]
        a_e = accel_mods[1]
        a_n = accel_mods[2]
        a_s = accel_mods[3]
        self.vx += (ex / self.mass) * (accel_dif/1000*10) * (self.HP/1000)
        if self.vx < 0:
            self.vx *= (1000 + a_w)/1000
        elif self.vx > 0:
            self.vx *= (1000 + a_e)/1000
        self.vy += (ey / self.mass) * (accel_dif/1000*10) * (self.HP/1000)
        if self.vy < 0:
            self.vy *= (1000 + a_n)/1000
        elif self.vy > 0:
            self.vy *= (1000 + a_s)/1000

    def divide(self, t, ratio):
        global birth_dif
        global exist_dif

        efficiency = (self.HP/1000)*(t/birth_dif) * (10-self.genecomplexity)/10
        if efficiency < 0 or ratio < 0:
            return
        if self.width < 0:
            self.markedfordeath = True
            return

        self.divisions += 1
        m = self.mass * (ratio / 1000) * efficiency
        self.mass *= ((1000 - ratio)/1000)
        e = (self.energy * (ratio / 1000) * efficiency)
        self.energy *= ((1000 - ratio)/1000)
        
        # Hope I don't break it now
        self.energy += self.genecode[2]
        self.mass += self.genecode[1]

        w = self.width * (((ratio + 1)/ 1000)**(1/2))

        self.AC = float((self.width / 4) * self.mass / exist_dif)

        self.width *= (((1001 - ratio)/1000)**(1/2))
        x_dir = choice([-1, 1])
        y_dir = choice([-1, 1])
        x = self.cx + x_dir*(self.width + w) / 4
        self.cx += - x_dir*(self.width + w) / 4
        y = self.cy + y_dir*(self.width + w) / 4
        self.cy += - y_dir*(self.width + w) / 4
        screen.coords(self.body, (self.cx - (self.width / 2))*scale, (self.cy - (self.width / 2))*scale, (self.cx + (self.width / 2))*scale, (self.cy + (self.width / 2))*scale)

        genecode = self.genecode
        mutation = randint(0,3)
        for i in range(mutation):
            genecode[randint(0, len(genecode)-1)] += randint(-20, 20)
        Organism(m, e, x, y, w, genecode)

    def grow(self, e):
        global exist_dif

        if e < 0 or self.width < 0:
            return
        self.energy -= e
        self.width += log(e+2)/((self.AC*(3/2))*log(self.width+10))
        self.AC = float((self.width / 4) * self.mass / exist_dif)
        if self.AC < 1:
            self.markedfordeath = True

        screen.coords(self.body, (self.cx - (self.width / 2)) * scale, (self.cy - (self.width / 2)) * scale, (self.cx + (self.width / 2)) * scale, (self.cy + (self.width / 2)) * scale)

    def recover(self, e):
        missingHP = 1000 - self.HP
        recovery = missingHP * self.genecode[11]/1000
        if recovery < self.energy:
            self.energy -= recovery/2
            self.HP += recovery
            if self.HP > 950:
                self.HP = 950

    # state resolution

    def exist(self):
        global exist_dif

        energy_loss = self.mass * ((self.width/2)**2) * pi * (exist_dif/(1000*1000000)) * (1000 / self.HP) * (1/self.AC)
        self.energy -= (energy_loss + self.genecomplexity/30)
        if self.energy <= 0:
            self.die()

    def move(self):
        global mvmnt_dif

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
        global exist_dif

        self.energy = e
        self.mass = m

        slope = mean(world_space_terrain[floor(y / t_chunkHEIGHT)][floor(x / t_chunkWIDTH)][0:4])
        if slope != 0:
            del self
            return

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

        self.AC = float((self.width / 4) * self.mass / exist_dif)
        self.HP = float(1000)

        self.markedfordeath = False
        self.tree_level = tree_level
        if randint(1,6) - tree_level < 0:
            self.markedfordeath = True
            del self
            return
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
        global union_dif

        chunk_fertility = world_space_fertility[self.y_chunk][self.x_chunk]
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
        global sunlight

        self.energy += sunlight - self.tree_level
        self.mass += sunlight - self.tree_level

    def die(self):
        screen.delete(self.body)
        del food_list[food_list.index(self)]
        del self

def create_food():
    global plant_per_chunk

    for i in range(max(x_chunkNUM*y_chunkNUM*plant_per_chunk-len(food_list), 1)):
        food(randint(50, 800), randint(50, 1000), randint(100, worldWIDTH - 100), randint(100, worldHEIGHT - 100), 0)

def create_initial_population(start_pop, dna_length):
    for creature in range(start_pop):
        global gene_range

        m = randint(1000, 2000)
        e = randint(1000, 2000)
        w = randint(30, 60)
        x = randint(round(w / 2) + 2*t_chunkWIDTH, worldWIDTH - round(w / 2) - 2*t_chunkWIDTH)
        y = randint(round(w / 2) + 2*t_chunkHEIGHT, worldHEIGHT - round(w / 2) - 2*t_chunkHEIGHT)

        genecode = []
        for j in range(dna_length):
            genecode.append(randint(400-min(300,gene_range), 600+min(300,gene_range)))
        Organism(m, e, x, y, w, genecode)
        organism_list[len(organism_list) - 1].early = True

    return organism_list


def fitness(elite_ratio):  # survival_ratio - how many out of a number of srvvl_dif creatures survive
    global elite_dif

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
        global mutnt_dif

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
            new_gene[randint(0, len(new_gene) - 1)] = randint(1,200)+randint(1,200)+randint(1,200)+randint(1,200)+randint(1,200)

        # Creates the organism

        m = randint(500, 1500)
        e = randint(500, 1500)
        w = organism_list[i].width
        x = randint(round(w / 2) + 2 * t_chunkWIDTH, worldWIDTH - round(w / 2) - 2 * t_chunkWIDTH)
        y = randint(round(w / 2) + 2 * t_chunkHEIGHT, worldHEIGHT - round(w / 2) - 2 * t_chunkHEIGHT)

        e = e + (organism_list[i].genecode[2])
        m = m + (organism_list[i].genecode[1])
        
        Organism(m, e, x, y, w, new_gene)
        organism_list[len(organism_list) - 1].child = True
        crossover_children.append(organism_list[len(organism_list) - 1])

    return crossover_children


def luckybreed(luck_ratio):
    global lucky_dif

    lucky = []
    luck_number = round(luck_ratio / lucky_dif * len(organism_list))
    while len(lucky) < luck_number + 1 and len(organism_list) > luck_number:
        i = randint(0, len(organism_list) - 1)
        if not organism_list[i].elite and not organism_list[i].child and not organism_list[i].lucky:
            lucky.append(organism_list[i])
            organism_list[i].lucky = True

    return lucky


def mutation(death_ratio):  # Mutates the leftovers, srvvl ratio affects how many organisms survive
    global srvvl_dif

    mutated = []
    for i in range(len(organism_list)):
        if not organism_list[i].elite and not organism_list[i].child and not organism_list[i].lucky:
            gene_mutation = organism_list[i].genecode
            for j in range(len(gene_mutation)):
                gene_mutation[j] = randint(1,200) + randint(1,200) + randint(1,200) + randint(1,200) + randint(1,200)
            organism_list[i].genecode = gene_mutation
            mutated.append(organism_list[i])
            if randint(1, srvvl_dif) < death_ratio:
                organism_list[i].markedfordeath = True
    return mutated



def generation_pass():
    global elite_ratio_constant
    global crossover_mutation_constant
    global lucky_survivor_constant
    global generation_death_constant

    new_generation = []

    create_food()

    elites = fitness(elite_ratio_constant)
    crossover_children = crossover(crossover_mutation_constant, elites)
    lucky_ones = luckybreed(lucky_survivor_constant)
    mutated = mutation(generation_death_constant)

    for i in range(len(organism_list) -1, -1, -1):
        if not organism_list[i].markedfordeath:
            new_generation.append(organism_list[i])
        else:
            organism_list[i].die()
    return new_generation

def time_pass():
    for entity in itertools.chain(organism_list, food_list):
        if not entity.markedfordeath:
            entity.brain()
            entity.motor()
        else:
            entity.die()

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
# Kohutavalt laisk ja mõttetu kood, aga on neljapäeva õhtu ja ma väga mõelda ei viitsi
def prompt():
    def constantchange():
        global worldWIDTH
        global worldHEIGHT
        global chunkWIDTH
        global chunkHEIGHT
        global t_chunkWIDTH
        global t_chunkHEIGHT
        global screenWIDTH
        global screenHEIGHT
        global birth_dif
        global exist_dif
        global accel_dif
        global mvmnt_dif
        global cnsme_dif
        global elite_ratio_constant
        global crossover_mutation_constant
        global lucky_survivor_constant
        global generation_death_constant
        global gene_range
        global sunlight
        global Aeg
        global initialpopulationnum
        global plant_per_chunk
        global lake_amount
        global wait
        worldWIDTH = round(fabs(int(Entry.get(e1))))
        worldHEIGHT = round(fabs(int(Entry.get(e2))))
        chunkWIDTH = round(fabs(int(Entry.get(e3))))
        chunkHEIGHT = round(fabs(int(Entry.get(e4))))
        t_chunkWIDTH = round(fabs(int(Entry.get(e5))))
        t_chunkHEIGHT = round(fabs(int(Entry.get(e6))))
        screenWIDTH = round(fabs(int(Entry.get(e7))))
        screenHEIGHT = round(fabs(int(Entry.get(e8))))
        birth_dif = fabs(int(Entry.get(e9)))
        exist_dif = fabs(int(Entry.get(e10)))
        accel_dif = fabs(int(Entry.get(e11)))
        mvmnt_dif = fabs(int(Entry.get(e12)))
        cnsme_dif = fabs(int(Entry.get(e13)))
        elite_ratio_constant = fabs(int(Entry.get(e14)))
        crossover_mutation_constant = fabs(int(Entry.get(e15)))
        lucky_survivor_constant = fabs(int(Entry.get(e16)))
        generation_death_constant = fabs(int(Entry.get(e17)))
        gene_range = round(fabs(int(Entry.get(e18))))
        sunlight = fabs(float(Entry.get(e19)))
        Aeg = round(fabs(int(Entry.get(e20))))
        initialpopulationnum = round(fabs(int(Entry.get(e21))))
        plant_per_chunk = round(fabs(int(Entry.get(e22))))
        lake_amount = round(fabs(int(Entry.get(e23))))
        wait = False
        prompter.destroy()

    longest_word = 40
    prompter = Tk()
    prompter.resizable(width=FALSE, height=FALSE)
    prompter.title("Evolution Simulator Setup")
    Label(prompter, text="WORLD CONSTANTS").grid(row=0, columnspan=2)
    Label(prompter, text="World Width".rjust(longest_word)).grid(row=1, column=0)
    e1 = Entry(prompter)
    e1.grid(row=1, column=1)
    e1.insert(END, '4000')
    Label(prompter, text="World Height".rjust(longest_word)).grid(row=2, column=0)
    e2 = Entry(prompter)
    e2.grid(row=2, column=1)
    e2.insert(END, '4000')
    Label(prompter, text="Chunk Width".rjust(longest_word)).grid(row=3, column=0)
    e3 = Entry(prompter)
    e3.grid(row=3, column=1)
    e3.insert(END, '100')
    Label(prompter, text="Chunk Height".rjust(longest_word)).grid(row=4, column=0)
    e4 = Entry(prompter)
    e4.grid(row=4, column=1)
    e4.insert(END, '100')
    Label(prompter, text="Terrain Chunk Width".rjust(longest_word)).grid(row=5, column=0)
    e5 = Entry(prompter)
    e5.grid(row=5, column=1)
    e5.insert(END, '50')
    Label(prompter, text="Terrain Chunk Height".rjust(longest_word)).grid(row=6, column=0)
    e6 = Entry(prompter)
    e6.grid(row=6, column=1)
    e6.insert(END, '50')
    Label(prompter, text="Screen Width".rjust(longest_word)).grid(row=7, column=0)
    e7 = Entry(prompter)
    e7.grid(row=7, column=1)
    e7.insert(END, '1000')
    Label(prompter, text="Screen Height".rjust(longest_word)).grid(row=8, column=0)
    e8 = Entry(prompter)
    e8.grid(row=8, column=1)
    e8.insert(END, '1000')
    Label(prompter, text="").grid(row=9, columnspan=2)
    Label(prompter, text="ENTITY CONSTANTS").grid(row=10, columnspan=2)
    Label(prompter, text="Birth Difficulty".rjust(longest_word)).grid(row=11, column=0)
    e9 = Entry(prompter)
    e9.grid(row=11, column=1)
    e9.insert(END, '1000')
    Label(prompter, text="Attrition".rjust(longest_word)).grid(row=12, column=0)
    e10 = Entry(prompter)
    e10.grid(row=12, column=1)
    e10.insert(END, '1000')
    Label(prompter, text="Inertia".rjust(longest_word)).grid(row=13, column=0)
    e11 = Entry(prompter)
    e11.grid(row=13, column=1)
    e11.insert(END, '1000')
    Label(prompter, text="Movement Drag".rjust(longest_word)).grid(row=14, column=0)
    e12 = Entry(prompter)
    e12.grid(row=14, column=1)
    e12.insert(END, '1000')
    Label(prompter, text="Consumption Difficulty".rjust(longest_word)).grid(row=15, column=0)
    e13 = Entry(prompter)
    e13.grid(row=15, column=1)
    e13.insert(END, '1000')
    Label(prompter, text="").grid(row=16, columnspan=2)
    Label(prompter, text="GENERATION PASS").grid(row=17, columnspan=2)
    Label(prompter, text="Elites Per Mille".rjust(longest_word)).grid(row=18, column=0)
    e14 = Entry(prompter)
    e14.grid(row=18, column=1)
    e14.insert(END, '200')
    Label(prompter, text="Crossovers Per Mille".rjust(longest_word)).grid(row=19, column=0)
    e15 = Entry(prompter)
    e15.grid(row=19, column=1)
    e15.insert(END, '200')
    Label(prompter, text="Lucky Organisms Per Mille".rjust(longest_word)).grid(row=20, column=0)
    e16 = Entry(prompter)
    e16.grid(row=20, column=1)
    e16.insert(END, '50')
    Label(prompter, text="Deaths Per Mille".rjust(longest_word)).grid(row=21, column=0)
    e17 = Entry(prompter)
    e17.grid(row=21, column=1)
    e17.insert(END, '250')
    Label(prompter, text="").grid(row=22, columnspan=2)
    Label(prompter, text="SPECIAL CONSTANTS").grid(row=23, columnspan=2)
    Label(prompter, text="Initial Gene Entropy".rjust(longest_word)).grid(row=24, column=0)
    e18 = Entry(prompter)
    e18.grid(row=24, column=1)
    e18.insert(END, '0')
    Label(prompter, text="Sunlight".rjust(longest_word)).grid(row=25, column=0)
    e19 = Entry(prompter)
    e19.grid(row=25, column=1)
    e19.insert(END, '2')
    Label(prompter, text="Generation Length".rjust(longest_word)).grid(row=26, column=0)
    e20 = Entry(prompter)
    e20.grid(row=26, column=1)
    e20.insert(END, '1000')
    Label(prompter, text="Init. Population".rjust(longest_word)).grid(row=27, column=0)
    e21 = Entry(prompter)
    e21.grid(row=27, column=1)
    e21.insert(END, '50')
    Label(prompter, text="Plants Per Chunk".rjust(longest_word)).grid(row=28, column=0)
    e22 = Entry(prompter)
    e22.grid(row=28, column=1)
    e22.insert(END, '2')
    Label(prompter, text="Lake Num".rjust(longest_word)).grid(row=29, column=0)
    e23 = Entry(prompter)
    e23.grid(row=29, column=1)
    e23.insert(END, '10')
    Label(prompter, text="").grid(row=30, columnspan=2)
    Button(prompter, text='Confirm', command=constantchange).grid(row=31, columnspan=2)
    prompter.mainloop()

prompt()
root = Tk()

root.resizable(width=FALSE, height=FALSE)
root.geometry(str(screenWIDTH)+"x"+str(screenHEIGHT))
root.title("Evolution Simulator V2")

root.bind("<Left>", leftKey)
root.bind("<Right>", rightKey)
root.bind("<Up>", upKey)
root.bind("<Down>", downKey)
root.bind("<Next>", nextKey)
root.bind("<Prior>", priorKey)
root.bind("<BackSpace>", backspaceKey)
root.bind("<Return>", returnKey)
colour_mode = 0

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

l1 = Label(status_bar, text="Population: ",textvariable=Populatsiooni_arv,width=(len("Population: ")+4),font=("arial",10))
l2 = Label(status_bar, text="Plant Count: ",textvariable=Toidu_arv,width=(len("Plant Count: ")+5),font=("arial",10))
l3 = Label(status_bar,text="Time until Generation Pass: ",textvariable=timer,width=(len("Time until Generation Pass: ")+4),font=("arial",10))
l4 = Label(status_bar,text="FPS: ",textvariable=FPS,font=("courier",10))
l1.pack(side=LEFT)
l2.pack(side=LEFT)
l3.pack(side=LEFT)
l4.pack(side=RIGHT)

# Menu, WiP but is not necessary for program to function
def hello():
    print("Option is not working yet")
def colourmodegene():
    global colour_mode
    colour_mode = 0
    messagebox.showinfo(title="Legend", message="The colour of the organism is determined by its genevalues in a given are of its DNA.\nFrom blue in the beggining to green in the middle and red in the end.\n")
def colourmodehealth():
    global colour_mode
    colour_mode = 1
    messagebox.showinfo(title="Legend", message="The green of the organism shows its healthiness.\nTougher and denser organisms are blue.\nOrganisms turn red as they age.\n")
def colourmodeenergy():
    global colour_mode
    colour_mode = 2
    messagebox.showinfo(title="Legend", message="The whiter the organism, the more energy it has.\n")
def about():
    messagebox.showinfo(title="About",message="Project: Evolution Simulator\nVersion 1.2\n")
def howto():
    messagebox.showinfo(title="How to use",message="Just look how the organism live and evolve.\nYou can choose variables from the options menu.\nUse \"Backspace\" and \"Enter\" to control gamespeed, arrowkeys to move and \"Page Up\" and \"Page down\" to zoom.")
def color_chooser():
    color = colorchooser.askcolor(title="Choose a background color")
    color_name = color[1]
    for i in range(len(chunk_list_for_menu)):
        screen.itemconfig(chunk_list_for_menu[i],fill=color_name)
def initpop():
    label12 = Label(screen,text="WiP").pack()
def generation_pass_button():
    generation_pass()
def reset_world_time():
    global Aeg
    global world_clock
    world_clock = Aeg
    
menubar = Menu(root)

options_menu = Menu(menubar,tearoff=0)
options_menu.add_command(label="Background color",command=color_chooser)
options_menu.add_command(label="New generation",command=generation_pass_button)
options_menu.add_command(label="Reset Generation Time",command=reset_world_time)
options_menu.add_command(label="Initial population WIP",command=initpop)
options_menu.add_command(label="Option 1 WIP",command=hello)
options_menu.add_command(label="Option 2 WIP",command=hello)
options_menu.add_command(label="Option 3 WIP",command=hello)
menubar.add_cascade(label="Options",menu=options_menu)

view_menu = Menu(menubar,tearoff=0)
view_menu.add_command(label="Colour Mode: Genes",command=colourmodegene)
view_menu.add_command(label="Colour Mode: Healthiness",command=colourmodehealth)
view_menu.add_command(label="Colour Mode: Energy",command=colourmodeenergy)
menubar.add_cascade(label="Set Colour Mode",menu=view_menu)

help_menu = Menu(menubar,tearoff=0)
help_menu.add_command(label="How to use",command=howto)
help_menu.add_command(label="About",command=about)
menubar.add_cascade(label="Help",menu=help_menu)

root.config(menu=menubar)

#Create Screen

screen = Canvas(root, width=worldWIDTH, height=worldHEIGHT, xscrollincrement="1", yscrollincrement="1")
screen.create_rectangle(0, 0, worldWIDTH, worldHEIGHT,width=10)

#Lake
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
chunk_list_for_menu = []
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

        if y >= y_t_chunkNUM - 2:
            a_s += -200
            a_n += -a_s

        if x <= 1:
            a_w += -200
            a_e += -a_w

        if x >= y_t_chunkNUM - 2:
            a_e += -200
            a_w += -a_e

        slope = floor(((1000-(((a_n**2 + a_s**2 + a_w**2 + a_e**2)/4)**(1/2)))/1000)*255)
       
        r_col = str(hex(slope)).replace("0x", "").rjust(2, "0")
        g_col = str(hex(slope)).replace("0x", "").rjust(2, "0")
        b_col = str(hex(slope)).replace("0x", "").rjust(2, "0")
        hex_col = "#" + r_col + g_col + b_col

        temp = world_square = screen.create_rectangle(t_chunkWIDTH * x, t_chunkHEIGHT * y, t_chunkWIDTH * (x + 1), t_chunkHEIGHT * (y + 1), outline="", fill=hex_col)

        world_space_terrain[y][x] = (a_w, a_e, a_n, a_s, vx, vy, world_square)
        chunk_list_for_menu.append(temp)
# Cool lakes
for i in range(lake_amount):
    x = randint(2,x_t_chunkNUM-3)
    y = randint(2,y_t_chunkNUM-3)
    for j in range(randint(0,4)+randint(1,6)):
        if x >= 0 and x < x_t_chunkNUM and y >= 0 and y < y_t_chunkNUM:
            world_space_terrain[y][x] = (-200, -200, -200, -200, 0, 0, world_space_terrain[y][x][6])
            screen.itemconfig(world_space_terrain[y][x][6], fill="blue")
            changer = choice([-1, 1])
            if randint(0,1) == 1:
                x += changer
            else:
                y += changer


#jõgi = screen.create_line(river(),fill="blue",width=10)

##Initialize Entities

create_food()
minimum_dna_length = 12
create_initial_population(initialpopulationnum, minimum_dna_length)

#Main Cycle
root.update()
time.sleep(1)
world_speed = 0.05
world_clock = Aeg
while True:
    start_time = time.time()

    world_clock -= 1

    update_chunks()

    Populatsiooni_arv.set("Population: "+str((len(organism_list))))
    Toidu_arv.set("Plant Count: "+str((len(food_list))))
    timer.set("Time until Generation Pass:  "+str(world_clock))
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
        end_time = time.time()
        if end_time > start_time:
            FPS.set("FPS: "+str(round(1.0/(end_time-start_time), 2)))


##Standard print mode

##create_initial_population(200,3)
##for i in range(len(organism_list)):
##    print(organism_list[i].genecode)
##new_generation = generation_pass()
##for i in range(len(new_generation)):
##    print(new_generation[i].genecode)

##root.mainloop()
