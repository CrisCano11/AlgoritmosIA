import random
import operator
from tabulate import tabulate


Parameters = {}
Amount = 0
Products = []
Population = []
Incumbent = {}
InitialSolution = {}
UnimprovedIterations = 0
Iterations = 0


random.seed(7)


def GetParameters():
	global Parameters
	Parameters["basket_size"] = int(input("Ingrese el tamaño de la canasta: \n"))
	Parameters["population_size"] = int(input("Ingrese el tamaño de la población: \n"))
	Parameters["diversity"] = int(input("Ingrese el tamaño de la diversidad: \n"))
	Parameters["recombination"] = int(input("Ingrese el porcentaje de la recombinación: \n"))
	Parameters["mutation"] = int(input("Ingrese el porcentaje de la mutación: \n"))
	Parameters["iterations"] = int(input("Ingrese el número de la iteraciones: \n"))
	Parameters["unimproved_iterations"] = int(input("Ingrese el número de iteraciones sin mejorar: \n"))
	Parameters["sons"] = int(input("Ingrese el número de hijos: \n"))
	Parameters["k"] = int(input("Ingrese el porcentaje de K: \n"))

	
	GetProducts()


def GetProducts():
    global Amount, Products, InitialSolution, Incumbent

    
    keep = 1
    
    while keep == 1:
        Product = {}
        Product["value"] = int(input("Ingrese el valor del producto: \n"))
        Product["size"] = int(input("Ingrese el tamaño del producto: \n"))
        Products.append(Product)
        Amount += 1
        
        keep = int(input("Desea agregar otro producto: \n 1. Si \n 2. No \n"))

    
    InitialSolution = GetAleatorySolution()

    
    print("Solución inicial: \n")
    ShowData(InitialSolution)

    
    Incumbent = InitialSolution

    
    print("Incumbente actual: \n")
    ShowData(Incumbent)

    
    GetPopulation()


def GetAleatorySolution(level = 1):
    global Amount

    if (level == 50):
        raise Exception('No es posible hallar toda la población cumpliendo diversidad')
    
    ArrayData = {}
    for i in range(Amount):
        ArrayData[i] = random.randint(0,1)

    if (validateDiversity(ArrayData)):
        ArrayData = GetZB(ArrayData)
    else:
        ArrayData = GetAleatorySolution(level + 1)

    
    return ArrayData


def validateDiversity(currentSolution):
    global Population, Amount, Parameters, Incumbent
    
    valid = True
    
    currentDiversity = 0

    
    if (len(Incumbent) > 0):
        
        for i in range(Amount):
            
            if (currentSolution[i] != Incumbent[i]):
                currentDiversity += 1

        
        if (currentDiversity < Parameters["diversity"]):
            
            valid = False

    
    if (valid == True):
        
        for i in range(len(Population)):
            
            currentDiversity = 0
            
            for j in range(Amount):
                
                if (currentSolution[i] != Population[i][j]):
                    currentDiversity += 1
            
            
            if (currentDiversity < Parameters["diversity"]):
                valid = False
                break


    return valid


def GetZB(ArraySolution):
    global Products, Amount, Parameters
    
    sumZ = 0
    sumB = 0
    
    for i in range(Amount):
        if (ArraySolution[i] == 1):
            sumZ += Products[i]['value']
            sumB += Products[i]['size']

    ArraySolution["z"] = sumZ
    ArraySolution["b"] = sumB

    if (sumB <= Parameters["basket_size"]):
        ArraySolution["feasibility"] = "SI"
    else:
        ArraySolution["feasibility"] = "NO"

    if (ArraySolution["feasibility"] == "SI"):
        ArraySolution["penalized"] = ArraySolution["z"]
    else:
        ArraySolution["penalized"] = ArraySolution["z"] / (ArraySolution["b"] - Parameters["basket_size"] + 5)

    return ArraySolution


def ShowData(ArrayData):
    global Amount
    
    header = {}
    
    for i in range(Amount):
        header[i] = "X" + str(i + 1)

       
    header["z"] = "Z"
    header["b"] = "B"
    header["feasibility"] = "Factibilidad"
    header["penalized"] = "Z penalizado"
    header["z_k"] = "Z penalizado - k"
    header["initial_range"] = "Rango Inicial"
    header["end_range"] = "Rango Final"

    
    if (type(ArrayData) != list):
        new = []
        new.append(ArrayData)
        ArrayData = new

    
    print(tabulate(ArrayData, headers=header))


