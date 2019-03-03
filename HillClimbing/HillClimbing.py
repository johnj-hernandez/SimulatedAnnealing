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
    #print("listaINICIAL",citiesList)
    #print("PERTURBADA",disturb)
    return disturb

def partialHillClimbing(initialSolution,adjMatrix):
    #para adaptarlo al problema haremos que compare con 5 posibles soluciones
    #para evaluar si se actualiza o no la solucion
    initial=initialSolution
    zi=calculateZ(initial,adjMatrix)
    improvement=False
    count=int(len(initialSolution)) #se comparara con n posibles soluciones
    #siendo n igual al tamaño del vector de ciudades, en este caso 100.
    while count>0:
        possible=disturb(initialSolution)
        zp=calculateZ(possible,adjMatrix)
        if zp<=zi:
            initial=possible[:]
            improvement=True
            count=0
        else:
            improvement=False
            count=count-1

    return initial,improvement


def hillClimbing(initialSolution,adjMatrix):
    iteraciones=0
    improvement=True
    while improvement:
        initialSolution,improvement=partialHillClimbing(initialSolution,adjMatrix)
        iteraciones+=1
    print("Number of iterations: ",iteraciones)
    initialSolution.append(initialSolution[0])
    print("the chosen path is: ",initialSolution)
    print("the final distance is: ",calculateZ(initialSolution,adjMatrix))

def printInitial(initial,distances):
    i=initial[:]
    i.append(initial[0])
    print("Initial Solution: ",i)
    print("Initial Distance: ",calculateZ(initial,distances))

matrix= distancesFromCoords()
solution=generateInitialSolution(100)
printInitial(solution,matrix)
hillClimbing(solution,matrix)

