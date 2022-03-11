#Algortimo geneticos

#Librerias
import random
import operator
from tabulate import tabulate

#Definición de variables
Parameters = {}
Amount = 0
Products = []
Population = []
Incumbent = {}
InitialSolution = {}
UnimprovedIterations = 0
Iterations = 0

# Sembrar semilla python
random.seed(7)

# Funcion donde solicitamos y llenamos todos los parametros iniciales
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

    # Llamado para obtener los productos
    GetProducts()

# Función para obtener los productos dinamicamente hasta que el usuario no quiera ingresar más
def GetProducts():
    global Amount, Products, InitialSolution, Incumbent

    # Se define la variable para que entre al ciclo por primera vez para llenar como minimo un producto
    keep = 1
    # Ciclo para llenar los productos según la necesidad del usuario
    while keep == 1:
        Product = {}
        Product["value"] = int(input("Ingrese el valor del producto: \n"))
        Product["size"] = int(input("Ingrese el tamaño del producto: \n"))
        Products.append(Product)
        Amount += 1
        # Cada que se ingresa un producto el usuario puede elegir ingresar otro o salir
        keep = int(input("Desea agregar otro producto: \n 1. Si \n 2. No \n"))

    # Obtenemos la solución inicial
    InitialSolution = GetAleatorySolution()

    # Mostramos la población inicial obtenida
    print("Solución inicial: \n")
    ShowData(InitialSolution)

    # Al no tener más opciones la solución inicial se guarda como incumbente
    Incumbent = InitialSolution

    # Mostramos la incumbente actual
    print("Incumbente actual: \n")
    ShowData(Incumbent)

    # Obtenemos la población inicial
    GetPopulation()

# Funcion para generar una solución aleatoria
def GetAleatorySolution(level = 1):
    global Amount

    # Si se llega a 50 repeticiones sin obtener una solución que cumpla diversidad se para la ejecución del script para evitar ciclo infinito
    if (level == 50):
        raise Exception('No es posible hallar toda la población cumpliendo diversidad')
    
    # Arreglo temporal para guardar los datos aleatorios
    ArrayData = {}
    # Se generan un aleatorio para cada producto, entre 0 y 1 para saber si se lleva el producto o no
    for i in range(Amount):
        ArrayData[i] = random.randint(0,1)

    # Validamos si la solución aleatoria encontrada cumple la diversidad
    if (validateDiversity(ArrayData)):
        # En caso de cumplir diversidad se calculan las columnas de la solución
        ArrayData = GetZB(ArrayData)
    else:
        # En caso de no cumplir diversidad se obtiene una nueva solución aleatoria
        ArrayData = GetAleatorySolution(level + 1)

    # Devolvemos la solución obtenida
    return ArrayData

# Funcion para validar la diversidad en la solución, recibe como parametro la solución a validar
def validateDiversity(currentSolution):
    global Population, Amount, Parameters, Incumbent
    # Tomamos como base que cumple diversidad
    valid = True
    # Variable que guardara la cantidad de items diferentes con cada miembro a verificar
    currentDiversity = 0

    # Validamos la diversidad con la incumbente si existe
    if (len(Incumbent) > 0):
        # Recorremos la solución y la incumbente según la cantidad de productos
        for i in range(Amount):
            # Si el item es diferente en la solucion y la incumbente se suma 1 a la diversidad
            if (currentSolution[i] != Incumbent[i]):
                currentDiversity += 1

        # Se valida si la diversidad obtenida es menor a la requerida según los parametros
        if (currentDiversity < Parameters["diversity"]):
            # Si la diversidad es menor se coloca que no cumple diversidad
            valid = False

    # Solo se validan los miembros de la población si cumple diversidad con la incumbente
    if (valid == True):
        # Recorremos todos los miembros de la población
        for i in range(len(Population)):
            # Reiniciamos los items diferentes al iniciar la validación con un nuevo miembro
            currentDiversity = 0
            # Recorremos la solución y la el miembro actual según la cantidad de productos
            for j in range(Amount):
                # Si el item es diferente en la solucion y el mienbro de la población se suma 1 a la diversidad
                if (currentSolution[i] != Population[i][j]):
                    currentDiversity += 1
            
            # Se valida si la diversidad obtenida es menor a la requerida según los parametros
            if (currentDiversity < Parameters["diversity"]):
                # Si la diversidad es menor se coloca que no cumple diversidad y se detiene la validación
                # ya que con un solo miembro con el que no cumpla diversidad esta no se cumple.
                valid = False
                break

    # Se retorna si cumple o no diversidad
    return valid