def GetPopulation():
    global Parameters, Population, Incumbent
    Person = {}
    for i in range(Parameters["population_size"]):
        Person = GetAleatorySolution()
        Population.append(Person)

        if (Person["penalized"] > Incumbent["penalized"]):
            Incumbent = Person

    Population = OrderPopulation(Population)

    
    print("Población inicial: \n")
    ShowData(Population)

    
    RangeCalculate()

def OrderPopulation(DataOrder):
    DataOrder.sort(key=lambda x: x['feasibility'], reverse = True)
    list1 = sorted(DataOrder, key=operator.itemgetter("feasibility", "penalized"), reverse = True)
    return list1

def RangeCalculate():
    global Population, Parameters
    K = Population[-1]["penalized"] * (Parameters["k"] / 100)
    sumZK = 0
    for i in range(len(Population)):
        Population[i]["z_k"] = Population[i]["z"] - K
        sumZK += Population[i]["z_k"]

    for i in range(len(Population)):
        if (i == 0):
            Population[i]["initial_range"] = 0.0000
            Population[i]["end_range"] = Population[i]["z_k"] / sumZK
        else:
            Population[i]["initial_range"] = Population[i - 1]["end_range"] + 0.0001
            if (i == (len(Population) - 1)):
                Population[i]["end_range"] = 0.9999
            else:
                Population[i]["end_range"] = Population[i - 1]["end_range"] + (Population[i]["z_k"] / sumZK)

    print("Población: \n")
    ShowData(Population)
    iterate()

def iterate():
	global Population, Parameters, Iterations, UnimprovedIterations, Amount, Incumbent, InitialSolution
	improveIncumbent = 0
	Iterations += 1

	NewPopulation = OrderPopulation(Population)

	
	if (Iterations <= Parameters["iterations"] and UnimprovedIterations < Parameters["unimproved_iterations"]):
			for i in range(Parameters["sons"]):
					Son = GetSon()
					GetIn = 0
					if (validateDiversity(Son)):
							GetIn = 1

					if (Son["penalized"] > Incumbent["penalized"]):
							Incumbent = Son
							GetIn = 1
							improveIncumbent = 1

					if (GetIn == 1):
							if (Son["penalized"] > NewPopulation[-1]["penalized"]):
									NewPopulation[-1] = Son

					NewPopulation = OrderPopulation(NewPopulation)

					

			currentIncumbent = Incumbent["penalized"]
			NewPopulation = mutate(NewPopulation)
			NewPopulation = recombine(NewPopulation)
			
			print("\nPoblación después de Recombinar y Mutar: \n")
			ShowData(NewPopulation)
			
			if (currentIncumbent != Incumbent["penalized"]):
					improveIncumbent = 1

			if (improveIncumbent == 1):
					UnimprovedIterations = 0
			else:
					UnimprovedIterations += 1

			print("Iteración " + str(Iterations) + ":\n")
			print("Iteraciones sin mejorar: " + str(UnimprovedIterations) + "\n")
			print("Incumbente actual: \n")
			ShowData(Incumbent)

			Population = OrderPopulation(NewPopulation)
			RangeCalculate()
			
	else:
			print("Final:\n")
			print("Iteraciones realizadas: " + str(Iterations - 1) + "\n")
			print("Incumbente obtenida: \n")
			ShowData(Incumbent)
			print("Población: \n")
			ShowData(Population)

def GetSon():
    global Parameters, Amount, Population
    FatherOne = GetFatherOne()
    FatherTwo = GetFatherTwo(FatherOne)
    crossing = random.randint(Parameters["diversity"] + 1, Amount - Parameters["diversity"])
    Son = {}
    for i in range(crossing):
        Son[i] = Population[FatherOne][i]
    for i in range(crossing, Amount):
        Son[i] = Population[FatherTwo][i]

    Son = GetZB(Son)

    return Son

def GetFatherOne():
    global Population
    number = random.random()
    Father = 0

    for i in range(len(Population)):
        if (number >= Population[i]["initial_range"] and number <= Population[i]["end_range"]):
            Father = i
            break

    return Father

