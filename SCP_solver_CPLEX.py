'''
Investigacion de operaciones 003 
Examen 2/4: Set Covering Problem
Ian Mauricio Saucedo Aleman     
Destiny Yareli De La Fuente Aguilar
Alberto Carlos Almaguer Rodríguez

'''
import cplex 
import os

def restricciones(numElementos, numSubconj, subconj, names):
    constraints = []
    coef_x = []
    for i in range(numElementos):
        for j in range(numSubconj):
            if (j + 1) in subconj[i]:
                coef_x.append(1)
            else: 
                coef_x.append(0)
        row = [names, coef_x]
        constraints.append(row)
        coef_x = []
    return constraints

def resolver(numElementos, numSubconj, costosSubconj, subconj, nombre_scp):
    problem = cplex.Cplex()
    problem.objective.set_sense(problem.objective.sense.minimize)
    names = []
    lower_bounds = []
    upper_bounds = []
    v_types = ""
    for i in range(numSubconj):
        names.append("x" + str(i + 1))
        lower_bounds.append(0)
        upper_bounds.append(10)
        v_types = v_types + "I"
    objective = costosSubconj
    problem.variables.add(obj = objective,
                      lb = lower_bounds,
                      ub = upper_bounds,
                      names = names, 
                      types = v_types)
    constraint_names = []
    constraints = restricciones(numElementos, numSubconj, subconj, names)
    rhs = []
    constraint_senses = []
    for i in range(numElementos):
        rhs.append(1)
        constraint_senses.append("G")
        constraint_names.append("c" + str(i + 1))
    problem.linear_constraints.add(lin_expr = constraints,
                               senses = constraint_senses,
                               rhs = rhs,
                               names = constraint_names)
    problem.solve()
    
    #print(problem.write_as_string())
    print("Soluciones")
    print(problem.solution.get_values())
    soluciones = problem.solution.get_values()
    val_objetivo = 0
    #confirmar_sol = ""
    #subconj_sol = []
    for i in range(numSubconj):
        val_objetivo = val_objetivo + soluciones[i] * costosSubconj[i]
    '''
    Esta parte se utilizo para verificar soluciones
    for i in range(len(subconj)):
        for j in range(len(soluciones)):
            if soluciones[j] == 1.0 and (j + 1) in subconj[i]: 
                confirmar_sol = confirmar_sol + "\nElemento " + str(i+1) + " en subconjunto: " + str(j+1)
    for i in range(len(soluciones)):
        if soluciones[i] == 1.0:
            subconj_sol.append(i+1)
    '''
    print("Valor objetivo: " + str(val_objetivo))
    #print(confirmar_sol)
    #print("Subconjuntos de la solucion: ", subconj_sol)
    archivoSolucion = open(nombre_scp.rstrip(".txt") + ".sol", "w")
    archivoSolucion.write("Soluciones: \n" + str(soluciones))
    archivoSolucion.write("\nValor objetivo: " + str(val_objetivo))
    print("Archivo solucion creado en " + archivoSolucion.name)
    archivoSolucion.close()

print("Ingresa la ruta del archivo: ")
ruta = str(input())
#ruta = 'C:/Users/iansa/Downloads/scp41.txt'
try: 
    archivo = open(ruta, 'r')

    lista = archivo.readline().split()

    #print(lista)
    cant_subconjuntos = 0 
    universo = 0 
    i=0
    for linea in lista:
        for palabra in linea.split():
            if i == 0:
                universo = palabra
            elif i== 1: 
                cant_subconjuntos = palabra 
        i=i+1

    print ('Cantidad de subconjuntos :'+ cant_subconjuntos)
    print ('Universo del 1 al '+ universo)
    u = int(universo) 
    s = int(cant_subconjuntos)

    j=0
    array_costos = []
    costos_subconjuntos = []
    array_subconjuntos = [[]]
    array_elementos = []
    x=0
    z=0
    k=s
    new_subconj = 0
    subconjunto_aux = []
    linea.split()
    for linea in archivo:
        for palabra in linea.split():
            if j < s: 
                costos_subconjuntos.append(int(palabra))
                j = j+1
            elif j == k:
                k = k + int(palabra) + 1
                j = j+1
                new_subconj = 1
                subconjunto_aux = []
            elif j < k:
                subconjunto_aux.append(int(palabra))
                j = j+1
        if subconjunto_aux != [] and new_subconj == 1:
            array_subconjuntos.append(subconjunto_aux)
            new_subconj = 0
    array_subconjuntos.pop(0)

    for i in range(u): 
        array_elementos.append(i + 1)
    resolver(u, s, costos_subconjuntos, array_subconjuntos, archivo.name)
except:
    print("No existe archivo correcto en ruta ingresada")