# Función para calcular los resultados de la solución
def GetZB(ArraySolution):
    global Products, Amount, Parameters
    # Variables para sumar el valor de z y b según los productos a llevar
    sumZ = 0
    sumB = 0
    # Recorremos la solución hasta la cantidad de productos
    for i in range(Amount):
        # En caso de que el valor de la solución sea 1, es decir que se lleva, se suman los valores de z y b respectivamente
        if (ArraySolution[i] == 1):
            sumZ += Products[i]['value']
            sumB += Products[i]['size']

    # Se agregan lo valores de z y b a las columnas respectivas de la solución
    ArraySolution["z"] = sumZ
    ArraySolution["b"] = sumB

    # Validamos Factibilidad según el tamaño de la canasta dado en los parametros
    if (sumB <= Parameters["basket_size"]):
        ArraySolution["feasibility"] = "SI"
    else:
        ArraySolution["feasibility"] = "NO"

    # Calculamos el z penalizado según la factibilidad obtenida
    if (ArraySolution["feasibility"] == "SI"):
        ArraySolution["penalized"] = ArraySolution["z"]
    else:
        ArraySolution["penalized"] = ArraySolution["z"] / (ArraySolution["b"] - Parameters["basket_size"] + 5)

    # Retornamos el arreglo con sus respectivos valores calculados
    return ArraySolution

# Función para mostrar los datos tabulados
def ShowData(ArrayData):
    global Amount
    # Variable para guardar los encabezados
    header = {}
    # Encabezados para los productos según la cantidad
    for i in range(Amount):
        header[i] = "X" + str(i + 1)

    # Encabezados para los demás datos    
    header["z"] = "Z"
    header["b"] = "B"
    header["feasibility"] = "Factibilidad"
    header["penalized"] = "Z penalizado"
    header["z_k"] = "Z penalizado - k"
    header["initial_range"] = "Rango Inicial"
    header["end_range"] = "Rango Final"

    # Para tabular debe ser una lista, si no lo es lo convertimos a una
    if (type(ArrayData) != list):
        new = []
        new.append(ArrayData)
        ArrayData = new

    # Imprimimos los datos
    print(tabulate(ArrayData, headers=header))

# Función para obtener la población inicial
def GetPopulation():
    global Parameters, Population, Incumbent
    # Variable donde se guarda la informacion de un miembro de la población antes de ingresarlo a la misma
    Person = {}
    # Se obtienen la cantidad de miembros de la población dados en los parametros iniciales
    for i in range(Parameters["population_size"]):
        # Se obtiene el miembro mediante una solución aleatoria
        Person = GetAleatorySolution()
        # Se agrega el miembro a la población
        Population.append(Person)

        # Si el miembro de la población es mejor que la incumbente esta es reemplazada
        if (Person["penalized"] > Incumbent["penalized"]):
            Incumbent = Person

    # Se ordena la población
    Population = OrderPopulation(Population)

    # Mostramos la poblacion inicial sin rango
    print("Población inicial: \n")
    ShowData(Population)

    # Despues de tener la población calculada obtenemos los rangos
    RangeCalculate()

