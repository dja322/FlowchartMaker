
import src.node as node
import src.graphic as graphic
import threading
import ast

tkinter_unique_colors = [
    'aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black',
    'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse',
    'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue',
    'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki',
    'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon',
    'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise',
    'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick',
    'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod',
    'gray', 'green', 'greenyellow', 'grey', 'honeydew', 'hotpink', 'indianred', 'indigo',
    'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue',
    'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightgrey',
    'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray',
    'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta',
    'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple',
    'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise',
    'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite',
    'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod',
    'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink',
    'plum', 'powderblue', 'purple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon',
    'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue',
    'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle',
    'tomato', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen'
]


updateFunction = None
g_manager = graphic.graphicManager()

def updateGraphics(nodes: list[node.Node]) -> None:
    g_manager.updateGraphic(Rowheight, Colheight, nodes)

def runInterface(ROWHEIGHT: int, COLHEIGHT: int) -> None:
    #initialize graphic variables
    global Rowheight, Colheight
    Rowheight = ROWHEIGHT
    Colheight = COLHEIGHT

    #run graphics in separate thread
    t1 = threading.Thread(target=cmdInterface, args=())
    #starts threads
    t1.start()

    g_manager.initWindow(Rowheight, Colheight)

def cmdInterface() -> None:
    nodeList = []

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
            verbose = input("Verbose print? (y/n): ").lower()
            if (verbose == 'y'):
                for node in nodeList:
                    print(f"{node}, Connections: {node.getCopyOfConnections()}, \
EntryPoint: {node.getEntryPoint()} Exitpoint: {node.getExitPoint()}\n")
            else:
                for node in nodeList:
                    print(f"({node}), ", end='')
        elif command == "6":
            for i, color in enumerate(tkinter_unique_colors):
                print(color, end=', ')
                if (i % 5 == 1):
                    print()
        elif command == '7':
            result = saveloadNodeList(nodeList=nodeList)
            if (result != None):
                nodeList = result
        elif command == "8" or command == "exit":
            break
        else:
            print("Invalid Command")

        #updates the graphics
        updateGraphics(nodeList)


#Menu function
def printMenu() -> None:
    print("""
--- MAIN MENU ---
1. Add Node
2. Add Connections to Node
3. Remove Connections to Node
4. Remove Node
5. Print Nodes
6. See Full List of valid colors(147 colors)
7. Save/Load flowchart
8. Exit
""")

