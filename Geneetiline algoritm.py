from random import randint

def esialgne_populatsioon(suurus,muutuja): # Loob esialge populatsiooni maatriksi
    alg_populatsioon = []
    for i in range(suurus):
        alg_populatsioon.append([randint(0,200)])
        for x in range(muutuja-1):
            alg_populatsioon[i].append(randint(0,200))
    return alg_populatsioon


def fitness(populatsioon,edasi): # edasi - Mitu parimad viiakse üle järgmisesse generatsiooni
    parimskoor = []
    skoor = []
    parimad = []
    for i in range(len(populatsioon)): # Arvutab skoori ja leiab seal parimad
        x = populatsioon[i][0]
        y = populatsioon[i][1]
        z = populatsioon[i][2]
        fitness_rating = (2*x+1)**2 + (3*y+4)**2 + (z-2)**2
        skoor.append(fitness_rating)
    for i in range(edasi):
        temp = max(skoor)
        parimskoor.append(temp)
        skoor.remove(temp)
        
    for i in range(len(populatsioon)): # Leiab, millistel vektoritel olid parimad tulemued ja lisab listi parimad
        x = populatsioon[i][0]
        y = populatsioon[i][1]
        z = populatsioon[i][2]
        fitness_rating = (2*x+1)**2 + (3*y+4)**2 + (z-2)**2
        for el in range(len(parimskoor)):
            if fitness_rating == parimskoor[el]:
                parimad.append(populatsioon[i])
                
        
        
    return parimad

def crossover(parimad): # Loob nõ lapsed, võttes kahelt vektrilt 2 suvalist arvu ja loob 3. suvalise arvu
    crossover_children = [[],[],[],[]]
    for i in range(len(parimad)): # Võtab 2 suvaliselt arvu vanematelt
        for j in range(len(parimad[0])-1):
            gene = parimad[randint(0,3)][randint(0,2)]
            crossover_children[i].append(gene)
    for i in range(len(parimad)): # Lisab suvalise arvu
        crossover_children[i].append(randint(0,200))
    return crossover_children

def lucky(populatsioon):
    lucky = []
    for i in range(20):
        if populatsioon[i] != parimad[0] and populatsioon[i] != parimad[1] and populatsioon[i] != parimad[2] and populatsioon[i] != parimad[3]:
            lucky.append(populatsioon[i])
            if len(lucky) == 4:
                break
    return lucky
    
def mutation(algpopulatsioon,parimad,lucky): # Võtab ülejäänud algpopulatsioonist ja muudab nende elemente suvaliselt
    mutation_children = []
    mutation_canditates = algpopulatsioon[:]
    while len(mutation_children) != 8:
        for i in range(1):
            if mutation_canditates[i] in parimad or mutation_canditates[i] in lucky:
                mutation_canditates.remove(mutation_canditates[i])
            else:
                mutation_children.append(mutation_canditates[i])
                mutation_canditates.remove(mutation_canditates[i])
                
    for i in range(len(mutation_children)):
        # WIP Muuda suvaline hulk arve suvalisteks aruvudeks
        
    return mutation_children
    
    
    

def next_gen():
    None
    new_generation = []
    
# Print
algpopulatsioon = esialgne_populatsioon(20,3)
parimad = fitness(algpopulatsioon,4) # Eliit
crossover = crossover(parimad) # Eliidi lapsed
lucky = lucky(algpopulatsioon)# Algpopulatsioonist need, kes ellu jäävad
uus_generatsioon = None
print("Algpopulatsioon: ",algpopulatsioon,"\n")
print("Parimad:",parimad)
print("Crossover childern: ",crossover)
print("Lucky ones: ",lucky,"\n")

print("Muteertitud",mutation(algpopulatsioon,parimad,crossover))

    