# Función para ordenar la población, esta se recibe como parametro ya que se puede ordenar la población temporal de las iteraciones
def OrderPopulation(DataOrder):
    # Ordenamos la población de manera desendente por la factibilidad
    DataOrder.sort(key=lambda x: x['feasibility'], reverse = True)
    # Completamos la lista ordenada por factibilidad y z penalizado de manera descendente
    list1 = sorted(DataOrder, key=operator.itemgetter("feasibility", "penalized"), reverse = True)
    # Retornamos la nueva lista ordenada
    return list1

# Función para calcular los rangos correspondientes a cada miembro de la población
def RangeCalculate():
    global Population, Parameters
    # Obtenemos el valor de K según el % de k de los parametros y el z penalizado del peor miembro de la población.
    # Como la población esta ordenada obtenemos el z penalizado del ultimo miembro
    K = Population[-1]["penalized"] * (Parameters["k"] / 100)
    # Variable donde se guardara la suma de z - k
    sumZK = 0
    # Recorremos todos los miembros de la población
    for i in range(len(Population)):
        # Obtenemos el valor de z - k de cada miembro de la población
        Population[i]["z_k"] = Population[i]["z"] - K
        # En cada iteración vamos sumando el valor de z -k del miembro actual a la suma de z -k
        sumZK += Population[i]["z_k"]

    # Después de tener el valor de z -k recorremos nuevamente la población para calcular los rangos
    for i in range(len(Population)):
        # Validamos si el valor del rango a calcular es para el primer miembro y aplicamos las formulas pra este
        if (i == 0):
            # Para el primer miembro el valor inicial siempre será 0.0000
            Population[i]["initial_range"] = 0.0000
            # Para el primer miembro el rango final es el valor de z -k dividido la suma de z -k
            Population[i]["end_range"] = Population[i]["z_k"] / sumZK
        else:
            # Para los demás miembros de la población el rango inicial siempre sera el rango final del miembro anterior + 0.0001
            Population[i]["initial_range"] = Population[i - 1]["end_range"] + 0.0001
            # En caso de que sea el ultimo miembro de la población el rango final será 0.9999
            if (i == (len(Population) - 1)):
                Population[i]["end_range"] = 0.9999
            else:
                # Para los demas se aplica la formula correspondiente
                Population[i]["end_range"] = Population[i - 1]["end_range"] + (Population[i]["z_k"] / sumZK)

    # Mostramos la poblacion con rango
    print("Población: \n")
    ShowData(Population)
    iterate()

