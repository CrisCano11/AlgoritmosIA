
import random
import operator
from tabulate import tabulate
#from collections import defaultdict

Parameters = {}
Amount = 0
Products = []
Population = []
Incumbent = {}
InitialSolution = {}
UnimprovedIterations = 0
Iterations = 0
ListTabu=[]
ListIncumbent=[]
ActualSolution = {}
random.seed(5)
def SolucionActual():
	global InitialSolution, ActualSolution
	ActualSolution=InitialSolution

def ShowDataTabu(ArrayData):
	global Amounts
	header = {}
	for i in range(Amount):
			header[i] = "X" + str(i + 1)   
	header["z"] = "Z"
	header["b"] = "B"
	header["feasibility"] = "Factibilidad"
	header["penalized"] = "Z penalizado"
	header["listtabu_size"] = "Lista Tabú"
	header["vType1"] = "Vecino 1"
	header["vType2"] = "Vecino 2"
	header["listincumbent_size"]="Lista de incumbentes"
	if (type(ArrayData) != list):
		new = []
		new.append(ArrayData)
		ArrayData = new
	print(tabulate(ArrayData, headers=header))


def GetParametersTabu():
	global Parameters
	Parameters["basket_size"] = int(input("Ingrese el tamaño de la canasta: \n"))
	Parameters["population_size"] = int(input("Ingrese el tamaño de la población: \n"))
	Parameters["diversity"] = int(input("Ingrese el porcentaje de la diversidad: \n"))
	Parameters["iterations"] = int(input("Ingrese el número de la iteraciones: \n"))
	Parameters["unimproved_iterations"] = int(input("Ingrese el número de iteraciones sin mejorar: \n"))
	Parameters["k"] = int(input("Ingrese el porcentaje de K: \n"))
	Parameters["listincumbent_size"] = int(input("Ingrese el tamaño de la lista de incumbentes: \n"))
	Parameters["listtabu_size"] = int(input("Ingrese el tamaño de la lista tabú: \n"))
	Parameters["vType1"] = int(input("Ingrese el porcentaje del vecino tipo 1: \n"))
	GetProducts()
	SolucionActual()

def GetProducts():
	global Amount, Products, InitialSolution, Incumbent,ListTabu,ListIncumbent
	keep = 1
	while keep == 1:
			Product = {}
			Product["value"] = int(input("Ingrese el valor del producto: \n"))
			Product["size"] = int(input("Ingrese el tamaño del producto: \n"))
			Products.append(Product)
			Amount += 1
			keep = int(input("Desea agregar otro producto: \n 1. Si \n 2. No \n"))
	InitialSolution = GetAleatorySolution()
	print("Solución inicial Tabú: \n")
	ShowDataTabu(InitialSolution)
	Incumbent = InitialSolution
	print("Incumbente actual Tabú: \n")
	ShowDataTabu(Incumbent)
	#GetPopulationTabu(InitialSolution,level =1)

def rangoVecinos(Vec1):
	rango1=1*Vec1/100
	Parameters['vType2']=Vec1-100
	return rango1

def GetAleatorySolution():
	global Amount
	ArrayData = {}
	for i in range(Amount):
		ArrayData[i] = random.randint(0,1)
	return ArrayData

def listaIncumbentes(solAct):
	global ListIncumbent, Parameters
	valid=listaTabu(solAct)
	list2=[]
	if (valid==True):
		if(len(ListIncumbent)==Parameters["listincumbent_size"]):
			cambio=random.random(0,Parameters["listincumbent_size"]-1)
			list2=ListIncumbent[cambio]=solAct
		else:
			list2=ListIncumbent.append(solAct)
	list2= ListIncumbent
	return list2

def listaTabu(Person):
	global Population, ListTabu
	valid=True
	for i in range(len(Population)-1):
		if(Person!=Population[i]):					
			ListTabu.append(Person)
			valid=True			
		else:
			valid=False
	print(valid)
	return valid

def DiversityTabu():
	global Parameters,ListIncumbent
	validar=False
	lista=ListIncumbent
	if (len(lista)<= Parameters["listincumbent_size"]/2):
		validar=False
	else:
		validar=True
	return validar

def GetTypeNeightbor():
	global Parameters, ActualSolution, Incumbent, Population
	#rangoVecinos(Parameters["vType1"])
	number = random.uniform(0,1)
	if	(number<=rangoVecinos(Parameters["vType1"])):
		vecino=Vecino1(ActualSolution)
		return vecino
	else:
		vecino=Vecino2(ActualSolution)
		return vecino

def GetPopulationTabu(Person, level):
	global Parameters, Population, Incumbent, ActualSolution
	Person = {}
	if (level == 50):
		raise Exception('No fue posible hallar vecinos diferentes')
	for i in range(Parameters["population_size"]-1):
		Person=GetTypeNeightbor()
		print(Person)
		
		validar= listaTabu(Person)
		if (validar==False):
			Person = GetPopulationTabu(Person, level + 1)
		else:
			Population.append(Person)
		if (Person["penalized"] > Incumbent["penalized"]):
			Incumbent = Person
			listaIncumbentes(Person)
		listaTabu(Person)
		ActualSolution= Person
	Population = OrderPopulation(Population)
	#print("Población inicial Tabú: \n")
	#ShowDataTabu(Population)

