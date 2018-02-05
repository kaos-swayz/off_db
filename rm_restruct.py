import json

def open_data(file_name):
    with open(file_name, "r", encoding="UTF-8") as fp:
        data = json.loads(fp.read())

    return data

def restruct_data(data):
    output = []
    for e in data:
        item = {}
        output.append(item)
    return output






if __name__ == "__main__":
    data = open_data("raw_data.txt")
    restructed_data = restruct_data(data)
    print(len(restructed_data))