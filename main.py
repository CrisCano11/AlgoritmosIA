import matplotlib.pyplot as plt
import random as rd
from genetico import *
from tabu import *

canas = 0
canasta = 0
bprima = 0
solucion = []
cantCosto = 0
arrProductos  = [] 
cantProducto = 1


def Parametros():
  global canas
  global cantProducto
  global arrProductos
  global canasta
  seguir = False
  n =0
  
  
  canasta = int(input("Ingrese el valor de la canasta \n"))
  if canasta == 0:
    print("La canasta no puede ser igual o menor a 0 (Cero)")
    return
  else:
    while n != 2:
          producto = {}
          producto['costo']  = int(input("Ingresa el  valor del producto:\n"))
          producto['peso']       = int(input("Ingresa el  tamaño del producto:\n"))
          producto['beneficio']        = float(producto['costo']) / float(producto['peso'])
          canas = canas + producto['peso']
          arrProductos.append(producto)
          cantProducto += 1
          n = int(input("Desea agregar otro producto: \n 1. Si \n 2. No \n"))

      
    if canasta >= canas:
        seguir = False
        print("Puede llevar todos los productos")
    elif canasta < canas:
        seguir = True   
  return seguir

def Goloso():
  nuevaLista = []
  global solucion
  global cantCosto
  global canasta
  global bprima 
  seguir = Parametros()
  
  if seguir:
    nuevaLista = sorted(arrProductos,key=lambda x: x['beneficio'],reverse= True)
    for j in range(len(nuevaLista)):
      if(nuevaLista[j]['peso'] <= canasta):
          solucion.append(1)
          canasta =  canasta - nuevaLista[j]['peso']
          bprima = bprima + nuevaLista[j]['peso']
          cantCosto += nuevaLista[j]['costo']
      else:
        solucion.append(0)
        
      print(' Costo: ',nuevaLista[j]['costo'], ' Peso: ',nuevaLista[j]['peso'], ' Canasta: ',canasta, ' Lleva: ', solucion[j])
    print('Beneficio: ', cantCosto, " B': ", bprima)
    
def Difuso():
	nucleo = int(input("Ingrese el valor donde Mu' = 1\n"))
	alfa  = int(input("Ingrese el valor de Alfacut\n"))
	title = input("Ingrese el nombre del grafico\n")
	escala =input("Ingrese su cualidad\n")
	variable = input("Ingrese su forma de medición\n")
	puntoCruce = (nucleo + alfa) / 2
	x= alfa,nucleo
	y= 0,1
	plt.plot(puntoCruce,0.5, marker="o", color="red")
	plt.plot(x,y)
	plt.xlabel(variable)
	plt.ylabel(escala)
	plt.title(title)
	plt.show()
  
def Dinamico():
  global arrProductos
  global cantCosto
  global canasta
  global bprima
  global cantProducto
  seguir = Parametros()
  dp = [[0 for x in range(canasta+1)] for x in range(cantProducto)]
  if seguir:
      
      for i in range(cantProducto):
          for j in range(canasta +1):
            print(dp)
            if i==0 or j==0:
                dp[i][j]=0
            elif arrProductos[i-1]['peso'] <= j:
                dp[i][j] = max(arrProductos[i - 1]['costo'] + dp[i - 1][j - arrProductos[i - 1]['peso']],dp[i - 1][j])
                
            else:
                dp[i][j] = dp[i - 1][j]
  print(cantProducto-1,canasta ,len(dp))          
  return print(dp[cantProducto-1][canasta])
    
opcion = int(input("Menu Principal \n Seleccione metodo de solución \n 1- Greddy - Goloso \n 2- Dinamico \n 3- Graficar conjunto difuso \n 4- Genetico \n 5- Tabu \n 0- Salir \n"))





if opcion == 1:
		Goloso()
		
elif opcion == 2:
		Dinamico()
		
elif opcion == 3:
		Difuso()
		
elif opcion == 4:
		iterate()
		
elif opcion == 5:
		iteracion()
		
else:
		print("Ingrese una opcion valida")
		
opcion = int(input("Menu Principal \n Seleccione metodo de solución \n 1- Greddy - Goloso \n 2- Dinamico \n 3- Graficar conjunto difuso \n 4- Genetico \n 5- Tabu \n 0- Salir \n"))