from PIL import Image, ImageDraw


from .dom import TextNode


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
        'overflowed',
        'text',
    ]

    def __init__(self, node):
        self.node = node
        self.style = Style()
        self.overflowed = False

        self.text = ''
        if isinstance(self.node, TextNode):
            self.text = self.node.whole_text

        if self.node.node_name in self.BLOCK_NODES:
            self.style.display = 'block'
        else:
            self.style.display = 'inline'

        self.child_frames = [
            self.__class__(child_node) for child_node in self.node.child_nodes
        ]

        self.x = self.y = self.w = self.h = 0

    def reflow(self):
        if self.text:
            self.w = len(self.text) * 6
            self.h = 20

        for child_frame in self.child_frames:
            child_frame.x = self.x + self.w
            child_frame.reflow()
            self.w += child_frame.w
            self.h = max(self.h, child_frame.h)

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
        if self.text:
            draw.text((self.x, self.y), self.text)

        for child_frame in self.child_frames:
            child_frame._draw(draw, level=level + 1)
