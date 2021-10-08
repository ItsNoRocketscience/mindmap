import json


class Network:
    """
    Class definition of MindMap-Network
    """

    def __init__(self):
        self.master = None
        self.elements = []
        self.connections = []

    def draw(self, canvas):
        self.master.draw(canvas)

    def add_master(self, pos, s, fill_color='black', **kwargs):
        """
        Add Master element to network
        :param pos: Position Tuple
        :param s: String
        :param fill_color: Fill color, default: 'black'
        :return: Nothing
        """
        self.master = Element(None, pos, s, fill_color, **kwargs)
        self.elements.append(self.master)

    def add_element(self, parent, pos, s, **kwargs):
        """
        Add new element to network
        :param parent: Element object as parent
        :param pos: Position tuple
        :param s: String
        :param kwargs: Other keyword arguments
        :return: Nothing
        """
        self.elements.append(Element(parent, pos, s, **kwargs))

    def save(self, file_path):
        """
        Save Network to json file
        :param file_path:
        :return: Nothing
        """
        if self.master is None:
            return

        data = {'master': self.master.to_json()}
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=True, indent=4)

    @classmethod
    def from_json(cls, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        network = cls()
        network.master = Element.from_json(data['master'])
        network.master.add_to_list(network.elements)
        return network


class Element:
    """
    Class definition of MindMap-Element
    """

    def __init__(self, parent, pos, s, fill_color='black',
                 font=('Purisa', 12), text_color='white'):
        self.parent = parent
        self.pos = pos
        self.s = s
        self.shape_size = ()
        self.fill_color = fill_color
        self.font = font
        self.text_color = text_color
        self.children = []
        self.shape = None
        self.text = None
        self.line = None
        self.highlighted = False
        if self.parent is not None:
            self.parent.children.append(self)

    def draw(self, canvas):
        """
        Draw Element on canvas
        """
        # Draw Text
        if self.text is None:
            self.text = canvas.create_text(
                *self.pos, text=self.s,
                fill=self.text_color, font=self.font)
        # Draw Shape
        if self.shape is None:
            bounds = canvas.bbox(self.text)
            x_size = (bounds[2] - bounds[0]) // 2
            y_size = (bounds[3] - bounds[1]) // 2
            if x_size / y_size > 4:
                self.shape_size = (x_size * 1.2, y_size * 1.5)
            else:
                self.shape_size = (max(x_size, y_size), max(x_size, y_size))
            self.shape = canvas.create_oval(
                self.pos[0] - self.shape_size[0], self.pos[1] - self.shape_size[1],
                self.pos[0] + self.shape_size[0], self.pos[1] + self.shape_size[1],
                fill=self.fill_color, width=4, outline=self.fill_color)
            canvas.tag_lower(self.shape)
        # Create connection
        if self.parent is not None and self.line is None:
            self.line = canvas.create_line(
                *self.parent.pos, *self.pos, fill='black')
            canvas.tag_lower(self.line)
        # Draw children
        for element in self.children:
            element.draw(canvas)

    def switch_highlight(self, canvas):
        self.highlighted = not self.highlighted
        if self.highlighted:
            canvas.itemconfigure(self.shape, outline='red')
        else:
            canvas.itemconfigure(self.shape, outline=self.fill_color)

    def to_json(self):
        """
        Save Object to json dictionary
        :return: data dictionary
        """
        data = {'pos': self.pos, 's': self.s, 'fill_color': self.fill_color,
                'font': self.font, 'text_color': self.text_color, 'children': []}
        for element in self.children:
            data['children'].append(element.to_json())

        return data

    @classmethod
    def from_json(cls, data, parent=None):
        """
        Create Element object from json dictionary
        :param data: Data dictionary
        :param parent: Parent object; default: None for master node
        :return: element
        """
        element = cls(parent, **{key: data[key] for key in data.keys() if not key == 'children'})
        for child in data['children']:
            element.children.append(Element.from_json(child, element))

        return element

    def add_to_list(self, el_list):
        """
        Recursive Function to add elements and children to list
        :param el_list: List of elements
        :return: Nothing
        """
        el_list.append(self)
        for element in self.children:
            element.add_to_list(el_list)