def GetFatherTwo(FatherOne, level = 1):
    global Population
    number = random.random()
    Father = 0

    if (level == 50):
        raise Exception('No fue posible hallar dos padres diferentes')

    for i in range(len(Population)):
        if (number >= Population[i]["initial_range"] and number <= Population[i]["end_range"]):
            Father = i
            break
    
    if (Father == FatherOne):
        Father = GetFatherTwo(FatherOne, level + 1)

    return Father

def mutate(MutatePopulation):
    global Amount, Incumbent
    localIncumbent = GetZB(Incumbent)
    genes = Amount * len(MutatePopulation)
    GeneMutate = random.randint(1, genes)
    GenFather = GeneMutate // Amount
    position = GeneMutate % Amount
    if (position == 0):
        position = Amount
        GenFather -= 1

    position -= 1

    if (MutatePopulation[GenFather][position] == 1):
        MutatePopulation[GenFather][position] = 0
    else:
        MutatePopulation[GenFather][position] = 1
    
    MutatePopulation[GenFather] = GetZB(MutatePopulation[GenFather])
    print("Nuevos datos")
    print(localIncumbent)
    print(MutatePopulation[GenFather])
    print(Incumbent)
    if (MutatePopulation[GenFather]["penalized"] > Incumbent["penalized"]):
        Incumbent = MutatePopulation[GenFather]

    return MutatePopulation

def recombine(RecombinePopulation):
    global Amount, Incumbent

    GenFather = random.randint(1, len(RecombinePopulation))
    Gen1 = random.randint(1, Amount)
    Gen2 = Gen1
    while Gen2 == Gen1:
        Gen2 = random.randint(1, Amount)

    GenFather -= 1
    Gen1 -= 1
    Gen2 -= 1

    assistant = RecombinePopulation[GenFather][Gen1]
    RecombinePopulation[GenFather][Gen1] = RecombinePopulation[GenFather][Gen2]
    RecombinePopulation[GenFather][Gen2] = assistant

    RecombinePopulation[GenFather] = GetZB(RecombinePopulation[GenFather])

    if (RecombinePopulation[GenFather]["penalized"] > Incumbent["penalized"]):
        Incumbent = RecombinePopulation[GenFather]

    return RecombinePopulation

# Datos quemados para pruebas
Parameters = {'basket_size': 15, 'population_size': 4, 'diversity': 2, 'recombination': 10, 'mutation': 2, 'iterations': 5, 'unimproved_iterations': 3, 'sons': 4, 'k': 90}
Products = [{'value': 815, 'size': 5}, {'value': 1040, 'size': 7}, {'value': 1980, 'size': 4}, {'value': 1520, 'size': 8}, {'value': 3570, 'size': 6}, {'value': 2100, 'size': 3}]
Amount = 6
InitialSolution = {0: 1, 1: 1, 2: 0, 3: 0, 4: 0, 5: 1, 'z': 3955, 'b': 15, 'feasibility': 'SI', 'penalized': 3955}

Incumbent = {0: 1, 1: 1, 2: 0, 3: 0, 4: 0, 5: 1, 'z': 3955, 'b': 15, 'feasibility': 'SI', 'penalized': 3955}

Population = [{0: 0, 1: 1, 2: 1, 3: 1, 4: 0, 5: 0, 'z': 2564, 'b': 13, 'feasibility': 'SI', 'penalized': 2564, 'z_k': 2253.0666666666666, 'initial_range': 0.0, 'end_range': 0.23463904355915965}, {0: 0, 1: 0, 2: 0, 3: 0, 4: 1, 5: 0, 'z': 2100, 'b': 7, 'feasibility': 'SI', 'penalized': 2100, 'z_k': 1789.0666666666666, 'initial_range': 0.23473904355915964, 'end_range': 0.4209561631281503}, {0: 0, 1: 1, 2: 0, 3: 1, 4: 1, 5: 0, 'z': 3850, 'b': 17, 'feasibility': 'NO', 'penalized': 481.25, 'z_k': 3539.0666666666666, 'initial_range': 0.4210561631281503, 'end_range': 0.7895219184359249}, {0: 1, 1: 1, 2: 0, 3: 1, 4: 0, 5: 1, 'z': 2332, 'b': 15, 'feasibility': 'NO', 'penalized': 388.6666666666667, 'z_k': 2021.0666666666666, 'initial_range': 0.7896219184359249, 'end_range': 0.9999}]

iterate()