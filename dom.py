from abc import (
    ABCMeta,
    abstractmethod,
)
from enum import Enum


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
    attributes = {}

    @abstractmethod
    def __init__(self, node_name, node_type, parent_node=None,
                 child_nodes=None, node_value=None,
                 attributes=None):
        self.node_name = node_name
        self.node_type = node_type
        self.parent_node = parent_node
        self.child_nodes = child_nodes or []
        self.node_value = node_value
        self.attributes = dict(attributes or [])

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
        return ", ".join(map(str, filter(lambda e: e, [
            self.node_name, self.node_value, self.attributes])))

    def pprint(self, level=0, indent="  "):
        current_indent = indent * level
        print("{}{}".format(current_indent, self))

        for child_node in self.child_nodes:
            child_node.pprint(level + 1)


class DocumentNode(Node):

    body = None
    head = None

    def __init__(self):
        super().__init__('#document', NodeType.DOCUMENT_NODE)


class ElementNode(Node):
    def __init__(self, node_name, attributes=None, parent_node=None):
        super().__init__(
            node_name,
            NodeType.ELEMENT_NODE,
            attributes=attributes,
            parent_node=parent_node,
        )


class TextNode(Node):
    def __init__(self, node_value, parent_node=None):
        super().__init__(
            '#text', NodeType.TEXT_NODE,
            node_value=node_value,
            parent_node=parent_node,
        )


class CommentNode(Node):
    def __init__(self, node_value, parent_node=None):
        super().__init__(
            "#comment",
            NodeType.COMMENT_NODE,
            node_value=node_value,
            parent_node=parent_node)


class ProcessingInstructionNode(Node):
    def __init__(self, node_value, parent_node=None):
        super().__init__(
            "#pi",  # XXX node_value is not #pi
            NodeType.PROCESSING_INSTRUCTION_NODE,
            node_value=node_value,
            parent_node=parent_node,
        )


class DocumentTypeNode(Node):
    def __init__(self, decl, parent_node=None):
        super().__init__(
            decl,
            NodeType.DOCUMENT_TYPE_NODE,
            parent_node=parent_node,
        )
