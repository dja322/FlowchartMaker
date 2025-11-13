import tkinter as tk
import math

class graphicManager:
    tiles: list = []
    textTiles: list = []
    c: tk.Canvas | None = None
    root: tk.Tk | None = None
    node_radius: int = 80


    # Function to destroy the button using its ID
    def clear_widgets(self) -> None:
        if self.c is not None:
            self.c.delete("all")

    #reinitializes Arrays, not good I know
    def reinitializeArrays(self, NodeList: list) -> None:
        listSize = len(NodeList)
        if listSize < 1:
            listSize = 1
        #INITIALIZE ARRAY FOR GRAPHIC
        empty_row = [-1] * listSize
        self.tiles = [empty_row.copy() for _ in range(listSize)]
        self.textTiles = [empty_row.copy() for _ in range(listSize)]

    def initWindow(self, ROWHEIGHT: int, COLHEIGHT: int) -> None:
        #INITIALIZES TKINTER STUFF
        self.root = tk.Tk()
        self.root.geometry(f"{ROWHEIGHT}x{COLHEIGHT}")
        tk.Button(self.root, text="Quit", command=self.root.destroy).pack()

        #initialize tKinter Canvas
        self.c = tk.Canvas(
            self.root, width=ROWHEIGHT, height=COLHEIGHT, 
            borderwidth=0, background='white')
        #pack Canvas
        self.c.pack()

        #run display
        self.root.mainloop()

    def updateGraphic(self, ROWHEIGHT: int, COLHEIGHT: int, NodeList: list) -> None:
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

            # Draw node circle
            self.tiles[i][0] = self.c.create_oval(
                node_x - self.node_radius + OFFSET,
                node_y - self.node_radius + OFFSET,
                node_x + self.node_radius - OFFSET,
                node_y + self.node_radius - OFFSET,
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
                loc = next((sub for sub in nodeLocations if connection[0] == sub[0].getID()), None)
                if (loc != None):
                    x1 = nodeLoc[1]
                    y1 = nodeLoc[2] + self.node_radius
                    x2 = loc[1]
                    y2 = loc[2] + self.node_radius
                    self.c.create_line(x1, y1, x2, y2, width=5, arrow=tk.LAST, fill=connection[1])

        self.c.pack()
    
