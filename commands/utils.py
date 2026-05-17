import json

def cargar_autoroles():
    try:
        with open('autoroles.json', 'r') as f:
            return json.load(f)
    except:
        return {}

def guardar_autoroles(data):
    with open('autoroles.json', 'w') as f:
        json.dump(data, f, indent=4)
