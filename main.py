import csv
import math
from copy import deepcopy
from pprint import pprint


def csvMatrixReader(path):
    adjacencyMatrix = []
    with open(path, 'r') as matrixFile:
        matrixReader = csv.reader(matrixFile, delimiter=';')
        for row in matrixReader:
            adjacencyMatrix.append([int(cell) for cell in row])
    return adjacencyMatrix


def multiplyMatrices(matrix1, matrix2):
    rows = len(matrix1)
    cols = len(matrix1[1])
    matrixProduct = [[0 for _ in range(cols)]for _ in range(rows)] # bestPractice "für alle"

    for row in range(rows):
        for col in range(cols):
            for i in range(cols):
                matrixProduct[row][col] += matrix1[row][i] * matrix2[i][col]
    return(matrixProduct)


def addingMatrices(matrix1, matrix2):
    rows = len(matrix1)
    cols = len(matrix1[1])
    matrixSum = [[0 for _ in range(cols)] for _ in range(rows)] # bestPractice "für alle"

    for row in range(rows):
        for col in range(cols):
            matrixSum[row][col] = matrix1[row][col] + matrix2[row][col]
    return matrixSum


def calcDistancyMatrix(adjacencyMatrix):
    rows = len(adjacencyMatrix)
    cols = len(adjacencyMatrix)

    distanzmatrix = [[0 if row == col else math.inf for row in range(rows)]for col in range(cols)] # initialisierung der Distanzmatrix
    for row in range(rows):
        for col in range(cols):
            if adjacencyMatrix[row][col] == 1:
                distanzmatrix[row][col] = adjacencyMatrix[row][col] # übertragen der Adjazenzmatrix

    matrix_step = adjacencyMatrix
    for step in range(2, rows+1): # zählt Durchläufe der Schleife
        matrix_step = multiplyMatrices(adjacencyMatrix, matrix_step) # berechnet die Adjazenzmtrix zur Potenz 'step'
        for row in range(rows):
            for col in range(cols):
                if distanzmatrix[row][col] == math.inf and matrix_step[row][col] != 0: # ersetzt Werte in jedem Durchlauf
                    distanzmatrix[row][col] = step
    return distanzmatrix


def calcExctricitys(distancyMatrix):
    eccentricitys = []
    if len(findComponents(adjacencyMatrix)) == 1:
        for row in distancyMatrix:
            eccentricitys.append(max(row))
        return eccentricitys


def calcDiameter(eccentricitys):
    try:
        return max((eccentricitys))
    except:
        return 'Graph nicht zusammenhängend'


def calcRadius(eccentricitys):
    try:
        return min((eccentricitys))
    except:
        return 'Graph nicht zusammenhängend'


def calcCentre(eccentricitys):
    centre = []
    try:
        for ecc in range(len(eccentricitys)):
            if eccentricitys[ecc] == min(eccentricitys):
                centre.append(ecc + 1)
        return centre
    except:
        return 'Graph nicht zusammenhängend'


def dfs(graph, visited, vertex, component):
    visited[vertex] = True
    component.append(vertex + 1)

    for neighbor in range(len(graph)):
        if graph[vertex][neighbor] == 1 and not visited[neighbor]:
            dfs(graph, visited, neighbor, component)


def findComponents(adjacencyMatrix):
    numVertices = len(adjacencyMatrix)
    visited = [False] * numVertices
    components = []

    for node in range(numVertices):
        if not visited[node]:
            component = []
            dfs(adjacencyMatrix, visited, node, component)
            components.append(component)
    return components


def removeVertex(matrix, vertex):
    matrix = deepcopy(matrix) #

    del matrix[vertex] # entfernt Zeile

    for vertexx in range(len(matrix)): # entfernt Spalte
        del matrix[vertexx][vertex]

    return matrix


def findArticulations(adjacencyMatrix):
    numVertices = len(adjacencyMatrix)
    articulations = []
    numArticulations = len(findComponents(adjacencyMatrix)) # Anzahl der Artikulationen in der Adjazenzmatrix

    for vertex in range(0, numVertices):
        matrixTemp = removeVertex(adjacencyMatrix, vertex)
        if len(findComponents(matrixTemp)) > numArticulations: # vergleicht, ob nach entfernen des Knoten mehr Artikulationen entstanden sind
            articulations.append(vertex + 1) # KnotenA = Knoten1
    return articulations

def removeEdge(matrix, vertex1, vertex2):
    matrix = deepcopy(matrix)
    if matrix[vertex1][vertex2]: # falsly/truly
        matrix[vertex1][vertex2] = 0
        matrix[vertex2][vertex1] = 0
    return matrix


def findBridges(adjacencyMatrix):
    rows = len(adjacencyMatrix)
    cols = len(adjacencyMatrix)
    bridges = []
    numComponents = len(findComponents(adjacencyMatrix)) # Anzahl der Komponenten in der Adjazenzmatrix

    for row in range(rows):
        for col in range(row, cols): # range(start, stop, step)
            matrixTemp = removeEdge(adjacencyMatrix, row, col)
            if len(findComponents(matrixTemp)) > numComponents: # vergleicht, ob nach entfernen der Kante mehr Artikulationen entstanden sind
                bridges.append([row+1, col+1]) # KnotenA = Knoten1
    return bridges


############################################################### print('Ausgabe:')

path = 'C:/Users/Paul/Kollegg/Informatik/scratch/xyz.csv'
adjacencyMatrix = csvMatrixReader(path)

print('Adjazenz Matrix:')
pprint(adjacencyMatrix)
print()

print('Distanz Matrix:')
distancyMatrix = calcDistancyMatrix(adjacencyMatrix)
pprint(distancyMatrix)
print()

excentricitys = calcExctricitys(distancyMatrix)

print(f'Exzentrizitäten: {dict(enumerate(excentricitys, start=1))} \n ')

print(f'Radius: {calcRadius(excentricitys)} \n')

print(f'Durchmesser: {calcDiameter(excentricitys)} \n')

print(f'Zentrum: {calcCentre(excentricitys)} \n')

print(f'Komponenten: {findComponents(adjacencyMatrix)} \n')

print(f'Artikulationen: {findArticulations(adjacencyMatrix)} \n')

print(f'Brücken: {findBridges(adjacencyMatrix)}')



# findArticulations(matrixAlsCsvEinlesen('C:/Users/Paul/Kollegg/Informatik/scratch/24n_01.csv'))
# findBridges(matrixAlsCsvEinlesen('C:/Users/Paul/Kollegg/Informatik/scratch/matrix3.csv'))
# calcWegMatrix((matrixAlsCsvEinlesen('C:/Users/Paul/Kollegg/Informatik/scratch/matrix2.csv')))
#
# findComponents((matrixAlsCsvEinlesen('C:/Users/Paul/Kollegg/Informatik/scratch/matrix.csv')))