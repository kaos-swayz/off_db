import json

def open_data(file_name):
    with open(file_name, "r", encoding="UTF-8") as fp:
        data = json.loads(fp.read())

    return data







if __name__ == "__main__":
    for e in open_data("raw_data.txt"):
        print(e)