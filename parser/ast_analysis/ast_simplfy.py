def simplify_ast(node, parent_type=None):
    simplified_node = {}

    if isinstance(node, str):
        return node

    if isinstance(node, dict):

        node_type = node.get('name')
        simplified_node['type'] = node_type
        simplified_node['parentType'] = parent_type


        children = []
        for key, value in node.items():
            if key != 'name':  
                child = simplify_ast(value, parent_type=node_type) 
                if child:  # Only add if the child is not empty.
                    children.append(child)
        if children:
            simplified_node['children'] = children

    
    elif isinstance(node, list):
        return [simplify_ast(item, parent_type=parent_type) for item in node]

    return simplified_node


