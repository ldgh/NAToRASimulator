import random as rd
import pandas as pd

class city:
    def __init__(self, numberOfGeneration):
        self.generations = {}
        self.familyList = {}
        self.famID = 0

        for gen in range(numberOfGeneration):
            self.generations[gen] = {}

    def getFamiliesForGeneration(self, generation):
        return list(self.generations[generation].keys())

    def addFamily(self, male, female, generation):
        id = self.famID
        self.famID = self.famID + 1
        self.generations[generation][id] = family(male, female)

        self.familyList[id] = generation

    def setChildToFamily(self, generation, famID, child):
        self.generations[generation][famID].addChildToFamily(child)

    def printCity(self):
        for gen in range(len(self.generations)):
            print(f" =========================== Generation {gen} ==========================")
            for id in self.generations[gen]:
                print(f"\tFamily {id}: ")
                self.generations[gen][id].printFamily()


class family:
    def __init__(self, father, mother):
        print(f"Creating a family with {father} and {mother}")
        self.father = father
        self.mother = mother
        self.children = []

    def addChildToFamily(self, child):
        self.children.append(child)

    def printFamily(self):
        print(f"\t\tMother : {self.mother} \t Father : {self.father}")
        print("\t\t\t", end="")
        for child in self.children:
            print(f"{child} ", end= "")
        print("\n*********************************")

def mergeGenealogies(inputFile, myCity, mergedCity):



def createCouples(myCity, maleList, femaleList, generation):
    maxCouple = min(len(maleList), len(femaleList))

    for couple in range(maxCouple):
        maleIndex = rd.randint(0, len(maleList)-1)
        femaleIndex = rd.randint(0, len(femaleList)-1)

        male = maleList.pop(maleIndex)
        female = femaleList.pop(femaleIndex)

        myCity.addFamily(male, female, generation)

    return myCity

def giveChildrenToCouples(myCity, childrenList, unrelatedProportion, generation):
    numberOfUnrelated = int(len(childrenList)*unrelatedProportion)
    print(f"{len(childrenList)}*{unrelatedProportion}")
    print(f"We will have {numberOfUnrelated} unrelateds")

    for unrelated in range(numberOfUnrelated):
        unrelatedIndex = rd.randint(0,len(childrenList)-1)
        removed = childrenList.pop(unrelatedIndex)
        print(f"The {removed} will be unrelated")

    families = myCity.getFamiliesForGeneration(generation)
    for child in childrenList:
        familyIndex = unrelatedIndex = rd.randint(0,len(families)-1)
        myCity.setChildToFamily(generation, families[familyIndex], child)

    return(myCity)

def getList (individuals, type, generation):
    if type != "all":
        toReturn = individuals.query(f"Sex == {type} and Generation == {generation}")["ID"].to_list()
    else:
        toReturn = individuals.query(f"Generation == {generation}")["ID"].to_list()
    return toReturn

def createSubGenealogies(inputFile, myCity):
    individuals = pd.DataFrame(columns=['ID', 'Sex', 'Generation'])
    id = 0

    for generation in range(0,len(inputFile)):
        maleList = []
        femaleList =[]
        for ind in range(0, inputFile[generation]['male']):
            temp = pd.DataFrame([[id, 1, generation]], columns=['ID', 'Sex', 'Generation'])
            individuals = pd.concat([individuals, temp])
            id = id+1
        for ind in range(0, inputFile[generation]['female']):
            temp = pd.DataFrame([[id, 2, generation]], columns=['ID', 'Sex', 'Generation'])
            individuals = pd.concat([individuals, temp])
            id = id+1

    for generation in range(0, len(inputFile) - 1):
        maleList = getList(individuals, 1, generation)
        femaleList = getList(individuals, 2, generation)
        childrenList = getList(individuals, 'all', generation+1)
        myCity = createCouples(myCity, maleList, femaleList, generation)
        myCity = giveChildrenToCouples(myCity, childrenList, inputFile[generation+1]['unrelated'], generation)

    myCity.printCity()
    return myCity, individuals
#input
#men #woman %unrelated %step

inputFile={}
inputFile[0]={}
inputFile[0]['male']=2
inputFile[0]['female']=3
inputFile[0]['unrelated']=0
inputFile[0]['step']=0

inputFile[1]={}
inputFile[1]['male']=5
inputFile[1]['female']=5
inputFile[1]['unrelated']=0.1
inputFile[1]['step']=0.1

inputFile[2]={}
inputFile[2]['male']=5
inputFile[2]['female']=5
inputFile[2]['unrelated']=0.5
inputFile[2]['step']=0

myCity = city(3)
mergedCity = city(3)
myCity, individuals = createSubGenealogies(inputFile, myCity)
myCity = mergeGenealogies(inputFile, myCity)