#load or save node list
def saveloadNodeList(nodeList: list[node.Node]) -> list[node.Node] | None:
    option = input("Please enter 'S' for save or 'L' for load: ").lower()
    #Save nodelist to user file
    if (option == 's'):
        option = input("Enter filename to save to: ")
        with open(option, 'w') as f:
            for inNode in nodeList:
                f.write(inNode.fileString() + '\n')
        return None
    #Load nodeList from inputted file
    elif(option == 'l'):
        option = input("Enter filename to load from: ")
        loadedNodeList: list = []
        try:
            with open(option, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    parsedLine = parseLoadString(line)
                    if (parsedLine != None):
                        id, label, color, entrypoint, exitpoint, connections = parsedLine
                        newNode = node.Node(id, label, color, entrypoint, exitpoint)
                        for connection in connections:
                            newNode.addNode(connection[0], connection[1])
                        loadedNodeList.append(newNode)
            return loadedNodeList

        except FileNotFoundError:
            print("File not found")
    else:
        print("Invalid option")
    return None
    
def parseLoadString(string: str) -> tuple | None:
    try:
        # Safely evaluate the string as a Python literal
        parsed = ast.literal_eval(string)

        # Basic structure validation
        if not isinstance(parsed, tuple) or len(parsed) != 6:
            raise ValueError("Input must be a tuple of length 6.")

        id, label, color, entrypoint, exitpoint, connection = parsed

        # Type checking
        if not all(isinstance(x, str) for x in (id, label, color)):
            raise TypeError("First three elements must be strings.")
        if not all(isinstance(x, bool) for x in (entrypoint, exitpoint)):
            raise TypeError("Fourth and fifth elements must be booleans.")
        if not isinstance(connection, list) or not all(isinstance(t, tuple) for t in connection):
            raise TypeError("Sixth element must be a list of tuples.")

        return parsed

    except Exception as e:
        print("Error loading file, invalid format")
        return None
 
#checks if id is present in node list
def checkNodeListForID(nodeList: list[node.Node], id: str) -> bool:
    result = next((sub for sub in nodeList if id == sub.getID()), None)
    if result == None:
        return True
    return False
    
#adds a unique node to node list
def addNode(nodeList: list[node.Node]) -> node.Node:
    print("Enter 'exit' to return to main menu")
    id = input("\nNew node ID: ")
    label = ''
    color = 'gray'
    entryPointInput = 'n'
    exitPointInput = 'n'
    entryPoint = False
    exitPoint = False
    if (id != 'exit'):
        label = input("New node Label: ")
        color = input("Color: ")
        entryPointInput = input("Is Entry Point? (y/n): ").lower()
        exitPointInput = input("Is Exit Point? (y/n): ").lower()

    while id != 'exit' and not checkNodeListForID(nodeList, id):
        print("Duplicate ID")
        id = input("\nID: ")
        label = input("Label: ")
        color = input("Color: ")
        entryPointInput = input("Is Entry Point? (y/n): ").lower()
        exitPointInput = input("Is Exit Point? (y/n): ").lower()

    if (entryPointInput == 'y'):
        entryPoint = True
    if (exitPointInput == 'y'):
        exitPoint = True

    return node.Node(id=id, label=label, color=color, entryPoint=entryPoint, exitPoint=exitPoint)

#add connection between two nodes
def addConnection(nodeList: list[node.Node]) -> None:
    nodeID = ""
    srcNode = None
    print("Enter 'exit' to return to main menu")
    
    while nodeID != 'exit':
        nodeID = input("\nSource Node ID: ")
        srcNode = next((sub for sub in nodeList if nodeID == sub.getID()), None)

        #check if there is a node matching ID
        if (srcNode == None): #If no node ask again
            if (nodeID != 'exit'):
                print("Invalid ID, no node found")
        else: #ask for new node connection
            while nodeID != 'exit':
                nodeID = input("Destination Node ID: ")
                if (nodeID == 'exit'):
                    break
                result = next((sub for sub in nodeList if nodeID == sub.getID()), None)
                if (result == None):
                    print("\nInvalid ID, no node found")
                else:
                    Color = input("Connection Color: ")
                    srcNode.addNode(nodeID, Color)
                    print("New Connection added")
                    print("\nAdd more connections or enter 'exit'")
                    updateGraphics(nodeList)

#Remove connection between two nodes
def removeConnection(nodeList: list[node.Node]) -> None:
    nodeID = ""
    result = None
    print("Enter 'exit' to return to main menu")
    
    while nodeID != 'exit':
        nodeID = input("\nSource Node ID: ")
        result = next((sub for sub in nodeList if nodeID == sub.getID()), None)

        if (result == None):
            print("Invalid ID, no node found")
        else:
            while nodeID != 'exit':
                nodeID = input("\nRemove connection Node ID: ")
                result = next((sub for sub in nodeList if nodeID == sub.getID()), None)
                if (result == None):
                    print("Invalid ID, no node found")
                else:
                    result.deleteConnection(nodeID)
                    updateGraphics(nodeList)

def removeNode(nodeList: list[node.Node]) -> None:
    nodeID = ""
    result = None
    print("Enter 'exit' to return to main menu")
    
    while nodeID != 'exit':
        nodeID = input("\nNode to delete ID: ")
        result = next((sub for sub in nodeList if nodeID == sub.getID()), None)

        if (result == None):
            print("Invalid ID, no node found")
        else:
            deleteID = result.getID()

            for node in nodeList:
                node.deleteConnection(deleteID, print_removal=False)
            nodeList.remove(result)
            updateGraphics(nodeList)
            break

