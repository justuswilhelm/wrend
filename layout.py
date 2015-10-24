from PIL import Image, ImageDraw


class Style:

    __slots__ = [
        'display',
    ]

    def __init__(self, **kwargs):
        for slot in self.__slots__:
            if slot in kwargs:
                setattr(self, slot, kwargs[slot])


class Frame:

    BLOCK_NODES = [
        'P',
        'DIV',
        'BODY',
        'H1',
        'H2',
        'H3',
        'H4',
        'H5',
        'H6',
        'HEADER',
        'UL',
        'LI',
    ]

    __slots__ = [
        'node',
        'style',
        'w',
        'h',
        'x',
        'y',
        'child_frames',
    ]

    def __init__(self, node):
        self.node = node
        self.style = Style()

        if self.node.node_name in self.BLOCK_NODES:
            self.style.display = 'block'
        else:
            self.style.display = 'inline'

        self.child_frames = [
            self.__class__(child_node) for child_node in node.child_nodes
        ]

        self.x = self.y = self.w = self.h = 0

    def reflow(self, container_width, container_height,
               container_x=0, container_y=0):
        self.w = container_width
        self.h = container_height
        self.x = container_x
        self.y = container_y

        if self.style.display == 'inline':
            required_width = len(self.node.node_value or "") * 10  # ??
            required_height = 20 if self.node.node_value else 0
        else:
            required_width = 0
            required_height = 0

        for child_frame in self.child_frames:
            child_width, child_height = child_frame.reflow(
                self.w, self.h, self.x, self.y)
            if child_frame.style.display == 'inline':
                self.x += child_width
            else:
                self.y += child_height

            required_width += child_width
            required_height += child_height

        if self.x + required_width > container_width:
            self.x = container_x
            self.y += required_height

        self.w = required_width
        self.h = required_height

        return required_width, required_height

    def __str__(self):
        return "{self.style.display}: {self.node}".format(self=self)

    def pprint(self):
        print("{}x{}, size {}x{}: {}".format(
            self.x, self.y, self.w, self.h,
            self,
        ))

        for child_frame in self.child_frames:
            child_frame.pprint()

    def draw(self):
        # set up dat window
        i = Image.new('RGBA', (self.w, self.h))
        draw = ImageDraw.Draw(i)
        self._draw(draw)
        i.save("helloworld.png")

    def _draw(self, draw, level=0):
        draw.rectangle(
            (self.x, self.y, self.w + self.x, self.h + self.y),
            fill='green',
            outline='red',
        )
        draw.text(
            (self.x, self.y),
            self.node.node_value or self.node.node_name)

        for child_frame in self.child_frames:
            child_frame._draw(draw, level=level + 1)