# Funcion de iteración, aplica para todas las iteraciones
def iterate():
    global Population, Parameters, Iterations, UnimprovedIterations, Amount, Incumbent, InitialSolution
    # Variable en donde diremos si se mejora o no la incumbente
    improveIncumbent = 0
    # Sumamos una nueva iteración a la cantidad de iteraciones realizadas, obteniendo la iteración actual
    Iterations += 1

    # Guardamos la población actual en una nueva variable, que iremos modificando para obtener la población para la siguiente iteración
    NewPopulation = OrderPopulation(Population)

    # Validamos que la iteación actual este dentro de la cantidad de iteraciones pedidas en los parametros
    # Validamos que las iteraciones sin mejorar este por debajo de las permitidas en los parametros

    if (Iterations <= Parameters["iterations"] and UnimprovedIterations < Parameters["unimproved_iterations"]):
        # Realizaremos el procedimiento tantas veces como hijos solicitados en los parametros
        for i in range(Parameters["sons"]):
            # Obtenemos el hijo
            Son = GetSon()
            # Variable dode se indica si el hijo puede validar z para entrar a la población
            GetIn = 0
            # Si el hijo cumple diversidad puede validar z para determinar si entra a la población
            if (validateDiversity(Son)):
                GetIn = 1

            # Si el hijo tiene mejora el z penalizado de la incumbente
            if (Son["penalized"] > Incumbent["penalized"]):
                # Reemplaza la incumbente
                Incumbent = Son
                # Puede validar z para determinar si entra a la población
                GetIn = 1
                # Se guarda la variable para indicar que la incumbente mejoro
                improveIncumbent = 1

            # Si el hijo puede validar z para determinar si entra a la población
            if (GetIn == 1):
                # Si el z penalizado del hijo es mejor que el z penalizado del más malo
                # Como la población esta ordenada validamos con el ultimo
                # Validamos con la nueva población ya que el más malo puede ser un hijo de ua iteración anterior
                if (Son["penalized"] > NewPopulation[-1]["penalized"]):
                    # Si el z penalizado del hijo es mejor, el hijo entra a reemplazar el mas malo
                    # Se reemplaza el mas malo de la nueva población ya que los padres debe seguir saliendo de la población anterior
                    NewPopulation[-1] = Son

            # Ordenamos la nueva población para que el más malo quede al final
            NewPopulation = OrderPopulation(NewPopulation)

            # Se repite el proceso para los demás hijos de la iteración

        # Guardamos la incumbente actual

        currentIncumbent = Incumbent["penalized"]
        NewPopulation = mutate(NewPopulation)
        NewPopulation = recombine(NewPopulation)
        
        print("\nPoblación después de Recombinar y Mutar: \n")
        ShowData(NewPopulation)
        
        if (currentIncumbent != Incumbent["penalized"]):
            improveIncumbent = 1

        # Si la incumbente mejoro se reinicia el contador de las iteracioes sin mejorar
        if (improveIncumbent == 1):
            UnimprovedIterations = 0
        else:
            # En caso de no mejorar la incumbente se suma uno al cotador de las iteraciones sin mejorar
            UnimprovedIterations += 1

        # Mostramos los datos otenidos
        print("Iteración " + str(Iterations) + ":\n")
        print("Iteraciones sin mejorar: " + str(UnimprovedIterations) + "\n")
        # Mostramos la incumbente actual
        print("Incumbente actual: \n")
        ShowData(Incumbent)

        # Al finalizar la iteración reemplazamos la población, ya que esta es la que se usará para la siguiente generación
        Population = OrderPopulation(NewPopulation)
        # Obtenemos los nuevos rangos de la población y al finalizar automaticamente se inicia la nueva iteración
        RangeCalculate()
        
    else:
        # Mostramos los datos otenidos cuando ya no se va a iterar más
        print("Final:\n")
        print("Iteraciones realizadas: " + str(Iterations - 1) + "\n")
        # Mostramos la incumbente actual
        print("Incumbente obtenida: \n")
        ShowData(Incumbent)
        # Mostramos la poblacion con rango
        print("Población: \n")
        ShowData(Population)

# Funcion para obtener hijos dentro de las iteraciones
def GetSon():
    global Parameters, Amount, Population
    # Obtenemos el primer padre
    FatherOne = GetFatherOne()
    # Obtenemos el segundo padre, se tiene en cuenta que no puede ser igual al primero
    FatherTwo = GetFatherTwo(FatherOne)
    # Obtenemos el cruce
    # Se tiene en cuenta la diversidad por lo que el cruce es mayor a la diversidad + 1 y meor a la cantidad de productos - diversidad
    crossing = random.randint(Parameters["diversity"] + 1, Amount - Parameters["diversity"])
    # Variable donde se guardara los datos del hijo
    Son = {}
    # Se asignan los valores desde el inicio hasta el cruce del padre uno
    for i in range(crossing):
        Son[i] = Population[FatherOne][i]
    # Se asigan los valores desde el cruce hasta el final del padre 2
    for i in range(crossing, Amount):
        Son[i] = Population[FatherTwo][i]

    # Se obtienen los datos para la solucion dada por el cruce
    Son = GetZB(Son)

    # Se retorna el hijo obtenido
    return Son

