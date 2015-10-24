from pyx import *


class Frame:

    BLOCK_NODES = [
        'P',
        'DIV',
        'BODY',
    ]

    BLOCK = 0
    INLINE = 1
    INLINE_BLOCK = 2

    __slots__ = [
        'node',
        'display',
        'w',
        'h',
        'x',
        'y',
        'child_frames',
    ]

    def __init__(self, node):
        self.node = node

        if self.node.node_name in self.BLOCK_NODES:
            self.display = self.BLOCK
        else:
            self.display = self.INLINE

        self.child_frames = [
            self.__class__(child_node) for child_node in node.child_nodes
        ]

        self.x = self.y = self.w = self.h = 0

    def reflow(self, w, h, x=0, y=0):
        self.w = w
        self.h = h
        self.x = x
        self.y = y

        if self.display == self.INLINE:
            required_width = 100  # ??
            required_height = 20
        else:
            required_width = w
            required_height = h

        for child_frame in self.child_frames:
            child_width, child_height = child_frame.reflow(w, h, x, y)
            if child_frame.display == self.INLINE:
                x += child_width
            else:
                y += child_height

            required_width += child_width
            required_height += child_height

        self.w = required_width
        self.h = required_height

        return required_width, required_height

    def __str__(self):
        if self.display == self.BLOCK:
            return "BLOCK: {}".format(self.node)
        else:
            return "INLINE: {}".format(self.node)

    def pprint(self):
        print("{}x{}, size {}x{}: {}".format(
            self.x, self.y, self.w, self.h,
            self,
        ))

        for child_frame in self.child_frames:
            child_frame.pprint()

    def draw(self):
        # set up dat window
        c = canvas.canvas()

        self._draw(c)
        c.writePDFfile()

    def _draw(self, c):
        c.stroke(path.rect(
            self.x,
            self.y,
            self.w,
            self.h,
        ))
        for child_frame in self.child_frames:
            child_frame._draw(c)
