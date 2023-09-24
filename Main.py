import csv
from colorama import Fore, Style  # Importar módulos necesarios

# Definir la clase MazeSolver para resolver el laberinto
class MazeSolver:
    def __init__(self):
        self.paths = []  # Lista para almacenar las rutas encontradas

    # Método para encontrar la entrada y salida del laberinto
    def find_start_end(self, maze):
        rows = len(maze)
        cols = len(maze[0])
        start = None
        end = None

        # Buscar la entrada en la primera y última fila
        for x in range(cols):
            if maze[0][x] == 0:
                start = (x, 0)  # Entrada en la primera fila
            if maze[rows - 1][x] == 0:
                end = (x, rows - 1)  # Salida en la última fila

        # Buscar la entrada en la primera y última columna (excepto las esquinas ya verificadas)
        for y in range(1, rows - 1):
            if maze[y][0] == 0:
                start = (0, y)  # Entrada en la primera columna
            if maze[y][cols - 1] == 0:
                end = (cols - 1, y)  # Salida en la última columna

        return start, end

    # Método recursivo para resolver el laberinto
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
            self.paths.append(list(path))  # Agregar la ruta encontrada a la lista de rutas
            path.pop()  # Eliminar la posición actual antes de retroceder
            return

        maze[startY][startX] = 1  # Marcar la celda como visitada

        # Explorar las cuatro direcciones posibles
        self.solve(maze, startX + 1, startY, endX, endY, path)
        self.solve(maze, startX - 1, startY, endX, endY, path)
        self.solve(maze, startX, startY + 1, endX, endY, path)
        self.solve(maze, startX, startY - 1, endX, endY, path)

        maze[startY][startX] = 0  # Desmarcar la celda antes de retroceder
        path.pop()  # Retroceder eliminando la posición actual

    # Método para mostrar el laberinto en color
    def display_maze(self, maze, path=[], show_crosses=False):
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if (x, y) in path and show_crosses:
                    print(Fore.GREEN + "0", end=' ')  # Mostrar "0" en verde en las rutas
                elif cell == 1:
                    print(Fore.RED + "1", end=' ')  # Mostrar "1" en rojo para obstáculos/paredes
                else:
                    print(Fore.WHITE + "0", end=' ')  # Mostrar "0"en blanco para espacio libre
            print(Style.RESET_ALL)  # Restablecer el color después de cada fila

def cargar_laberinto(matriz):
    laberinto = []
    with open(matriz, 'r') as archivo:
        lector_csv = csv.reader(archivo)
        for fila in lector_csv:
            laberinto.append(list(map(int, fila)))  # Leer el laberinto desde el archivo CSV
    return laberinto

matriz = 'matriz.csv'
laberinto = cargar_laberinto(matriz)  # Cargar el laberinto desde el archivo CSV

solver = MazeSolver()  # Crear una instancia de MazeSolver
start, end = solver.find_start_end(laberinto)  # Encontrar la entrada y salida del laberinto
startX, startY = start # type: ignore
endX, endY = end # type: ignore

# Mostrar el laberinto original en color
solver.display_maze(laberinto)

# Resolver el laberinto
solver.solve(laberinto, startX, startY, endX, endY)



# Mostrar todas las rutas encontradas en color
for idx, path in enumerate(solver.paths):
    print(f'\nRuta {idx + 1}:')
    solver.display_maze(laberinto, path, show_crosses=True)