# Funcion con la que se obtiene el primer padre para un hijo
def GetFatherOne():
    global Population
    # Obtenemos un aleatorio
    number = random.random()
    # Por defecto no se ha seleccionado padre dentro de la población
    Father = 0

    # Recorremos la población
    for i in range(len(Population)):
        # Si el aleatorio se encuentra dentro del rango del miembro de la población actual
        if (number >= Population[i]["initial_range"] and number <= Population[i]["end_range"]):
            # El miembro de la población actual es seleccionado como padre
            Father = i
            # Se termina la validación del rango, ya que no es posible que este detro del rango de dos miembros de la población
            break

    # Retornamos el padre obtenido
    return Father

# Función para obtener el segundo padre
def GetFatherTwo(FatherOne, level = 1):
    global Population
    # Obtenemos un aleatorio
    number = random.random()
    # Por defecto no se ha seleccionado padre dentro de la población
    Father = 0

    # Se se llevan 50 repeticiones sin econtrar un padre diferente al primero se suspende la eecución para evitar ciclos infinitos
    if (level == 50):
        raise Exception('No fue posible hallar dos padres diferentes')

    # Recorremos la población    
    for i in range(len(Population)):
        # Si el aleatorio se encuentra dentro del rango del miembro de la población actual
        if (number >= Population[i]["initial_range"] and number <= Population[i]["end_range"]):
            # El miembro de la población actual es seleccionado como padre
            Father = i
            # Se termina la validación del rango, ya que no es posible que este detro del rango de dos miembros de la población
            break
    
    # Si el padre obtenido es igual al padre uno
    if (Father == FatherOne):
        # Se llama de manera recursiva para otener un segundo padre diferente al primero
        Father = GetFatherTwo(FatherOne, level + 1)

    # Se retorna el padre obtenido
    return Father

# Funcion para realizar la mutación
def mutate(MutatePopulation):
    global Amount, Incumbent
    localIncumbent = GetZB(Incumbent)
    # Obtenemos la cantidad de genes
    genes = Amount * len(MutatePopulation)
    # Aleatoriamente sacamos el gen a mutar
    GeneMutate = random.randint(1, genes)
    # Obtenemos el miembro de la poblacion del gen
    GenFather = GeneMutate // Amount
    # Obtenemos la posicion del gen en el miembro de la poblacion
    position = GeneMutate % Amount
    # En caso de que la posicion nos de 0 realmente es el ultimo gen del miembro de la poblacion, la cantidad de productos
    if (position == 0):
        position = Amount
        GenFather -= 1

    # Por indices en los arreglos se les resta 1 a los datos obtenidos
    position -= 1

    # Cambiamos el valor del gen
    if (MutatePopulation[GenFather][position] == 1):
        MutatePopulation[GenFather][position] = 0
    else:
        MutatePopulation[GenFather][position] = 1
    
    # Obtenemos los datos con la nueva solucion obtenida por mutación
    MutatePopulation[GenFather] = GetZB(MutatePopulation[GenFather])
    print("Nuevos datos")
    print(localIncumbent)
    # Si la nueva solucion mejora la incumbente la reemplaza
    print(MutatePopulation[GenFather])
    print(Incumbent)
    if (MutatePopulation[GenFather]["penalized"] > Incumbent["penalized"]):
        Incumbent = MutatePopulation[GenFather]

    # Retornamos la nueva poblacion obtenida
    return MutatePopulation

def recombine(RecombinePopulation):
    global Amount, Incumbent

    # Obtenemos el miembro de la poblacion del gen
    GenFather = random.randint(1, len(RecombinePopulation))
    # Obtenemos el primer gen
    Gen1 = random.randint(1, Amount)
    # Obtenemos el segundo gen, diferente al gen 1
    Gen2 = Gen1
    while Gen2 == Gen1:
        Gen2 = random.randint(1, Amount)

    # Por indices en los arreglos se les resta 1 a los datos obtenidos
    GenFather -= 1
    Gen1 -= 1
    Gen2 -= 1

    # Intercambiamos los valores de los genes
    assistant = RecombinePopulation[GenFather][Gen1]
    RecombinePopulation[GenFather][Gen1] = RecombinePopulation[GenFather][Gen2]
    RecombinePopulation[GenFather][Gen2] = assistant

    # Obtenemos los datos con la nueva solucion obtenida por mutación
    RecombinePopulation[GenFather] = GetZB(RecombinePopulation[GenFather])

    # Si la nueva solucion mejora la incumbente la reemplaza
    if (RecombinePopulation[GenFather]["penalized"] > Incumbent["penalized"]):
        Incumbent = RecombinePopulation[GenFather]

    # Retornamos la nueva poblacion obtenida
    return RecombinePopulation

