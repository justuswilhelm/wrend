def pprint_dom(node, level=0, indent="  "):
    current_indent = indent * level
    print("{}{}".format(current_indent, node))

    for child_node in node.child_nodes:
        pprint_dom(child_node, level + 1)
