import json

def Style(filename:str):
    with open(filename, 'r') as f:
        data = json.load(f)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def Sort(filename:str):
    with open(filename, 'r') as f:
        data = json.load(f)
    result = {key : data[key] for key in sorted(data)}
    with open(filename, 'w') as f:
        json.dump(result, f, indent=4)

Sort("Fuel.json")