# Datos quemados para pruebas
Parameters = {'basket_size': 15, 'population_size': 4, 'diversity': 2, 'recombination': 10, 'mutation': 2, 'iterations': 5, 'unimproved_iterations': 3, 'sons': 4, 'k': 90}
Products = [{'value': 815, 'size': 5}, {'value': 1040, 'size': 7}, {'value': 1980, 'size': 4}, {'value': 1520, 'size': 8}, {'value': 3570, 'size': 6}, {'value': 2100, 'size': 3}]
Amount = 6
InitialSolution = {0: 1, 1: 1, 2: 0, 3: 0, 4: 0, 5: 1, 'z': 3955, 'b': 15, 'feasibility': 'SI', 'penalized': 3955}
# Incumbent = {0: 1, 1: 1, 2: 1, 3: 0, 4: 0, 5: 0, 'z': 2153, 'b': 14, 'feasibility': 'SI', 'penalized': 2153}
# Population = [{0: 0, 1: 1, 2: 1, 3: 1, 4: 0, 5: 0, 'z': 2564, 'b': 13, 'feasibility': 'SI', 'penalized': 2564}, {0: 0, 1: 0, 2: 0, 3: 0, 4: 1, 5: 0, 'z': 2100, 'b': 7, 'feasibility': 'SI', 'penalized': 2100}, {0: 0, 1: 1, 2: 0, 3: 1, 4: 1, 5: 0, 'z': 3850, 'b': 17, 'feasibility': 'NO', 'penalized': 481.25}, {0: 1, 1: 1, 2: 0, 3: 1, 4: 0, 5: 1, 'z': 2332, 'b': 15, 'feasibility': 'NO', 'penalized': 388.6666666666667}]

# Incumbente mejorada en la población
Incumbent = {0: 1, 1: 1, 2: 0, 3: 0, 4: 0, 5: 1, 'z': 3955, 'b': 15, 'feasibility': 'SI', 'penalized': 3955}

# Población con rangos
Population = [{0: 0, 1: 1, 2: 1, 3: 1, 4: 0, 5: 0, 'z': 2564, 'b': 13, 'feasibility': 'SI', 'penalized': 2564, 'z_k': 2253.0666666666666, 'initial_range': 0.0, 'end_range': 0.23463904355915965}, {0: 0, 1: 0, 2: 0, 3: 0, 4: 1, 5: 0, 'z': 2100, 'b': 7, 'feasibility': 'SI', 'penalized': 2100, 'z_k': 1789.0666666666666, 'initial_range': 0.23473904355915964, 'end_range': 0.4209561631281503}, {0: 0, 1: 1, 2: 0, 3: 1, 4: 1, 5: 0, 'z': 3850, 'b': 17, 'feasibility': 'NO', 'penalized': 481.25, 'z_k': 3539.0666666666666, 'initial_range': 0.4210561631281503, 'end_range': 0.7895219184359249}, {0: 1, 1: 1, 2: 0, 3: 1, 4: 0, 5: 1, 'z': 2332, 'b': 15, 'feasibility': 'NO', 'penalized': 388.6666666666667, 'z_k': 2021.0666666666666, 'initial_range': 0.7896219184359249, 'end_range': 0.9999}]

# Se inicia obteniendo los parametros
# GetParameters()
iterate()