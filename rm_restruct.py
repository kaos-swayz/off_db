import json

def open_data(file_name):
    with open(file_name, "r", encoding="UTF-8") as fp:
        data = json.loads(fp.read())

    return data

def restruct_data(data):
    output = []

    return output



def check_count(data):
    len_41 = 0
    len_43 = 0
    len_inne = 0
    for e in data:
        # print(len(e))
        if len(e) == 41:
            len_41 += 1
        elif len(e) == 43:
            len_43 += 1
        else:
            len_inne += 1
            print(len(e))
            print(e)
    print("len 41: {}, lend 43: {}, inne: {}".format(len_41, len_43, len_inne))



if __name__ == "__main__":
    data = open_data("raw_data.txt")
    print(data[0])

    check_count(data)

    restructed_data = restruct_data(data)
    print(len(restructed_data))