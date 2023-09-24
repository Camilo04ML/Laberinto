import csv
# Colorama es una extensión para mostrar los caracteres de distintos colores
from colorama import Fore, Style  

# Primero se define la clase que resolverá el laberinto
class MazeSolver:
    def __init__(self):
        self.paths = []  

    # Método para encontrar la entrada y salida del laberinto
    def find_start_end(self, maze):
        rows = len(maze)
        cols = len(maze[0])
        start = None
        end = None

        # Ubicación de la entrada y la salida
        for x in range(cols):
            if maze[0][x] == 0:
                start = (x, 0)  
            if maze[rows - 1][x] == 0:
                end = (x, rows - 1)  

        # Se busca la entrada en la primera y última columna (excepto las esquinas anteriormente establecidas)
        for y in range(1, rows - 1):
            if maze[y][0] == 0:
                start = (0, y)  
            if maze[y][cols - 1] == 0:
                end = (cols - 1, y)  

        return start, end

    # Este es el método recursivo para resolver el laberinto
    def solve(self, maze, startX, startY, endX, endY, path=[]):
        rows = len(maze)
        cols = len(maze[0])

        # Verificar si estamos fuera de los límites o en una celda bloqueada
        if (
            startX < 0 or startX >= cols or
            startY < 0 or startY >= rows or
            maze[startY][startX] == 1
        ):
            return

        path.append((startX, startY))  # Agregar la posición actual a la ruta

        if startX == endX and startY == endY:
            self.paths.append(list(path)) 
            path.pop()  
            return

        maze[startY][startX] = 1  # Marcar la celda como visitada

        # Explorar las cuatro direcciones posibles
        self.solve(maze, startX + 1, startY, endX, endY, path)
        self.solve(maze, startX - 1, startY, endX, endY, path)
        self.solve(maze, startX, startY + 1, endX, endY, path)
        self.solve(maze, startX, startY - 1, endX, endY, path)

        maze[startY][startX] = 0  
        path.pop()  

    # Método para mostrar el laberinto en color
    def display_maze(self, maze, path=[], show_crosses=False):
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if (x, y) in path and show_crosses:
                    print(Fore.GREEN + "0", end=' ')  # Mostrar los "0" en verde 
                elif cell == 1:
                    print(Fore.RED + "1", end=' ')  # Mostrar los "1" en rojo 
                else:
                    print(Fore.WHITE + "0", end=' ')  # Mostrar los espacios no recorridos en blanco
            print(Style.RESET_ALL)  



def cargar_laberinto(matriz):
    laberinto = []
    with open(matriz, 'r') as archivo:
        lector_csv = csv.reader(archivo) #Se carga el archivo csv
        for fila in lector_csv:
            laberinto.append(list(map(int, fila)))  
    return laberinto


# Ejecución del programa
matriz = 'matriz.csv'
laberinto = cargar_laberinto(matriz)  

solver = MazeSolver()  
start, end = solver.find_start_end(laberinto)  
startX, startY = start 
endX, endY = end 

# Mostrar el laberinto original en color
print(f'\nLaberinto:')
solver.display_maze(laberinto)

# Resolver el laberinto
solver.solve(laberinto, startX, startY, endX, endY)

# Mostrar todas las rutas encontradas en color
for idx, path in enumerate(solver.paths):
    print(f'\nRuta #{idx + 1}:')
    solver.display_maze(laberinto, path, show_crosses=True)