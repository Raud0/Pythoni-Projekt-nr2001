from random import randint

def esialgne_populatsioon(suurus,muutuja):
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
    for i in range(len(populatsioon)):
        x = populatsioon[i][0]
        y = populatsioon[i][1]
        z = populatsioon[i][2]
        fitness_rating = (2*x+1)**2 + (3*y+4)**2 + (z-2)**2
        skoor.append(fitness_rating)
    for i in range(edasi):
        temp = max(skoor)
        parimskoor.append(temp)
        skoor.remove(temp)
        
    for i in range(len(populatsioon)):
        x = populatsioon[i][0]
        y = populatsioon[i][1]
        z = populatsioon[i][2]
        fitness_rating = (2*x+1)**2 + (3*y+4)**2 + (z-2)**2
        for el in range(len(parimskoor)):
            if fitness_rating == parimskoor[el]:
                parimad.append(populatsioon[i])
        
        
    return parimad

print(fitness(esialgne_populatsioon(20,3),3))
    
    


    