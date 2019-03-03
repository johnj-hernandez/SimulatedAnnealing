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
    #print("delta",delta)
    if prob>ran:
       # print("True",prob,ran)
        return True
    else:
        #print("False",prob,ran)
        return False


def generateInitialSolution(nCities):
    list1=[i for i in range(100)]
    list2=[]
    while len(list1)>0:
        rand1=random.randint(0,len(list1)-1)
        list2.append(list1.pop(rand1))
    return list2

def disturb(citiesList):
    disturb=citiesList[:]
    rand1=random.randint(0,99)
    rand2=random.randint(0,99)
    temp1=disturb[rand1]
    disturb[rand1]=disturb[rand2]
    disturb[rand2]=temp1
    return disturb

def PartialSimulatedAnnealing(initialSolution,adjMatrix,temper,alpha):
    initial=initialSolution
    possible=disturb(initialSolution)
    zi=calculateZ(initial,adjMatrix)
    zp=calculateZ(possible,adjMatrix)
    if zp<zi:
        temper=temper*alpha
        initial=possible[:]
    else:
        delta=zp-zi
        if evaluateChangeWithProb(temper,delta):
            temper=temper*alpha
            initial=possible[:]
    return initial,temper

def SimulatedAnnealing(initialSolution,adjMatrix,initialTem,finalTemp,alpha):
    iteraciones=0
    while finalTemp<initialTem:
        initialSolution,initialTem=PartialSimulatedAnnealing(initialSolution,adjMatrix,initialTem,alpha)
        iteraciones+=1
    print("Number of Iterations: ",iteraciones)
    initialSolution.append(initialSolution[0])
    print("the chosen path is: ",initialSolution)
    print("the final distance is: ",calculateZ(initialSolution,adjMatrix))

def printInitial(initial,distances):
    i=initial[:]
    i.append(initial[0])
    print("Initial Solution: ",i)
    print("Initial Distance: ",calculateZ(initial,distances))

tempI=10000
tempF=1
alpha=0.9999
matrix= distancesFromCoords()
solution=generateInitialSolution(100)
printInitial(solution,matrix)
SimulatedAnnealing(solution,matrix,tempI,tempF,alpha)

