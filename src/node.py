import tkinter as tk

class Node:
    '''
    Node class that contains information about a node
    Holds its ID, label, conections, if it is an entry/exit point, and color
    '''

    def __init__(self, id: str, label: str, color: str='gray', entryPoint:bool=False, exitPoint:bool=False):
        self.__id: str = id
        self.__label: str = label
        self.__NodesToFlowTo: list[tuple] = []
        self.__entryPoint: bool = entryPoint
        self.__exitPoint: bool = exitPoint
        self.__color: str = color if self.__isValidColor(color) else 'gray'

    #get methods
    def getID(self) -> str:
        return self.__id
    
    def getLabel(self) -> str:
        return self.__label
    
    def getCopyOfConnections(self) -> list:
        return self.__NodesToFlowTo.copy()
    
    def getEntryPoint(self) -> bool:
        return self.__entryPoint
    
    def getExitPoint(self) -> bool:
        return self.__exitPoint
    
    def getColor(self) -> str:
        return self.__color
    
    # Setter methods
    def setID(self, id: str):
        self.__id = id
    
    def setLabel(self, label: str):
        self.__label = label
    
    def setEntryPoint(self, entryPoint: bool):
        self.__entryPoint = entryPoint
    
    def setExitPoint(self, exitPoint: bool):
        self.__exitPoint = exitPoint

    def setColor(self, color: str):
        if (self.__isValidColor(color)):
            self.__color = color
        else:
            self.__color = 'gray'
    
    def __isValidColor(self, color: str='gray') -> bool:
        root = tk.Tk()
        root.withdraw()  # hide main window
        try:
            root.winfo_rgb(color)
            return True
        except tk.TclError:
            return False
        finally:
            root.destroy()

    #Node flow functions

    #Adds a node to this nodes list of where it flows to
    def addNode(self, nodeID:str, color:str='gray'):
        if (self.__isValidColor(color)):
            if (nodeID, color) not in self.__NodesToFlowTo:
                self.__NodesToFlowTo.append((nodeID, color))
        else:
            if (nodeID, color) not in self.__NodesToFlowTo:
                self.__NodesToFlowTo.append((nodeID, 'gray'))

    #deletes connections from this node to another node
    def deleteConnection(self, nodeID:str, color:str = "",  deleteAllFlowsToID:bool=True, resetFlows:bool=False, 
                         print_removal = True):
        if (resetFlows):
            self.__NodesToFlowTo.clear()
        elif (deleteAllFlowsToID):
            self.__NodesToFlowTo = list(filter(lambda x: nodeID not in x, self.__NodesToFlowTo))
        else:
            try:
                self.__NodesToFlowTo.remove((nodeID, color))
                if print_removal:
                    print("\nNode Conncetion removed")
            except ValueError:
                if print_removal:
                    print("\nNode connection not found")
        
    def fileString(self):
        return f"('{self.getID()}', '{self.getLabel()}', '{self.getColor()}', {self.getEntryPoint()}, \
{self.getExitPoint()}, {self.getCopyOfConnections()})"

    def __str__(self):
        return f"{self.getID()}, {self.getLabel()}"
        
    