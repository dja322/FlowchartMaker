
class Node:
    __label = None #Name to display
    __id = None #Unique ID
    __NodesToFlowTo = [] #Holds tuples for nodes this node flows to and a descriptor, [id, desc]
    __entryPoint = False
    __exitPoint = False


    def __init__(self, label, id, entryPoint=False, exitPoint=False):
        self.__label = label
        self.__id = id
        self.__entryPoint = entryPoint
        self.__exitPoint = exitPoint

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
    
    # Setter methods
    def setID(self, id):
        self.__id = id
    
    def setLabel(self, label):
        self.__label = label
    
    def setEntryPoint(self, entryPoint):
        self.__entryPoint = entryPoint
    
    def setExitPoint(self, exitPoint):
        self.__exitPoint = exitPoint
    
    #Node flow functions

    #Adds a node to this nodes list of where it flows to
    def addNode(self, nodeID, description = ""):
        if (nodeID, description) not in self.__NodesToFlowTo:
            self.__NodesToFlowTo.append((nodeID, description))

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
        
    