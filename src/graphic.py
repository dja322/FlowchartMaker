import tkinter as tk
import math

class graphicManager:
    tiles = []
    textTiles = []
    c = None
    root = None

    # Function to destroy the button using its ID
    def clear_widgets(self):
        if self.c is not None:
            self.c.delete("all")

    #reinitializes Arrays, not good I know
    def reinitializeArrays(self, NodeList):
        listSize = len(NodeList)
        if listSize < 1:
            listSize = 1
        #INITIALIZE ARRAY FOR GRAPHIC
        empty_row = [-1] * listSize
        self.tiles = [empty_row.copy() for _ in range(listSize)]
        self.textTiles = [empty_row.copy() for _ in range(listSize)]

    def initWindow(self, ROWHEIGHT, COLHEIGHT, NodeList):
        #INITIALIZES TKINTER STUFF
        self.root = tk.Tk()
        self.root.geometry(f"{ROWHEIGHT}x{COLHEIGHT}")
        tk.Button(self.root, text="Quit", command=self.root.destroy).pack()
        listSize = len(NodeList)
        if listSize < 1:
            listSize = 1

        self.reinitializeArrays(NodeList)

        #initialize tKinter Canvas
        self.c = tk.Canvas(
            self.root, width=ROWHEIGHT, height=COLHEIGHT, 
            borderwidth=0, background='white')
        #pack Canvas
        self.c.pack()

        #Create graphic constants
        OFFSET = 5
        col_width = COLHEIGHT/listSize
        row_height = ROWHEIGHT/listSize

        #positions nodes
        x_position: int = 0
        y_position: int = 0
        for node in NodeList:
            x1 = x_position*col_width
            y1 = y_position*row_height
            x2 = (x_position+1)*col_width
            y2 = (y_position+1)*row_height
            self.tiles[x_position][y_position] = self.c.create_oval(
                                    x1 + OFFSET, y1 + OFFSET,
                                    x2 - OFFSET, y2 - OFFSET,
                                    fill=node.getColor())
            
            self.textTiles[x_position][y_position] = self.c.create_text(
                (x1 + x2) / 2, (y1 + y2) / 2, text=f"ID:{node.getID()}\nLabel:{node.getLabel()}")
            
            x_position += 1
            if (x_position >= listSize):
                x_position = 0
                y_position += 1
        
        #yield root, tiles, textTiles
        #run display
        self.root.mainloop()

    def updateGraphic(self, ROWHEIGHT, COLHEIGHT, NodeList):
        #ensures no crashes from self.c being nothing
        if (self.c == None):
            return
        
        nodeLocations = []
        listSize = len(NodeList)
        if listSize < 1:
            listSize = 1

        #sets dimensions and clears all widgets
        self.reinitializeArrays(NodeList)
        self.clear_widgets()
        
        #Create graphic constants
        OFFSET = 5
        width = COLHEIGHT
        height = ROWHEIGHT
        center_x = width / 2
        center_y = height / 2
        radius = min(width, height) / 2.5  # Keep nodes inside the canvas

        # Place nodes in a circular layout
        for i, node in enumerate(NodeList):
            angle = (2 * math.pi / listSize) * i
            # Compute node center position
            node_x = center_x + radius * math.cos(angle)
            node_y = center_y + radius * math.sin(angle)
            node_radius = 80  # Size of node circles

            # Draw node circle
            self.tiles[i][0] = self.c.create_oval(
                node_x - node_radius + OFFSET,
                node_y - node_radius + OFFSET,
                node_x + node_radius - OFFSET,
                node_y + node_radius - OFFSET,
                fill=node.getColor()
            )

            # Draw text label
            self.textTiles[i][0] = self.c.create_text(
                node_x, node_y,
                text=f"ID:{node.getID()}\nLabel:{node.getLabel()}"
            )

            # Store location for connection lines
            nodeLocations.append([node, node_x, node_y])

        # Draw connection arrows
        for nodeLoc in nodeLocations:
            connections = nodeLoc[0].getCopyOfConnections()
            for connection in connections:
                loc = next((sub for sub in nodeLocations if connection[0] == nodeLoc[0].getID()), None)
                if (loc != None):
                    x1 = loc[1]
                    y1 = loc[2] + node_radius
                    x2 = nodeLoc[1]
                    y2 = nodeLoc[2] + node_radius
                    self.c.create_line(x1, y1, x2, y2, width=5, arrow=tk.LAST, fill=connection[1])

        self.c.pack()
    
