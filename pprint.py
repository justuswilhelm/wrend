def pprint(node, level=0, indent="  "):

    current_indent = indent * level
    print("{}{}".format(current_indent, node))

    for child_node in node.child_nodes:
        pprint(child_node, level + 1)
