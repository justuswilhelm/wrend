from abc import (
    ABCMeta,
    abstractmethod,
)
from enum import Enum
from re import sub


class NodeType(Enum):
    ELEMENT_NODE = 1
    TEXT_NODE = 3
    PROCESSING_INSTRUCTION_NODE = 7
    COMMENT_NODE = 8
    DOCUMENT_NODE = 9
    DOCUMENT_TYPE_NODE = 10
    DOCUMENT_FRAGMENT_NODE = 11


class Node(metaclass=ABCMeta):
    node_name = None
    node_type = None
    parent_node = None
    child_nodes = None
    node_value = None
    attributes = None

    @abstractmethod
    def __init__(self, node_name, node_type, node_value=None, attributes=None):
        self.node_name = node_name
        self.node_type = node_type
        self.node_value = node_value
        self.child_nodes = []
        self.attributes = dict(attributes or [])

    def append_child(self, node):
        self.child_nodes.append(node)
        node.parent_node = self

    @property
    def first_child(self):
        return self.child_nodes[0]

    @property
    def last_child(self):
        return self.child_nodes[-1]

    @property
    def previous_sibling(self):
        # TODO
        pass

    @property
    def next_sibling(self):
        # TODO
        pass

    def __str__(self):
        return ", ".join(map(repr, filter(lambda e: e, [
            self.node_name, self.node_value, self.attributes])))

    def pprint(self, level=0, indent="  "):
        current_indent = indent * level
        print("{}{}".format(current_indent, self))

        for child_node in self.child_nodes:
            child_node.pprint(level + 1)


class DocumentNode(Node):

    body = None
    head = None

    def __init__(self, child_nodes=None):
        super().__init__(
            '#document',
            NodeType.DOCUMENT_NODE,
        )


class ElementNode(Node):
    def __init__(self, node_name, attributes=None):
        super().__init__(
            node_name,
            NodeType.ELEMENT_NODE,
            attributes=attributes,
        )

    def get_elements_by_tag_name(self, tag_name):
        result = []
        for child_node in self.child_nodes:
            child_node.get_elements_by_tag_name(tag_name)
        return result

    def get_children(self):
        result = []
        for child_node in self.child_nodes:
            if isinstance(child_node, TextNode) and child_node.whole_text():
                result.append(child_node)
            else:
                result.append(child_node)


class TextNode(Node):
    WHITESPACE_RE = r'\s+'

    def __init__(self, node_value):
        super().__init__(
            '#text', NodeType.TEXT_NODE,
            node_value=node_value,
        )

    @property
    def whole_text(self):
        data = sub(self.WHITESPACE_RE, ' ', self.node_value)
        if data != ' ':
            return data


class CommentNode(Node):
    def __init__(self, node_value):
        super().__init__(
            "#comment",
            NodeType.COMMENT_NODE,
            node_value=node_value,
        )


class ProcessingInstructionNode(Node):
    def __init__(self, node_value):
        super().__init__(
            "#pi",  # XXX node_value is not #pi
            NodeType.PROCESSING_INSTRUCTION_NODE,
            node_value=node_value,
        )


class DocumentTypeNode(Node):
    def __init__(self, decl):
        super().__init__(
            decl,
            NodeType.DOCUMENT_TYPE_NODE,
        )
