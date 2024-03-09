import requests
from settings import db

def fetch_ast():
    url = "http://localhost:8080//processing-service/process-code/rust"

    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            print("Data:", data)
            db.session.add(data)
            db.session.commit()
            return data

        else:
            print(f"Failed to fetch AST: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(e)
        return None



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