def OrderPopulation(DataOrder):
	if(len(DataOrder)==0):
		list1=DataOrder
	else:
		DataOrder.sort(key=lambda x: x['feasibility'], reverse = True)
		list1 = sorted(DataOrder, key=operator.itemgetter("feasibility", "penalized"), reverse = True)
		return list1


def iteracion():
	global Population, Parameters, Iterations, UnimprovedIterations, Amount, Incumbent, InitialSolution, ActualSolution,ListTabu,ListIncumbent
	improveIncumbent = 0
	Iterations += 1
	ActualSolution=InitialSolution
	print("\nSolución Actual Tabú: \n")
	ShowDataTabu(ActualSolution)
	ListIncumbent=ActualSolution
	Incumbent=InitialSolution
	ListTabu=ActualSolution
	Population.append(ActualSolution)
	print("\nPoblación Tabú: \n")
	ShowDataTabu(Population)
	print("\nLista tabú: \n")
	ShowDataTabu(ListTabu)
	print("\nLista de incumbentes Tabú: \n")
	ShowDataTabu(ListIncumbent)
	if (Iterations <= Parameters["iterations"] and UnimprovedIterations < Parameters["unimproved_iterations"]):
		Diversidad=random.uniform(0,1)
		if(Diversidad<=Parameters["diversity"]):
			ValidDiv=DiversityTabu()
			if(ValidDiv==True):
				if(len(ListIncumbent)==Parameters["listincumbent_size"]):
					cambio=random.uniform(0,Parameters["listincumbent_size"]-1)
					ListIncumbent[cambio]=ActualSolution
		
		NewPopulation=GetPopulationTabu(ActualSolution, level = 1)
		ShowDataTabu(NewPopulation)
		Population.clear()
		Population.append(ActualSolution)
		currentIncumbent = Incumbent["penalized"]
		if (currentIncumbent != Incumbent["penalized"]):
					improveIncumbent = 1
		if (improveIncumbent == 1):
				UnimprovedIterations = 0
		else:
				UnimprovedIterations += 1
		print("Iteración Tabú " + str(Iterations) + ":\n")
		print("Iteraciones sin mejorar Tabú : " + str(UnimprovedIterations) + "\n")
		print("Incumbente actual Tabú: \n")
		ShowDataTabu(Incumbent)
		Population = OrderPopulation(NewPopulation)
		print("Lista Tabú: \n")
		ShowDataTabu(ListTabu)
		print("Lista de incumbentes: \n")
		ShowDataTabu(ListIncumbent)
		
	else:
		print("Final Tabú:\n")
		print("Iteraciones realizadas Tabú: " + str(Iterations - 1) + "\n")
		print("Incumbente obtenida Tabú: \n")
		ShowDataTabu(Incumbent)
		print("Población Tabú: \n")
		ShowDataTabu(Population)
		ShowDataTabu(ListTabu)
		ShowDataTabu(ListIncumbent)
		ShowDataTabu(ActualSolution)

def Vecino1(ChangePerson):
    global Amount
    #localIncumbent = GetZB(Incumbent)
    #genes = Amount * len(ChangePerson)
    GeneMutate = random.randint(1, Amount)
    #GenFather = GeneMutate // Amount2/5=2
    #position = GeneMutate % Amount3%5=2
    GeneMutate -= 1
    if (ChangePerson[GeneMutate] == 1):
        ChangePerson[GeneMutate] = 0
    else:
        ChangePerson[GeneMutate] = 1
    ChangePerson = GetZB(ChangePerson)
				
    return ChangePerson

def Vecino2(RecombinePopulation):
    global Amount
    #GenFather = random.randint(1, len(RecombinePopulation))
    Gen1 = random.randint(1, Amount)
    Gen2 = Gen1
    while Gen2 == Gen1:
        Gen2 = random.randint(1, Amount)
    #GenFather -= 1
    Gen1 -= 1
    Gen2 -= 1
    aux = RecombinePopulation[Gen1]
    RecombinePopulation[Gen1] = RecombinePopulation[Gen2]
    RecombinePopulation[Gen2] = aux
    RecombinePopulation = GetZB(RecombinePopulation)
    return RecombinePopulation

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

# Datos quemados para pruebas
Parameters = {'basket_size': 15, 'population_size': 4, 'diversity': 10, 'vType1': 40, 'iterations': 5, 'unimproved_iterations': 3, 'listincumbent_size': 3, 'k': 90,'listtabu_size':3}
Products = [{'value': 815, 'size': 5}, {'value': 1040, 'size': 7}, {'value': 1980, 'size': 4}, {'value': 1520, 'size': 8}, {'value': 3570, 'size': 6}, {'value': 2100, 'size': 3}]
Amount = 6
InitialSolution = {0: 1, 1: 1, 2: 0, 3: 0, 4: 0, 5: 1, 'z': 3955, 'b': 15, 'feasibility': 'SI', 'penalized': 3955}

Incumbent = {0: 1, 1: 1, 2: 0, 3: 0, 4: 0, 5: 1, 'z': 3955, 'b': 15, 'feasibility': 'SI', 'penalized': 3955}
ListTabu={0: 1, 1: 1, 2: 0, 3: 0, 4: 0, 5: 1, 'z': 3955, 'b': 15, 'feasibility': 'SI', 'penalized': 3955}
ListIncumbent = {0: 1, 1: 1, 2: 0, 3: 0, 4: 0, 5: 1, 'z': 3955, 'b': 15, 'feasibility': 'SI', 'penalized': 3955}

iteracion()
			
	
	
	

	