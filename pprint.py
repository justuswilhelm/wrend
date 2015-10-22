def pprint(node, level=0, indent="  "):
    current_indent = indent * level
    try:
        print("{}<{}>".format(current_indent, node.name))

        for child_node in node.nodes:
            pprint(child_node, level + 1)

        print("{}</{}>".format(indent * level, node.name))
    except AttributeError:
        print("{}{}".format(current_indent, node.data))
