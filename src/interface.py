
import src.node as node
import src.graphic as graphic
import threading

def cmdInterface():
    nodeList = []
    #initialize graphic variables
    Rowheight = 1000
    Colheight = 1000
    g_manager = graphic.graphicManager()
    
    #run graphics in separate thread
    t1 = threading.Thread(target=g_manager.initWindow, args=(Rowheight, Colheight, nodeList))
    #starts threads
    t1.start()

    while True:
        printMenu()
        command = input("> ")

        if command == "1":
            newNode = addNode(nodeList=nodeList)
            if (newNode.getID() != 'exit'):
                nodeList.append(newNode)
                print("\nNode Added")
        elif command == "2":
            addConnection(nodeList=nodeList)
        elif command == "3":
            removeConnection(nodeList=nodeList)
        elif command == "4":
            removeNode(nodeList=nodeList)
        elif command == "5":
            for node in nodeList:
                print(f"({node}), ", end=', ')
        elif command == "6" or command == "exit":
            break
        else:
            print("Invalid Command")

        #updates the graphics
        g_manager.updateGraphic(Rowheight, Colheight, nodeList)

#Menu function
def printMenu():
    print("""
--- MAIN MENU ---
1. Add Node
2. Add Connections to Node
3. Remove Connections to Node
4. Remove Node
5. Print Nodes
6. Exit
""")
    
#checks if id is present in node list
def checkNodeListForID(nodeList, id) -> bool:
    result = next((sub for sub in nodeList if id == sub.getID()), None)
    if result == None:
        return True
    return False
    
#adds a unique node to node list
def addNode(nodeList) -> node.Node:
    print("Enter 'exit' to return to main menu")
    print("\nPlease enter ID and Label for new node")
    id = input("\nID: ")
    label = input("Label: ")

    while id != 'exit' and not checkNodeListForID(nodeList, id):
        print("Duplicate ID")
        id = input("\nID: ")
        label = input("Label: ")

    return node.Node(id, label)

#add connection between two nodes
def addConnection(nodeList):
    nodeID = ""
    result = None
    print("Enter 'exit' to return to main menu")
    print("\nPlease enter ID of source Node")
    
    while nodeID != 'exit':
        nodeID = input("\nNode ID: ")
        result = next((sub for sub in nodeList if nodeID == sub.getID()), None)

        #check if there is a node matching ID
        if (result == None): #If no node ask again
            if (nodeID != 'exit'):
                print("Invalid ID, no node found")
        else: #ask for new node connection
            while nodeID != 'exit':
                print("Please enter ID of new destination Node")
                nodeID = input("\nNode ID: ")
                result = next((sub for sub in nodeList if nodeID == sub.getID()), None)
                if (result == None):
                    print("\nInvalid ID, no node found")
                else:
                    description = input("\nConnection Description: ")
                    result.addNode(nodeID, description)
                    print("\nNew Connection added")

#Remove connection between two nodes
def removeConnection(nodeList):
    nodeID = ""
    result = None
    print("Enter 'exit' to return to main menu")
    print("\nPlease enter ID of source Node")
    
    while nodeID != 'exit':
        nodeID = input("\nNode ID: ")
        result = next((sub for sub in nodeList if nodeID == sub.getID()), None)

        if (result == None):
            print("Invalid ID, no node found")
        else:
            while nodeID != 'exit':
                print("Please enter ID of destination Node to remove connection")
                nodeID = input("\nNode ID: ")
                result = next((sub for sub in nodeList if nodeID == sub.getID()), None)
                if (result == None):
                    print("Invalid ID, no node found")
                else:
                    result.deleteConnection(nodeID)

def removeNode(nodeList):
    nodeID = ""
    result = None
    print("Enter 'exit' to return to main menu")
    print("\nPlease enter ID of Node to delete")
    
    while nodeID != 'exit':
        nodeID = input("\nNode ID: ")
        result = next((sub for sub in nodeList if nodeID == sub.getID()), None)

        if (result == None):
            print("Invalid ID, no node found")
        else:
            deleteID = result.getID()

            for node in nodeList:
                node.deleteConnection(deleteID, print_removal=False)
            nodeList.remove(result)
            break

