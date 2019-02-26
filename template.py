#el algoritmo tambien me dira desde donde es mejor empezar
#el problema debe ser el paso por referencia/valor
import string, math,random

def distancesFromCoords():
    f = open('kroA100.tsp')
    data = [line.replace("\n","").split(" ")[1:] for line in f.readlines()[6:106]]
    coords =  list(map(lambda x: [float(x[0]),float(x[1])], data))
    distances = []
    for i in range(len(coords)):
        row = []
        for j in range(len(coords)):
            row.append(math.sqrt((coords[i][0]-coords[j][0])**2 + (coords[i][1]-coords[j][1])**2))
        distances.append(row)
    return distances

def calculateZ(myList,distances): 
    #Recibo la lista con el orden actual, como las ciudades
    #en este caso seran enumeradas del 0 al 99 usaremos su nombre como indice para referirse a las distancias
    sum=0
    for i in range(len(myList)-1):
        fromCity=myList[i] #el numero en la posicion i. (que puede ser del 0 al 99)
        toCity=myList[i+1]
        sum=sum+distances[fromCity][toCity]

    #al final tambien se debe retornar a la inicial es decir la de la posicion 1 asi que:
    toCity=myList[0] #el numero en la posicion i. (que puede ser del 0 al 99)
    fromCity=myList[len(myList)-1]
    sum=sum+distances[fromCity][toCity]
    return sum


def evaluateChangeWithProb(temper,delta):
    ran=random.random()
    prob=math.exp(-delta/temper)
    if prob>ran:
        return True
    else:
        return False


def generateInitialSolution(nCities):
    return [i for i in range(100)]

def disturb(citiesList):
    rand1=random.randint(0,99)
    rand2=random.randint(0,99)
    temp1=citiesList[rand1]
    citiesList[rand1]=citiesList[rand2]
    citiesList[rand2]=temp1
    return citiesList


def compareSolutions(initial,possible,adjMatrix):
    zi=calculateZ(initial,adjMatrix)
    zp=calculateZ(possible,adjMatrix)

    if(zp<zi):
        return True
    else:
        return False


def PartialSimulatedAnnealing(initialSolution,adjMatrix,temper,alpha):
    initial=initialSolution
    possible=disturb(initialSolution)

    if compareSolutions(initial,possible,adjMatrix):
        temper=temper*alpha
    else:
        delta=calculateZ(possible,adjMatrix)-calculateZ(initial,adjMatrix)
        if evaluateChangeWithProb(temper,delta):
            temper=temper*alpha
        else:
            initialSolution=initial
    return temper

def SimulatedAnnealing(initialSolution,adjMatrix,initialTem,finalTemp,alpha):
    while finalTemp<initialTem:
        initialTem=PartialSimulatedAnnealing(initialSolution,adjMatrix,initialTem,alpha)
    print("the chosen path is: ",initialSolution)
    print("the final distance is: ",calculateZ(initialSolution,adjMatrix))

tempI=100
tempF=10
alpha=0.8
matrix= distancesFromCoords()
solution=generateInitialSolution(100)

SimulatedAnnealing(solution,matrix,tempI,tempF,alpha)

