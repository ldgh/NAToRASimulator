import random as rd
import pandas as pd
import sys

class city:
    def __init__(self, numberOfGeneration):
        self.generations = {}
        self.familyList = {}
        self.famID = 0
        self.numberOfGeneration = numberOfGeneration

        for gen in range(numberOfGeneration):
            self.generations[gen] = {}

    def changeParentsToGetStep(self, generation):
        keys = self.generations[generation].keys()
        first = min(keys)
        last = max(keys)

        random = rd.randint(0, 1)
        toChange = "m"
        if random == 1:
            toChange = "f"

        family1 = rd.randint(first, last)

        while len(self.generations[generation][family1].children) == 0:
            family1 = rd.randint(first, last)

        indToChange1 = self.generations[generation][family1].father
        if toChange == "m":
            indToChange1 = self.generations[generation][family1].mother

        family2 = family1
        while(family1 == family2):
            family2 = rd.randint(first, last)

            indToChange2 = self.generations[generation][family2].mother
            if toChange == "m":
                indToChange2 = self.generations[generation][family2].father
                if(self.areSiblings(indToChange1, indToChange2, generation)):
                    family2 = family1
                else:
                    if len(self.generations[generation][family2].children) == 0:
                        family2 = family1
        #print(f"I found two individuals non related to create step brothers: {indToChange1} and {indToChange2}")

        if(toChange == "m"):
            removed = self.generations[generation][family2].changeMother(indToChange1)
        else:
            removed = self.generations[generation][family2].changeFather(indToChange1)

        return (len(self.generations[generation][family2].children)+len(self.generations[generation][family1].children))


    def changeParent(self, ind, generation, role):
        oldFamily = -1

        keys = self.generations[generation].keys()
        first = min(keys)
        last = max(keys)

        for family in self.generations[generation]:
            mother, father = self.generations[generation][family].getParents()

            #======================#
            toCompare = mother
            if(role == "f"):
                toCompare = father

            # ======================#
            if toCompare == ind:
                oldFamily = family

        #print(f"My old family is {oldFamily}")
        toChange = oldFamily
        while (toChange == oldFamily):
            toChange = rd.randint(first, last)

        #print(f"Changing the {ind} from family {oldFamily} to {toChange}")
        if(oldFamily == -1):
            getchar()
        if(role == "f"):
            toChangeInd = self.generations[generation][toChange].changeFather(ind)
            toChangeInd = self.generations[generation][oldFamily].changeFather(toChangeInd)
        if (role == "m"):
            toChangeInd = self.generations[generation][toChange].changeMother(ind)
            toChangeInd = self.generations[generation][oldFamily].changeMother(toChangeInd)

        #print(f"=================== Saindo ({generation}) ======================")

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



    def areSiblings(self, ind1, ind2, generation):
        for family in self.generations[generation]:
            if self.generations[generation][family].areSiblings(ind1, ind2):
                return True
        return False

    def getParents(self, generation):
        mothersList = []
        fathersList = []

        for family in self.generations[generation]:
            mother, father = self.generations[generation][family].getParents()
            mothersList.append(mother)
            fathersList.append(father)

        return mothersList, fathersList

class family:
    def __init__(self, father, mother):
        #print(f"Creating a family with {father} and {mother}")
        self.father = father
        self.mother = mother
        self.children = []

    def changeFather(self, ind):
        toReturn = self.father
        self.father = ind
        return toReturn

    def changeMother(self, ind):
        toReturn = self.mother
        self.mother = ind
        return toReturn


    def addChildToFamily(self, child):
        self.children.append(child)

    def printFamily(self):
        print(f"\t\tMother : {self.mother} \t Father : {self.father}")
        print("\t\t\t", end="")
        for child in self.children:
            print(f"{child} ", end= "")
        print("\n*********************************")

    def getParents(self):
        return self.mother, self.father

    def areSiblings(self, ind1, ind2):
        if ind1 in self.children and ind2 in self.children:
            return True
        return False

def mergeGenealogies(inputFile, myCity):
    numberOfTries = 50
    for generation in range(len(myCity.generations)-1):
        actual = generation
        next = generation+1
        previous = generation - 1

        motherList, fatherList = myCity.getParents(next)

        siblings = True
        while siblings and numberOfTries > 0:
            siblings = False
            for i in range(len(motherList)):
                if(myCity.areSiblings(motherList[i], fatherList[i], actual)):
                    siblings = True
                    random = rd.randint(0,1)
                    if random == 1:
                        myCity.changeParent(fatherList[i], next, "f")
                    else:
                        myCity.changeParent(motherList[i], next, "m")
            numberOfTries = numberOfTries - 1

        if numberOfTries <= 0:
            return True

        #Now, step brothers
        if generation != 0:
            numberOfStep = inputFile[generation]['step'] * (inputFile[generation]['male']+inputFile[generation]['female'])
            if int(numberOfStep) > 0:
                stepBrothers = 0
                while stepBrothers < numberOfStep:
                    created = myCity.changeParentsToGetStep(previous)
                    stepBrothers = stepBrothers + created
        numberOfTries = 50



    return False



def getchar():
    c = sys.stdin.read(1)

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
    #print(f"{len(childrenList)}*{unrelatedProportion}")
    #print(f"We will have {numberOfUnrelated} unrelateds")

    for unrelated in range(numberOfUnrelated):
        unrelatedIndex = rd.randint(0,len(childrenList)-1)
        removed = childrenList.pop(unrelatedIndex)
        #print(f"The {removed} will be unrelated")

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

    #myCity.printCity()
    return myCity, individuals
#input
#men #woman %unrelated %step

inputFile={}
inputFile[0]={}
inputFile[0]['male']=2
inputFile[0]['female']=2
inputFile[0]['unrelated']=0
inputFile[0]['step']=0

inputFile[1]={}
inputFile[1]['male']=5
inputFile[1]['female']=5
inputFile[1]['unrelated']=0.4
inputFile[1]['step']=0.1

inputFile[2]={}
inputFile[2]['male']=5
inputFile[2]['female']=5
inputFile[2]['unrelated']=0.5
inputFile[2]['step']=0

loop = True
numberOfTries = 0

while loop and numberOfTries < 50:
    loop = False
    print(f"Creating city ({numberOfTries})")
    myCity = city(3)
    print(f"Creating the sub-genealogies ({numberOfTries})")
    myCity, individuals = createSubGenealogies(inputFile, myCity)
    print(f"Merging the sub-genealogies ({numberOfTries})")
    loop = mergeGenealogies(inputFile, myCity)

    if(loop):
        numberOfTries = numberOfTries + 1

if numberOfTries == 50:
    print("I tried 50 times to get a valid genealogy. It was not possible, please change your input file and try again")
else:
    print(f"Sai do loop com {numberOfTries} tentativas")
    myCity.printCity()