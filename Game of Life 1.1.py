from tkinter import *
from tkinter import filedialog
import time
import json

#Grid code from Arthur Vaisse @ Stack Overflow
class Cell():
    FILLED_COLOR_BG = "black"
    EMPTY_COLOR_BG = "white"
    FILLED_COLOR_BORDER = "black"
    EMPTY_COLOR_BORDER = "black"

    def __init__(self, master, x, y, size):
        """ Constructor of the object called by Cell(...) """
        self.master = master
        self.abs = x
        self.ord = y
        self.size= size
        self.fill= False

    def _switch(self):
        """ Switch if the cell is filled or not. """
        self.fill= not self.fill

    def draw(self):
        """ order to the cell to draw its representation on the canvas """
        if self.master != None :
            fill = Cell.FILLED_COLOR_BG
            outline = Cell.FILLED_COLOR_BORDER

            if not self.fill:
                fill = Cell.EMPTY_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER

            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = fill, outline = outline)

class CellGrid(Canvas):
    def __init__(self,master, rowNumber, columnNumber, cellSize, *args, **kwargs):
        Canvas.__init__(self, master, width = cellSize * columnNumber , height = cellSize * rowNumber, *args, **kwargs)

        self.cellSize = cellSize

        self.grid = []
        for row in range(rowNumber):

            line = []
            for column in range(columnNumber):
                line.append(Cell(self, column, row, cellSize))

            self.grid.append(line)

        #memorize the cells that have been modified to avoid many switching of state during mouse motion.
        self.switched = []

        #bind click action
        self.bind("<Button-1>", self.handleMouseClick)  
        #bind moving while clicking
        self.bind("<B1-Motion>", self.handleMouseMotion)
        #bind release button action - clear the memory of midified cells.
        self.bind("<ButtonRelease-1>", lambda event: self.switched.clear())

        self.draw()



    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()

    def _eventCoords(self, event):
        row = int(event.y / self.cellSize)
        column = int(event.x / self.cellSize)
        return row, column

    def handleMouseClick(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]
        cell._switch()
        cell.draw()
        #add the cell to the list of cell switched during the click
        self.switched.append(cell)

    def handleMouseMotion(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]

        if cell not in self.switched:
            cell._switch()
            cell.draw()
            self.switched.append(cell)

            
#Game of Life Code Begins Here
def invert(grid):
    for i in grid.grid:
        for j in i:
            j._switch()
            j.draw()
    grid.update()
        
def clear(app, grid):
    #Get Current Height and Width from grid list
    height = len(grid.grid)
    width = len(grid.grid[0]) #The length of the row (width) within the column list
    for i in grid.grid:
        for j in i:
            j.fill = False
            j.draw()
    grid.update()
    reset(app, height, width)

def printout(grid):
    gridlist = {}
    for i in grid.grid:
        for j in i:
            gridlist[j.abs, j.ord] = j.fill
    #for i in gridlist:
    #        print(i,gridlist[i])
    fout = filedialog.asksaveasfile(mode='w', defaultextension=".txt", initialdir = "C:\\", title = "Select file", filetypes = (("Text files","*.txt"),("all files","*.*")))
    gridlist_new = dict([(str(i),j) for i,j in gridlist.items()])
    fout.write(json.dumps(gridlist_new))
    fout.close()

def importsc(grid):
    fin = filedialog.askopenfilename(defaultextension=".txt", initialdir = "C:\\", title = "Select file", filetypes = (("Text files","*.txt"),("all files","*.*")))
    with open(fin, 'r') as f:
        data = json.load(f)
        newdict = dict([(eval(str(i)),j) for i,j in data.items()])
    #for i in newdict:
     #   print(i,newdict[i])
    for i in grid.grid:
        for j in i:
            if (j.abs, j.ord) in newdict:
                j.fill = newdict[(j.abs, j.ord)]
                j.draw()
    grid.update()

def create_window(app):
    window = Toplevel(app)
    label2 = Label(window, text="Settings").grid(row=1, column=1)
    label3 = Label(window, text='Height of Grid').grid(row=2, column=1)
    height = Entry(window)
    height.grid(row=2, column=2)
    height.insert(0,25)
    label4 = Label(window, text="Width of Grid").grid(row=3, column=1)
    width = Entry(window)
    width.grid(row=3, column=2)
    width.insert(0,25)
    button6 = Button(window, text="Accept and Reset", command= lambda : reset(app, height.get(), width.get())).grid(row=4, column=1)
    
def reset(app, height=None, width=None):
    height = int(height)
    width = int(width)
    app.destroy()
    main(height, width)
    
def gameoflife(grid, lgt):
    len = int(lgt.get())
    for l in range(len):
        indices = {}
        for i in grid.grid:
            for j in i:
                live = 0
                pos = i.index(j)
                try:
                    up = grid.grid[grid.grid.index(i)-1]
                    down = grid.grid[grid.grid.index(i)+1]
                    topl = up[pos-1]
                    top = up[pos]
                    topr = up[pos+1]
                    left = i[pos-1]
                    right = i[pos+1]
                    botl = down[pos-1]
                    bot = down[pos]
                    botr = down[pos+1]
                except:
                    pass
                if topl.fill == True:
                    live+=1
                if top.fill == True:
                    live+=1
                if topr.fill == True:
                    live+=1
                if left.fill == True:
                    live+=1
                if right.fill == True:
                    live+=1
                if botl.fill == True:
                    live+=1
                if bot.fill == True:
                    live+=1
                if botr.fill == True:
                    live+=1
                indices[(j.abs, j.ord)] = live
                #Store variable live and assign to index value, dictionary?
                #Calculate in second for loop
        for i in grid.grid:
            for j in i:
                live = indices[(j.abs, j.ord)]
                if j.fill == True and live == 2 or live == 3:
                    pass
                if j.fill == True and live<2:
                    j.fill = False
                if j.fill == True and live>3:
                    j.fill = False
                if j.fill == False and live == 3:
                    j.fill = True
                j.draw()
        grid.update()
        grid.delete(ALL)
    invert(grid)
    invert(grid)
    
def main(height,width):
    app = Tk()
    grid = CellGrid(app, height, width, 10)
    button_frame = Frame(app)
    button_frame.pack(side="bottom", expand=False)
    button = Button(button_frame, text="Commence Game of Life!", command=lambda : gameoflife(grid, lgt))
    button2 = Button(app, text='Clear Grid', command = lambda : clear(app, grid))
    button3 = Button(button_frame, text="Export Schematic", command = lambda : printout(grid))
    button4 = Button(button_frame, text='Import Schematic', command = lambda : importsc(grid))
    button5 = Button(button_frame, text='Settings', command = lambda : create_window(app))
    label = Label(button_frame, text="Number of Iterations").grid(row=2, column=1)
    lgt = Entry(button_frame)
    grid.pack()
    button.grid(row=1, column=1)
    button2.pack()
    button3.grid(row=2, column=3)
    button4.grid(row=1, column=3)
    button5.grid(row=3, column=2)
    lgt.grid(row=2, column=2)
    app.mainloop()
    
if __name__ == "__main__":
    defheight = 25
    defwidth = 25
    main(defheight,defwidth)
