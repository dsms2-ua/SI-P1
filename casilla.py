class Casilla():
    def __init__(self, f, c):
        self.fila=f
        self.col=c
        
    def getFila (self):
        return self.fila
    
    def getCol (self):
        return self.col
        
    def __eq__(self, other):
        return self.fila==other.fila and self.col==other.col

    def __hash__(self):
        return hash((self.fila, self.col))
    
    def __str__(self):
        return f"({self.fila}, {self.col})"