import tkinter as tk

class Node:
    '''
    Node class that contains information about a node
    Holds its ID, label, conections, if it is an entry/exit point, and color
    '''

    __label = None #Name to display
    __id = None #Unique ID
    __NodesToFlowTo = [] #Holds tuples for nodes this node flows to and color of connection, [id, color]
    __entryPoint = False
    __exitPoint = False
    __color = 'gray'

    def __init__(self, label, id, color='gray', entryPoint=False, exitPoint=False):
        self.setLabel(label)
        self.setID(id)
        self.setEntryPoint(entryPoint)
        self.setExitPoint(exitPoint)
        self.setColor(color)

    #get methods
    def getID(self):
        return self.__id
    
    def getLabel(self):
        return self.__label
    
    def getCopyOfConnections(self):
        return self.__NodesToFlowTo.copy()
    
    def getEntryPoint(self):
        return self.__entryPoint
    
    def getExitPoint(self):
        return self.__exitPoint
    
    def getColor(self):
        return self.__color
    
    # Setter methods
    def setID(self, id):
        self.__id = id
    
    def setLabel(self, label):
        self.__label = label
    
    def setEntryPoint(self, entryPoint):
        self.__entryPoint = entryPoint
    
    def setExitPoint(self, exitPoint):
        self.__exitPoint = exitPoint

    def setColor(self, color):
        if (self.__isValidColor(color)):
            self.__color = color
        else:
            self.__color = 'gray'
    
    def __isValidColor(self, color):
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
    def addNode(self, nodeID, color='gray'):
        if (self.__isValidColor(color)):
            if (nodeID, color) not in self.__NodesToFlowTo:
                self.__NodesToFlowTo.append((nodeID, color))
        else:
            if (nodeID, color) not in self.__NodesToFlowTo:
                self.__NodesToFlowTo.append((nodeID, 'gray'))

    #deletes connections from this node to another node
    def deleteConnection(self, nodeID, description = "",  deleteAllFlowsToID = True, resetFlows = False, 
                         print_removal = True):
        if (resetFlows):
            self.__NodesToFlowTo.clear()
        elif (deleteAllFlowsToID):
            self.__NodesToFlowTo = list(filter(lambda x: nodeID not in x, self.__NodesToFlowTo))
        else:
            try:
                self.__NodesToFlowTo.remove((nodeID, description))
                if print_removal:
                    print("\nNode Conncetion removed")
            except ValueError:
                if print_removal:
                    print("\nNode connection not found")
        

    def __str__(self):
        return f"{self.__id}, {self.__label}"
        
    