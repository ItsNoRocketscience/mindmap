class Network():
    """
    Class definition of MindMap-Network
    """
    def __init__(self):
        self.master = None
        self.entries = []
        self.connections = []

    def draw(self, canvas):
        self.master.draw()

class Element():
    """
    Class definition of MindMap-Element
    """
    def __init__(self, master, pos, s, size, color='black'):
        self.master = master
        self.pos = pos
        self.string = s
        self.size = size
        self.color = color
        self.children = []

    def draw(self, canvas):
        """
        Draw Element on canvas
        """
        canvas.create_oval(pos[0]-self.size, pos[1]-self.size,
                           pos[0]+self.size, pos[1]+self.size, fill=self.color)

        for element in self.children:
            element.draw()
            # ToDo: Add connection
