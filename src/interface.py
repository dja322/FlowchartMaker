
import src.node as node
import src.graphic as graphic
import threading

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

def updateGraphics(nodes):
    g_manager.updateGraphic(Rowheight, Colheight, nodes)

def cmdInterface(ROWHEIGHT, COLHEIGHT):
    print(len(tkinter_unique_colors))
    nodeList = []

    global Rowheight, Colheight
    Rowheight = ROWHEIGHT
    Colheight = COLHEIGHT

    #initialize graphic variables
    
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
                print(f"({node}), ", end='')
        elif command == "6":
            for i, color in enumerate(tkinter_unique_colors):
                print(color, end=', ')
                if (i % 5 == 1):
                    print()
        elif command == "7" or command == "exit":
            break
        else:
            print("Invalid Command")

        #updates the graphics
        updateGraphics(nodeList)

    t1.join()

#Menu function
def printMenu():
    print("""
--- MAIN MENU ---
1. Add Node
2. Add Connections to Node
3. Remove Connections to Node
4. Remove Node
5. Print Nodes
6. See Full List of valid colors(147 colors)
7. Exit
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
    id = input("\nNew node ID: ")
    label = ''
    color = 'gray'
    if (id != 'exit'):
        label = input("New node Label: ")
        color = input("Color: ")

    while id != 'exit' and not checkNodeListForID(nodeList, id):
        print("Duplicate ID")
        id = input("\nID: ")
        label = input("Label: ")
        color = input("Color: ")

    return node.Node(id, label, color)

#add connection between two nodes
def addConnection(nodeList):
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
def removeConnection(nodeList):
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

def removeNode(nodeList):
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

