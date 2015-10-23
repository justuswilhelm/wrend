class Node:

    ELEMENT_NODE = 1
    TEXT_NODE = 3
    PROCESSING_INSTRUCTION_NODE = 7
    COMMENT_NODE = 8
    DOCUMENT_NODE = 9
    DOCUMENT_TYPE_NODE = 10
    DOCUMENT_FRAGMENT_NODE = 11

    __slots__ = [
        'node_name',
        'node_value',
        'node_type',
        'child_nodes',
        'parent_node',
        'attributes',
    ]

    def __init__(self, node_name, node_type, parent_node=None,
                 child_nodes=None, node_value=None,
                 attributes=None):
        self.node_name = node_name
        self.node_type = node_type
        self.parent_node = parent_node
        self.child_nodes = child_nodes or []
        self.node_value = node_value
        self.attributes = {} if not attributes else dict(attributes)

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
